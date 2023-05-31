from django.core.management.base import BaseCommand
from Alerts.scheduler import Command as SchedulerCommand

class Command(BaseCommand):
    help = 'Starts the email scheduler'

    def handle(self, *args, **options):
        scheduler = SchedulerCommand()
        scheduler.handle()
