import collections
import datetime

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import JSONField
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import Model, Q
from django.utils import timezone
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.module_loading import import_string

from .util import PGAdvisoryLock

class Subscription(models.Model):
    sender_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
        related_name="notification_subscription_sender_types",
        on_delete=models.CASCADE
    )
    sender_id = models.PositiveIntegerField(null=True)
    sender = GenericForeignKey('sender_type', 'sender_id')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    digest = models.BooleanField(default=False)

    class Meta:
        app_label = 'notificationcenter'
        unique_together = ('user', 'notification_name', 'sender_type', 'sender_id', 'digest',)


class Notification(models.Model):
    """
    A Notification object contains the data necessary to send an email notification to users
    who are subscribed to receive notifications of type 'name' and, optionally, that relate
    to an associated 'sender' object.

    The 'context' property is intended to contain info about the nature of the notification.
    A common usage would be to include the ID of the user who triggered the action
    responsible for creating the notification.
    """
    sender_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
        related_name="notification_sender_types",
        on_delete=models.CASCADE
    )
    sender_id = models.PositiveIntegerField(null=True)
    sender = GenericForeignKey('sender_type', 'sender_id')

    context = JSONField(default=dict)

    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    html = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_sent = models.DateTimeField(blank=True, null=True)
    date_digested = models.DateTimeField(blank=True, null=True)
    recipients = JSONField(blank=True, null=True)

    def mark_as_sent(self, recipients=None):
        self.date_sent = timezone.now()
        self.recipients = recipients
        self.save()

#-------------------------------------------------------------------------------
class NotificationCenter(object):
    def __init__(self):
        self.from_email = settings.NOTIFICATION_CENTER_SENDER_EMAIL

        self.implicit_subscription_rules = []
        self.alter_recipient_rules = []

        self.digest_implicit_subscription_rules = []
        self.digest_alter_recipient_rules = []

        # The default email address used for a subscribed user is user.email
        # An email_accessor function may be assigned to customize this behavior.
        self.email_accessor = lambda user: user.email

    #--------------------------------------------------------------------------
    def add_implicit_subscription_rule(self, notification_name, rule_func, digest=False):
        if not digest:
            self.implicit_subscription_rules.append((notification_name, rule_func))
        else:
            self.digest_implicit_subscription_rules.append((notification_name, rule_func))

    def add_alter_recipient_rule(self, notification_name, rule_func, digest=False):
        if not digest:
            self.alter_recipient_rules.append((notification_name, rule_func))
        else:
            self.digest_alter_recipient_rules.append((notification_name, rule_func))

    #--------------------------------------------------------------------------
    def subscribe(self, user, notification_name, sender=None, digest=False, force=False):
        """
        Add an observer to the subscription table
        :return:
        """
        subscription_info = {
            'user': user,
            'notification_name': notification_name,
            'digest': digest,
            }

        if isinstance(sender, Model):
            subscription_info['sender_type'] = ContentType.objects.get_for_model(sender)
            subscription_info['sender_id'] = sender.id

        subscription, created = Subscription.objects.get_or_create(**subscription_info)

        if created or force:
            subscription.is_active = True

        subscription.save()

    #--------------------------------------------------------------------------
    def unsubscribe(self, user, notification_name, sender=None, digest=False):
        """
        Remove an observer from the subscription table
        :return:
        """
        subscription_info = {
            'user': user,
            'notification_name': notification_name,
            'digest': digest,
        }

        if isinstance(sender, Model):
            subscription_info['sender_type'] = ContentType.objects.get_for_model(sender)
            subscription_info['sender_id'] = sender.id

        try:
            subscription = Subscription.objects.get(**subscription_info)
            subscription.is_active = False
            subscription.save()
        except Subscription.DoesNotExist:
            subscription_info['is_active'] = False
            Subscription.objects.create(**subscription_info)

    #--------------------------------------------------------------------------
    def subscriptions(self, notification_name, sender=None, digest=False):
        sender_filter = Q(sender_type__isnull=True)
        if sender:
            sender_filter |= Q(
                sender_type=ContentType.objects.get_for_model(sender),
                sender_id=sender.id,
            )

        digest_filter = Q(digest=digest)

        notification_name_filter = Q(notification_name=notification_name)
        notification_subname = notification_name

        while True:
            separator_index = notification_subname.rfind(':')
            if separator_index == -1:
                break
            notification_subname = notification_subname[:separator_index]
            notification_name_filter |= Q(notification_name=notification_subname)

        return Subscription.objects.filter(sender_filter & digest_filter & notification_name_filter)

    #--------------------------------------------------------------------------
    def active_subscriptions(self, notification_name, sender=None, digest=False):
        return self.subscriptions(notification_name, sender=sender, digest=digest).filter(is_active=True)

    #--------------------------------------------------------------------------
    def inactive_subscriptions(self, notification_name, sender=None, digest=False):
        return self.subscriptions(notification_name, sender=sender, digest=digest).filter(is_active=False)

    #--------------------------------------------------------------------------
    def subscribers(self, notification_name, sender=None, digest=False):
        """
        Return the list of users subscribed to a notification of a given name
        and optionally, from a given sender

        :param notification_name:
        :param sender:
        :return:
        """

        # Update recipient list with any applicable alteration rules
        subscribers = set()
        if not digest:
            implicit_subscription_rules = self.implicit_subscription_rules
        else:
            implicit_subscription_rules = self.digest_implicit_subscription_rules

        for implicit_subscription_notification_name, alter_subscribers_func in implicit_subscription_rules:
            if notification_name.startswith(implicit_subscription_notification_name):
                alter_subscribers_func(subscribers, notification_name, sender)

        # Get the list of explicit subscribers to the given notification
        active_subscriptions = self.active_subscriptions(notification_name, sender=sender, digest=digest)
        subscribers.update([s.user for s in active_subscriptions])

        # Exclude those who have explicitily unsubscribed
        inactive_subscriptions = self.inactive_subscriptions(notification_name, sender=sender, digest=digest)
        subscribers.difference_update([s.user for s in inactive_subscriptions])

        return subscribers

    #--------------------------------------------------------------------------
    def post_notification(self, notification_name, sender, subject, text='', html=None,
                          link=None, context=None, notify_immediately=False):
        """
        :param notification_name:
        :param sender:
        :param subject:
        :return:
        """
        # TODO: Raise an error if the subject is malformed (ex: contains newlines)?

        notification_info = {
            'name': notification_name,
            'subject': subject,
            'text': text,
            'html': html,
            'link': link,
            'context': context if context else {},
        }

        if isinstance(sender, Model):
            notification_info['sender_type'] = ContentType.objects.get_for_model(sender)
            notification_info['sender_id'] = sender.id

        notification = Notification.objects.create(**notification_info)

        if notify_immediately:
            self.notify({ 'pk': notification.id })

    #--------------------------------------------------------------------------
    def notify(self, filter_params=None):
        """
        :return:
        """
        with PGAdvisoryLock("NotificationCenter.notify"):
            qs_params = { 'date_sent__isnull': True }
            if filter_params:
                qs_params.update(filter_params)
            notifications = Notification.objects.filter(**qs_params).order_by('date_created')

            for notification in notifications:
                notification_context = notification.context

                # Determine the list of subscriber email addresses
                subscribers = self.subscribers(notification.name, sender=notification.sender)
                email_addresses = set([self.email_accessor(user) for user in subscribers])

                # Update email recipient list with any applicable alteration rules
                for notification_name, alter_recipients_func in self.alter_recipient_rules:
                    if notification.name.startswith(notification_name):
                        alter_recipients_func(email_addresses, notification)

                # Remove any falsy email address values that might've accumulated
                email_addresses.discard(None)
                email_addresses.discard('')

                # If there are any subscribers to this notification, send an email
                if email_addresses:
                    headers = notification_context.get('headers')
                    email = EmailMultiAlternatives(
                        subject=notification.subject,
                        body=notification.text,
                        from_email=self.from_email,
                        to=None,
                        bcc=email_addresses,
                        headers=headers
                    )

                    if notification.html:
                        email.attach_alternative(notification.html, "text/html")

                    try:
                        email.send(fail_silently=False)
                        notification.mark_as_sent({
                            'bcc': list(email_addresses),
                        })
                    except Exception as e:
                        # TODO: Log that the send failed
                        print(e)
                        pass
                else:
                    # If there are no subscribers to this notification, don't bother
                    # constructing an email. Simply mark it as sent.
                    notification.mark_as_sent()


    #---------------------------------------------------------------------------
    def digest(self, subject, grouping, template, recipients=None):
        """
        Send out a digest of all notifications for users that want a summary.

        :param grouping: a dictionary of notification name lists.

        digest({'active': ['purchasing:purchase_order:approve'], 'activity': ['purchasing:purchase_order:approve']})

        :return:
        """
        notifications = Notification.objects.filter(date_digested__isnull=True).order_by('date_created')
        digests = {}

        # When grouping, limit the notifications to the grouping set.
        names = []
        for key, ns in grouping:
            names = names + ns
        notifications = notifications.filter(
                name__in=names
            ).order_by(
                'sender_type', 'sender_id', 'name'
            )
        notifications = sorted(notifications, key=lambda x: x.date_created)

        for notification in notifications:
            subscribers = self.subscribers(notification.name, sender=notification.sender, digest=True)
            email_addresses = set([self.email_accessor(user) for user in subscribers])

            # Update email recipient list with any applicable alteration rules.
            for notification_name, alter_recipients_func in self.digest_alter_recipient_rules:
                if notification.name.startswith(notification_name):
                    alter_recipients_func(email_addresses, notification)

            email_addresses.discard(None)

            for email in email_addresses:
                digest = digests.get(email, collections.OrderedDict())
                for key, names in grouping:
                    group = digest.get(key, [])
                    if notification.name in names:
                        group.append(notification)
                    digest[key] = group
                digests[email] = digest

            # Mark this notification as having been digested.
            notification.date_digested = timezone.now()
            notification.save()

        # Send out the digested emails.
        for email, notifications in digests.items():

            # Scrub duplicate items.
            for key, values in notifications.items():
                unique = collections.OrderedDict()
                for notification in values:
                    unique[notification.sender] = notification
                notifications[key] = unique.values()

            context = {
                'today': datetime.date.today(),
                'notifications': notifications,
            }
            html = render_to_string(template, context)

            if (recipients and email in recipients) or recipients is None:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=strip_tags(html),
                    from_email=self.from_email,
                    to=[email],
                )
                email.attach_alternative(html, 'text/html')

                try:
                    email.send()
                except Exception:
                    pass

# A ready-to-import-and-use instance of the NotificationCenter
default_center = NotificationCenter()
if hasattr(settings, 'DEFAULT_NOTIFICATION_CENTER_EMAIL_ADDRESS_ACCESSOR'):
    default_center.email_accessor = import_string(settings.DEFAULT_NOTIFICATION_CENTER_EMAIL_ADDRESS_ACCESSOR)
