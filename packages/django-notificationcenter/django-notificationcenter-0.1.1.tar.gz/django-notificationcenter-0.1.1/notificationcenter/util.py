import traceback

from django.conf import settings
from django.core import mail
from django.core.mail import mail_admins
from django.db import connection
from django.db.utils import OperationalError

#-------------------------------------------------------------------------------
class PGAdvisoryLock(object):
    """
   Locks database operations on a sandbox with a pg_advisory lock.

   Use the same shared lock_value to ensure mutually exlusive access to
   the desired database records.
   """
    #---------------------------------------------------------------------------
    def __init__(self, lock_value):
        self.lock_hash = hash(lock_value)

    #---------------------------------------------------------------------------
    def __enter__(self):
        db_engine = settings.DATABASES['default']['ENGINE']
        if db_engine == 'django.db.backends.postgresql_psycopg2':
            cursor = connection.cursor()
            cursor.execute('SELECT pg_advisory_lock(%s)' % self.lock_hash)

    #---------------------------------------------------------------------------
    def __exit__(self, type, value, traceback):
        db_engine = settings.DATABASES['default']['ENGINE']
        if db_engine == 'django.db.backends.postgresql_psycopg2':
            cursor = connection.cursor()
            cursor.execute('SELECT pg_advisory_unlock(%s)' % self.lock_hash)


#------------------------------------------------------------------------------
class EmailCheck:
    """
    A context manager for use in email notification testing. Appearing within
    a test method as

        with EmailContext(self, users=[user1, ...]) as _:
            <block>

    or

        with EmailContext(self, contacts=[contact1, ...]) as _:
            <block>

    it will ensure that execution of <block> results in sending email to
    the given list of users/contacts. Note that exactly one of users and
    contacts must be provided. Note also that either users or contacts
    can be given as a function of one null argument; this is useful when
    the recipient list must be calculated after execution of the block.

    """
    def __init__(self, context, options, strict=True):
        self.context = context
        self.strict = strict
        self.options = options

        from .models import default_center as notification_center
        self.notification_center = notification_center

    def __enter__(self):
        # Clear the mail outbox
        mail.outbox = []
        return None

    def __exit__(self, exc_type, exc_value, trace):
        # Defer handling of any raised exceptions
        if exc_type:
            return False

        from .models import default_center as notification_center

        # Trigger notification delivery (is this really necessary?)
        self.notification_center.notify()

        # Ensure the mail outbox contains the expected message.
        messages = [msg for msg in mail.outbox]
        message_count = len(messages)

        recipients = self.options.get('recipients')

        if recipients:
            self.context.assertEqual(message_count, 1, "Unable to find expected message")
            message = messages[0]

            # Ensure that message has the expected bcc recipients
            expected = set()
            for recipient in recipients:
                if isinstance(recipient, str):
                    expected.add(recipient)
                else:
                    expected.add(self.notification_center.email_accessor(recipient))
            observed = set(message.recipients())
            self.context.assertEqual(expected - observed, set(), "missing recipients: %s" % (expected - observed))

            # Optionally require an exact match of bcc recipients
            if self.strict:
                self.context.assertEqual(observed - expected, set(), "extraneous recipients: %s" % (observed - expected))

            expected_subject = self.options.get('subject')
            if expected_subject:
                self.context.assertEqual(message.subject, expected_subject)

            expected_body_content = self.options.get('body')
            if expected_body_content:
                if not isinstance(expected_body_content, list):
                    expected_body_content = list(expected_body_content)

                for substring in expected_body_content:
                    self.context.assertIn(substring, message.body)

        else:
            self.context.assertEqual(message_count, 0, "An email was unexpectedly sent")

        return True


#-------------------------------------------------------------------------------
class NotifyOnError():
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_value, exc_traceback):
        # If an error was raised, email it to the admins.
        # Return False, as we wish to allow the exception to be re-raised
        if (exc_type and exc_value and exc_traceback):
            message_body = '\n'.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            mail_admins(
                "An uncaught exception has occurred",
                message_body,
                fail_silently=True
            )
        return False
