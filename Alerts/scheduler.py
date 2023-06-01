
# Get the data for the table (example DataFrame)
#data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
#df = pd.DataFrame(data)
# Convert the DataFrame to an HTML table
#table_html = df.to_html(index=False)
# Send the email with the HTML table in the body
#send_mail('Alert',f'You have a new alert for search phrase: {alert.search_phrase}\n\n{table_html}',
#        'from@example.com',[alert.email],fail_silently=False,)


import schedule
import time
import requests
import pandas as pd
from datetime import datetime, timedelta

# Dictionary to store the last sent time for each alert
last_sent_times = {}

def get_alerts():
    print('inside get_alerts method')
    response = requests.get('http://127.0.0.1:8000/api/alerts/list/')
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to fetch alerts from the API.')
        return []

def send_email(alert):
    search_phrase = alert['search_phrase']
    email = alert['email']
    frequency = alert['frequency']

    # Check if it's time to send the email based on the frequency
    last_sent = last_sent_times.get(f"{email}_{search_phrase}_last_sent")

    if last_sent is None or last_sent + timedelta(minutes=get_minutes(frequency)) <= datetime.now():
        # Set up the Mailgun API request payload
        payload = {
            "from": "Mailgun Sandbox <postmaster@sandboxa81ff9ec1470403d876656d36da6d3ea.mailgun.org>",
            "to": email,
            "subject": "Alert",
            "text": f"A alert for '{search_phrase}' has been triggered (Frequency: {frequency})."
        }
        # Make the Mailgun API request
        response = requests.post(
            "http://api.mailgun.net/v3/sandboxa81ff9ec1470403d876656d36da6d3ea.mailgun.org/messages",
            auth = ("api", "c570d35e4bbfd9481d3847537b7c8f45-5d9bd83c-ac5c6863"),
            data = payload,
            verify = False
        )
        import pdb
        pdb.set_trace()
        # Check if the email was sent successfully
        if response.status_code == 200:
            print(f"Email sent to {email} successfully.")
            # Update the last sent time
            last_sent_times[f"{email}_{search_phrase}_last_sent"] = datetime.now()
        else:
            print(f"Failed to send email to {email}.")
    else:
        print(f"No need to send email for {email} at this time.")

def get_minutes(frequency):
    if '2' in frequency:
        return 2
    elif '10' in frequency:
        return 10
    elif '30' in frequency:
        return 30
    else:
        return 0

def task_to_execute():
    alerts = get_alerts()
    if alerts:
        for alert in alerts:
            send_email(alert)
    else:
        print('No alerts found.')

def schedule_job():
    alerts = get_alerts()
    if alerts:
        for alert in alerts:
            frequency = alert['frequency']
            minutes = get_minutes(frequency)
            if minutes > 0:
                # Create a job for each alert based on the frequency
                schedule.every(minutes).minutes.do(send_email, alert)
                # Set the initial last sent time to None
                last_sent_times[f"{alert['email']}_{alert['search_phrase']}_last_sent"] = None
            else:
                print(f"Invalid frequency specified for {alert['search_phrase']}: {frequency}")
    else:
        print('No alerts found.')

def run_scheduler():
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print('Scheduler stopped.')
            break

if __name__ == '__main__':
    schedule_job()
    run_scheduler()
