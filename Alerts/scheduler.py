from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from Alerts.models import Alert
import schedule
import time

class Command(BaseCommand):
    help = 'Starts the email scheduler'

    def handle(self, *args, **options):
        # Schedule the email sending task for all alerts in the database
        for alert in Alert.objects.all():
            self.schedule_email(alert)

        # Run the scheduler in a separate thread
        while True:
            schedule.run_pending()
            time.sleep(1)

    def send_email(self, alert):
    # Get the data for the table (example DataFrame)
    data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
    df = pd.DataFrame(data)
    # Convert the DataFrame to an HTML table
    table_html = df.to_html(index=False)
    # Send the email with the HTML table in the body
    send_mail(
        'Alert',
        f'You have a new alert for search phrase: {alert.search_phrase}\n\n{table_html}',
        'from@example.com',
        [alert.email],
        fail_silently=False,
    )

    def schedule_email(self, alert):
        # Convert frequency from minutes to seconds
        interval_seconds = alert.frequency * 60

        # Schedule the email sending task for the alert
        schedule.every(interval_seconds).seconds.do(self.send_email, alert)
