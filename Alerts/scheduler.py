import schedule
import time
import requests
import pandas as pd
from datetime import datetime, timedelta
import requests
import urllib.parse
import os
import sys
import django
# Dictionary to store the last sent time for each alert
last_sent_times = {}
from django.conf import settings
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the directory of the Django project (one folder back)
project_dir = os.path.abspath(os.path.join(script_dir, '..'))
# Add the project directory to the system path
sys.path.append(project_dir)
# Manually configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EbayAlert.settings")
django.setup()
# Now you can access the Django settings
installed_apps = settings.INSTALLED_APPS
# Start your scheduler logic here
from Alerts.models import Alert, Price
from config import DEV
def search_ebay(keyword):
    url = DEV['EBAY_API_URL']
    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.0.0",
        "SECURITY-APPNAME": DEV['SECURITY-APPNAME'],
        "RESPONSE-DATA-FORMAT": "JSON",
        "keywords": keyword,
        "itemFilter.paramName": "MinPrice",
        "paginationInput.entriesPerPage": 20
    }
    response = requests.get(url, params = params, verify = False)
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        if 'findItemsByKeywordsResponse' in data:
            search_response = data['findItemsByKeywordsResponse'][0]
            if 'searchResult' in search_response:
                search_result = search_response['searchResult'][0]
                if 'item' in search_result:
                    items = search_result['item']
                    # Create an empty DataFrame
                    df = pd.DataFrame(columns=['Title', 'URL', 'Location', 'Price'])
                    for item in items:
                        title = item.get('title', [''])[0]
                        viewItemURL = item.get('viewItemURL', [''])[0]
                        location = item.get('location', [''])[0]
                        currentPrice = item.get('sellingStatus', [{'currentPrice': [{'__value__': '0'}]}])[0]['currentPrice'][0]['__value__']
                        # Append values to DataFrame
                        # Append values to a temporary DataFrame
                        temp_df = pd.DataFrame({'Title': [title], 'URL': [viewItemURL], 'Location': [location], 'Price': [currentPrice]})
                        # Concatenate the temporary DataFrame with the main DataFrame
                        df = pd.concat([df, temp_df], ignore_index=True)
                    return df
                else:
                   return "No items found."
            else:
                return "No search results found."
        else:
            return "Invalid JSON response."
        
    else:
        print(f"Failed to retrieve search results from eBay API. Error code: {response.status_code}")
        return None

def get_alerts():
    print('inside get_alerts method')
    from django.core import serializers
    import json
    alerts = Alert.objects.all()
    serialized_data = serializers.serialize('json', alerts)
    data = json.loads(serialized_data)
    converted_data = []
    for item in data:
        new_item = {'id': item['pk']}
        new_item.update(item['fields'])
        converted_data.append(new_item)
    return converted_data
   # if response.status_code == 200:
   #     return response.json()
   # else:
   #     print('Failed to fetch alerts from the API.')
   #     return []

def send_email(alert):
    search_phrase = alert['search_phrase']
    email = alert['email']
    frequency = alert['frequency']
    response_data = search_ebay(search_phrase)
    table_html = response_data.to_html(index=False) 
    # Check if it's time to send the email based on the frequency
    last_sent = last_sent_times.get(f"{email}_{search_phrase}_last_sent")
    first_row = response_data.iloc[0]
    title = first_row['Title']
    viewItemURL = first_row['URL']
    location = first_row['Location']
    currentPrice = first_row['Price']        
    # Check if a record with the same email and frequency already exists
    existing_price = Price.objects.filter(email_id=email, frequency=frequency)     
    if existing_price:
        # Delete the existing record
        existing_price.delete()
     
    # Create a new Price object and save it to the database
    price = Price(item=title, email_id=email, price=currentPrice, frequency=frequency)
    price.save()
    if last_sent is None or last_sent + timedelta(minutes=get_minutes(frequency)) <= datetime.now():
        # Set up the Mailgun API request payload
        email_body = f"""
                    <html>
                    <head></head>
                    <body>
                    {table_html}
                    </body>
                    </html>
                    """
        payload = {
            "from": DEV['MAILGUN_SENDER'],
            "to": email,
            "subject": "Alert",
            "html": email_body
           # "text": f"A alert for '{search_phrase}' has been triggered (Frequency: {frequency})\n\n{table_html}."
        }
        
        # Make the Mailgun API request
        response = requests.post(
            DEV['MAILGUN_API_URL'],
            auth = ("api", DEV['MAILGUN_APIKEY']),#"YOUR_API_KEY"
            data = payload,
            verify = False
        )
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
