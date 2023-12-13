# Projet Serrurier

## Description

Projet Serrurier is a Python application designed to automate the monitoring and management of phone calls in a professional context. The application uses Selenium and Python to scrutinize a call logging system, identify important calls, and send notifications via SMS.
It was created at the request of a locksmith who deals with emergencies. Customers sometimes wait no more than 10 seconds on the phone, so they hang up, which leads to a loss of customers. Thanks to this python program, once the locksmith has finished his callback, he knows that someone has tried to contact him and has his contact details by text message.

## Prerequisites

- Python 3.8 or newer
- Python libraries: Selenium, PyVirtualDisplay, PyTZ (see `requirements.txt` for the complete list)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/monsieurgoodmood/projet-serrurier.git

## Install dependencies:

pip install -r requirements.txt

## Configuration

Create a .env file at the root of the project with the following variables:
SMS_API_KEY=your_api_key
PHONE_NUMBERS=phone_number1, phone_number2, etc.
SENDER_NAME=YourName
LOGIN_USERNAME=your_username
LOGIN_PASSWORD=your_password
CHROME_DRIVER_PATH=path/to/chromedriver
BROWSER_PATH1=login_url
BROWSER_PATH2=call_log_url

Adjust the values according to your environment and credentials.

## Usage

Run the main script to start the application:
python main.py

## Project Structure

lesclefsdubonheur/: Python virtual environment folder.
main.py: The main script of the project.
params.py: Management of environment variables.
requirements.txt: List of project dependencies.

## Contribution
If you wish to contribute to the project, please follow these instructions:

Fork the repository
Create a new branch for your features
Submit a pull request with a detailed description

## Contact
For any questions or suggestions, feel free to contact me, Arthur Choisnet at arthur.choisnet74@gmail.com
