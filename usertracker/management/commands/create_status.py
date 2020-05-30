from django.core.management.base import BaseCommand
from usertracker.models import THE_STATUSES, TheStatus

class Command(BaseCommand):
    help = 'get or create new status from TheStatus Model'


    def handle(self, *args, **kwargs):
        for x in THE_STATUSES:
            get, created = TheStatus.objects.get_or_create(name=x[0])
            self.stdout.write(self.style.WARNING(f'status of "{get.name}" already exists!'))
            if created:
                self.stdout.write(self.style.SUCCESS(f'status of "{created}" created with success!'))
