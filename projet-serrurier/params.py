from dotenv import load_dotenv
import os

# Charger les variables depuis le fichier .env
load_dotenv()

# Lire les variables d'environnement
SMS_API_KEY = os.getenv("SMS_API_KEY")
PHONE_NUMBERS = os.getenv("PHONE_NUMBERS")
SENDER_NAME = os.getenv("SENDER_NAME")
LOGIN_USERNAME = os.getenv("LOGIN_USERNAME")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
BROWSER_PATH1 = os.getenv("BROWSER_PATH1")
BROWSER_PATH2 = os.getenv("BROWSER_PATH2")
