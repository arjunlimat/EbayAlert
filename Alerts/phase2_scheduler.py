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
from Alerts.models import Price
# Dictionary to store the last sent time for each alert
last_sent_times = {}
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
    response = requests.get(url, params=params, verify=False)
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

def check_price_changes():
    prices = Price.objects.all()
    for price in prices:
        search_phrase = price.item
        email = price.email_id
        current_price = search_ebay(search_phrase)
        
        if current_price is not None:
            current_price = float(current_price)
            
            if current_price < price.price:
                # Price has decreased, send email
                subject = "New cheaper product is available for your search"
                body = f"The price of the product '{search_phrase}' has decreased. Check it out now!"
                send_email_notification(email, subject, body)
            else:
                # Price has not changed
                subject = "No price changes"
                body = f"Your search results for '{search_phrase}' didn't have price changes over the last 2 days. Act now before prices change."
                send_email_notification(email, subject, body)
        else:
            print(f"Failed to retrieve current price for '{search_phrase}'")

def send_email_notification(email, subject, body):
    # Set up the Mailgun API request payload
    email_body = f"""
        <html>
        <head></head>
        <body>
        {body}
        </body>
        </html>
        """
    payload = {
        "from": DEV['MAILGUN_SENDER'],
        "to": email,
        "subject": subject,
        "html": email_body
    }

    # Make the Mailgun API request
    response = requests.post(
        DEV['MAILGUN_API_URL'],
        auth=("api", DEV['MAILGUN_APIKEY']),
        data=payload,
        verify=False
    )
    # Check if the email was sent successfully
    if response.status_code == 200:
        print(f"Email sent to {email} successfully.")
    else:
        print(f"Failed to send email to {email}.")

def schedule_job():
    # Schedule the job to run every 2 days
    schedule.every(2).days.do(check_price_changes)

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
