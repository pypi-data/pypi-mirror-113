from django.core.management.base import BaseCommand

#-------------------------------------------------------------------------------
class Command(BaseCommand):
    """
    Sends out any notifications in the NotificationCenter queue
    """
    def handle(self, *args, **options):
        from ...models import default_center
        default_center.notify()
