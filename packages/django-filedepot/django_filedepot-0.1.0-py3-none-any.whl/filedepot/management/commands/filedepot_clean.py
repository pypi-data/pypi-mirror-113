import datetime

from django.core.management.base import BaseCommand

from ...models import File

#-------------------------------------------------------------------------------
class Command(BaseCommand):
    """
    The filedepot_clean command is used to filedepot records (and associated
    files) that are more than one day old.

    python manage.py filedepot_clean
    """
    help = 'Remove filedepot records that are more than one day old.'

    #---------------------------------------------------------------------------
    def handle(self, *args, **options):
        now = datetime.datetime.now()
        two_days_ago = now - datetime.timedelta(days=2)

        for file in File.objects.filter(date_created__lt=two_days_ago):
            file.delete()
