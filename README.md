# EbayAlert
A service to manage alerts for products prices on Ebay.com, the service will allow a user to create an alert so he can receive updates about specific products search phrases delivered to his email address.
# Django Alert Management System

The Django Alert Management System is a web application that allows users to create alerts for product prices on Ebay.com and receive updates delivered to their email address. The application provides a simple and convenient way to track and monitor product prices based on user-defined search phrases.

## Features

- User registration and authentication
- Alert creation with search phrase, email address, and frequency settings
- Scheduled email notifications with the first 20 products sorted by the lowest price
- CRUD operations for managing alerts

## Technologies Used

- Django: A high-level Python web framework for rapid development and clean design.
- SQLite: A lightweight and serverless database used for local development.
- Bootstrap: A popular CSS framework for responsive and modern user interfaces.
- Django Schedule: A library for creating and managing scheduled tasks within Django.
- Django SMTP Email: A built-in Django module for sending email notifications.

## Getting Started

### Prerequisites

- Python 3.x
- Django
- SQLite

### Installation

Clone the repository:

git clone https://github.com/arjunlimat/EbayAlert.git
Navigate to the project directory:

##

cd your-repo
Install the required dependencies:

##

pip install -r requirements.txt

Apply database migrations:

##

python manage.py migrate

Run the development server:
##
python manage.py runserver

Access the application in your web browser at http://localhost:8000.

##Usage
Register a new user account or log in to an existing account.
Create alerts by providing the search phrase, email address, and frequency.
Scheduled email notifications will be sent based on the specified frequency, containing the first 20 products sorted by the lowest price.
Manage your alerts by editing, deleting, or creating new ones.


##Acknowledgements
Django Documentation
Bootstrap Documentation
Django Schedule Documentation
Django SMTP Email Documentation


Feel free to modify and customize the README.md file according to your project's specific details, dependencies, and instructions.

Let me know if you need any further assistance!