### EbayAlert
A service to manage alerts for products prices on Ebay.com, the service will allow a user to create an alert so he can receive updates about specific products search phrases delivered to his email address.
This EbayAlert is a web application that allows users to create alerts for product prices on Ebay.com and receive updates delivered to their email address. The application provides a simple and convenient way to track and monitor product prices based on user-defined search phrases.
This project allows users to set up alerts for specific product searches on eBay and receive periodic email notifications with the lowest-priced products matching their search criteria. The alerts can be configured to trigger every 2, 10, or 30 minutes.

- Users can create alerts by providing the search phrase, email address, and frequency (2, 10, or 30 minutes).
- The system periodically fetches the lowest-priced products from eBay using the eBay Finding API based on the search phrase.
- If new products are found or the prices change, an email is sent to the user's email address using the Mailgun API.
- The email contains a table with the details of the matching products, including the title, URL, location, and price.

### Features

- User registration and authentication
- Alert creation with search phrase, email address, and frequency settings
- Scheduled email notifications with the first 20 products sorted by the lowest price
- CRUD operations for managing alerts
- Currently used default SQLite3 database but we can use PostgreSQL database (Scalability).

### Technologies Used

- Django: A high-level Python web framework for rapid development and clean design.
- SQLite3: A lightweight and serverless database used for local development.
- HTML,React: A popular UI react framework for creating alert with HTMK template.
- Django Schedule: A library for creating and managing scheduled tasks within Django.
- Mail Gun:  Powerful email delivery service and email automation platform. 
It provides developers with a set of APIs that allow easy integration of email functionality into applications and websites.

### Getting Started

### Prerequisites

- Python 3.x
- Django
- SQLite3
- Mail GUN API Key
- Ebay Finding API APP-NAME

### Installation

Clone the repository:

git clone https://github.com/arjunlimat/EbayAlert.git
Navigate to the project directory:

cd EbayAlert

Please go to Alerts/config.py , replace the with the appropriate values
### config.py
DEV = {
    'SECURITY-APPNAME': 'yourappname',
    'MAILGUN_APIKEY': 'mailgunapi',
    'EBAY_API_URL': 'EBAY_API_URL', 
    'MAILGUN_SENDER': 'MAILGUN_SENDER',
    'MAILGUN_API_URL': 'MAILGUN_API_URL',
}

### Install the required dependencies:

pip install -r requirements.txt

### Apply database migrations:

python manage.py migrations Alerts

python manage.py migrate

### Run the development server:

docker-compose up

Access the application in your web browser at http:/localhost:8080/api/alerts/create/.

### APIs

### http:/localhost:8080/api/alerts/list/ 

- Show the list of alerts

### http:/localhost:8080/api/alerts/create/ 

- Allows user to create alert and make sure this mail id added mail gun sandbox account verified list.

### http:/localhost:8080/api/alerts/1/update/ 

- Update the alert based on alert id (Above alert id 1)

### http:/localhost:8080/api/alerts/1/delete/  

- Delete the alert based on alert id (Above alert id 1 is getting deleted)

### Usage
Create alerts by providing the search phrase, email address, and frequency.
Scheduled email notifications will be sent based on the specified frequency, containing the first 20 products sorted by the lowest price.
Manage your alerts by editing, deleting, or creating new ones.

The project leverages the eBay Finding API to search for products based on keywords.
It utilizes the Mailgun API for sending email notifications to users. 
The scheduler.py file contains the scheduling logic for periodically fetching products and sending email notifications. 
The views.py file defines the API endpoints for creating, retrieving, updating, and deleting alerts. 
The models.py file contains the database models for storing the alert and price data.

### Obtain API credentials:
eBay Finding API: Sign up for an eBay developer account and obtain the necessary API credentials.
Mailgun API: Sign up for a Mailgun account and obtain the API key and domain.

- Update the eBay API credentials in the search_ebay function in scheduler.py and phase2_scheduler.py.
- Update the Mailgun API credentials and email settings in the send_email function in scheduler.py and phase2_scheduler.py.

The provided docker-compose.yml file defines three services: web, scheduler1, and scheduler2. Here's a breakdown of each service:

### web service:

It builds the image using the Dockerfile in the current context.
Maps port 8080 of the container to port 8080 of the host machine.
Executes the command python manage.py runserver 0.0.0.0:8080 to start the Django development server.
Below both schedulers are depends upon django serivice, so it necessary to start django first.

### scheduler1 service:
It also builds the image using the same Dockerfile in the current context.
Executes the command sh -c "sleep 20 && python Alerts/scheduler.py" to wait for 20 seconds and then run the scheduler.py script inside the container.
This scheduler will fetch data from Alerts table and send mail using Mail Gun service.
I was using Mail Gun sandbox service to send mail . Please create Mail Gun sandbox account and add your mail id and verified participants.
Then use the add your mail id into above alerts. 
This service handles below requirement:
- User should obtain the first 20 products sorted by the lowest price every 2, 10 or 30 minutes
delivered to his email address as per alert configuration.

### scheduler2 service:
It also builds the image using the same Dockerfile in the current context.
Executes the command sh -c "sleep 25 && python Alerts/phase2_scheduler.py" to wait for 25 seconds and then run the phase2_scheduler.py script inside the container.
This configuration allows you to start the Django server first and then start the two schedulers with a delay of 20 and 25 seconds, respectively, after the Django server is up and running.
This service handles below requirement
- New cheaper product is available for your search and
- Your search results didn’t have price changes over the last 2 days, act now before prices
change

- Above both scheduler functionality can also be implemented by cron job or aws lambda or azure function to trigger.
### Unit test cases
- created django unit test cases inside tests.py

### Acknowledgements
- Django Documentation
- Django Schedule Documentation
- Mail Gun API Documentation
- EBay Developers API Documentation

Feel free to modify and customize the README.md file according to your project's specific details, dependencies, and instructions.

Let me know if you need any further assistance!