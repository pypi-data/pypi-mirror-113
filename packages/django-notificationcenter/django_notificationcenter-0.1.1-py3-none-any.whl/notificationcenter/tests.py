from django.core import mail
from django.contrib.auth import get_user_model
from django.test import TestCase

from notificationcenter.models import NotificationCenter

User = get_user_model()
PASSWORD = '12345'

class NotificationCenterTests(TestCase):
    def setUp(self):
        # Create a few users to serve as observers to notification
        self.ricky = self._create_user('ricky', 'ricky@swearnet.com')
        self.julian = self._create_user('julian', 'julian@swearnet.com')
        self.bubbles = self._create_user('bubbles', 'bubbles@swearnet.com')

        self.notification_center = NotificationCenter()

    def _create_user(self, username, email):
        user, _ = User.objects.get_or_create(username=username, email=email)
        user.is_active = True
        user.set_password(PASSWORD)
        user.save()
        return user

    def test_event_notification(self):
        notification_name = 'trailerparkboys:cyrus_is_out_of_jail'
        notification_info = {
            'sender': None,
            'subject': "Cyrus was sprung from jail and he's coming for the driveway",
            'text': "Cyrus is on his way. We're gonna have a gunfight on our hands",
            'html': "<html><body>Cyrus is on his way. We're gonna have a gunfight on our hands</body></html>",
        }


        # Post a notification with no subscribers. Ensure no email is sent.
        mail.outbox = []
        self.notification_center.post_notification(notification_name, **notification_info)
        self.notification_center.notify()
        self.assertEqual(0, len(mail.outbox))

        # Subscribe a few users to that notification, post another notification, then process
        mail.outbox = []
        self.notification_center.subscribe(self.ricky, notification_name)
        self.notification_center.subscribe(self.julian, notification_name)
        self.notification_center.post_notification(notification_name, **notification_info)
        self.notification_center.notify()

        # Test that an email was sent to ricky and julian
        self.assertEqual(1, len(mail.outbox))
        message = mail.outbox[0]

        mail.outbox = []
        self.notification_center.unsubscribe(self.ricky, notification_name)
        self.notification_center.unsubscribe(self.julian, notification_name)
        self.notification_center.post_notification(notification_name, **notification_info)
        self.notification_center.notify()

        self.assertEqual(0, len(mail.outbox))

    def test_event_notification_with_sender(self):
        notification_name = 'trailerparkboys:hungry_kitty'

        purrmonster = self._create_user(username='purrmonster', email="purrmonster@kittylandlovecenter.com")
        shitrock = self._create_user(username='shitrock', email="purrmonster@kittylandlovecenter.com")

        # Bubbles wants to receive notifications about all hungry kitties
        self.notification_center.subscribe(self.bubbles, notification_name)

        # Ricky and Julian are only interested in notifications about specific hungry kitties
        self.notification_center.subscribe(self.ricky, notification_name, sender=purrmonster)
        self.notification_center.subscribe(self.julian, notification_name, sender=shitrock)

        purrmonster_notification_subject = "Ever since Lahey locked up food mountain, Purrmonster has been scavenging for scraps."
        self.notification_center.post_notification(
            notification_name,
            subject=purrmonster_notification_subject,
            sender=purrmonster
        )
        shitrock_notification_subject = "Shitrock has gone missing again and probably hasn't eaten in days."
        self.notification_center.post_notification(
            notification_name,
            subject=shitrock_notification_subject,
            sender=shitrock
        )
        self.notification_center.notify()

        # Ensure two notification emails were sent
        self.assertEqual(2, len(mail.outbox))

        # Verify that only bubbles and ricky received a notification about purrmonster
        purrmonster_message = mail.outbox[0]
        self.assertEqual(purrmonster_message.subject, purrmonster_notification_subject)
        self.assertEqual(set(purrmonster_message.recipients()), set([self.ricky.email, self.bubbles.email]))

        # Verify that only Bubbles and Julian received a notification about shitrock
        shitrock_message = mail.outbox[1]
        self.assertEqual(shitrock_message.subject, shitrock_notification_subject)
        self.assertEqual(set(shitrock_message.recipients()), set([self.julian.email, self.bubbles.email]))

    def test_event_notification_digest(self):
        mail.outbox = []
        notification_name = 'trailerparkboys:cyrus_is_out_of_jail'

        # Subscribe a few digest users to the notifications.
        self.notification_center.subscribe(self.ricky, notification_name, digest=True)
        self.notification_center.subscribe(self.julian, notification_name, digest=True)

        notification_info = {
            'sender': None,
            'subject': "Cyrus was sprung from jail and he's coming for the driveway",
            'text': "Cyrus is on his way. We're gonna have a gunfight on our hands",
            'html': "<html><body>Cyrus is on his way. We're gonna have a gunfight on our hands</body></html>",
            'link': "https://www.wikipedia.org"
        }
        self.notification_center.post_notification(notification_name, **notification_info)
        self.notification_center.notify()
        self.assertEqual(len(mail.outbox), 0)

        notification_info = {
            'sender': None,
            'subject': "Just a false alarm, Trever is an idiot",
            'text': "Trevor is an idiot, he was confused about seeing Cyrus",
            'html': "<html><body>Trevor is an idiot, he was confused about seeing Cyrus</body></html>",
            'link': "https://www.wikipedia.org"
        }
        self.notification_center.post_notification(notification_name, **notification_info)
        self.notification_center.notify()
        self.assertEqual(len(mail.outbox), 0)

        self.notification_center.digest(
            'Test Digest', [
                ('test', ['trailerparkboys:cyrus_is_out_of_jail'])
            ], 'notificationcenter/digest.html'
        )
        self.assertEqual(len(mail.outbox), 2)

