import http.client
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import re
import pytz
from pyvirtualdisplay import Display
import params

# Utilisation des variables
api_key = params.SMS_API_KEY
phone_numbers = params.PHONE_NUMBERS
sender_name = params.SENDER_NAME
username = params.LOGIN_USERNAME
password = params.LOGIN_PASSWORD
chrome_driver_path = params.CHROME_DRIVER_PATH
browser_link1 = params.BROWSER_PATH1
browser_link2 = params.BROWSER_PATH2

# Reste de votre code


display = Display(visible=0, size=(800, 600))
display.start()

def send_sms_via_smspartner(phone_number, call_time):
    conn = http.client.HTTPSConnection("api.smspartner.fr")
    message = f"Numéro: {phone_number}, Heure d'appel: {call_time.strftime('%d/%m/%Y %H:%M:%S')}"
    payload = json.dumps({
        "apiKey": api_key,
        "phoneNumbers": phone_number,
        "sender": sender_name,
        "gamme": 1,
        "message": message
    })
    headers = {
        'Content-Type': 'application/json',
        'Content-Length': str(len(payload)),
        'cache-control': 'no-cache'
    }
    conn.request("POST", "/v1/send", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def login():
    browser.get(browser_link1)
    wait = WebDriverWait(browser, 20)
    username_elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#content > login-component > div > div > form > div > div:nth-child(1) > input')))
    username_elem.send_keys(username)
    password_elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#content > login-component > div > div > form > div > div:nth-child(2) > input')))
    password_elem.send_keys(password)
    password_elem.send_keys(Keys.RETURN)
    time.sleep(5)
    browser.get(browser_link2)

# Configuration des options de Chrome
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--enable-logging --v=1")
chrome_options.add_argument("--enable-logging")
chrome_options.add_argument("--v=1")

# Utilisation du chemin complet vers Chromedriver et options pour chrome_options
browser = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
login()

sent_messages_times = {}

while True:
    try:
        browser.refresh()
        wait = WebDriverWait(browser, 30)
        rows_found = False
        max_attempts = 5
        attempt = 0

        while not rows_found and attempt < max_attempts:
            try:
                table_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#callLogsTable > tbody')))
                rows = table_elem.find_elements(By.TAG_NAME, 'tr')
                if rows:
                    rows_found = True
                else:
                    attempt += 1
                    time.sleep(5)
            except:
                attempt += 1
                time.sleep(5)

        if not rows_found:
            print("Aucune ligne trouvée dans le tableau après plusieurs tentatives. Continuez...")
            continue

        paris_timezone = pytz.timezone('Europe/Paris')
        current_time = datetime.datetime.now(paris_timezone)

        for i in range(1, len(rows) + 1):
            time_selector = f'#callLogsTable > tbody > tr:nth-child({i}) > td:nth-child(1)'
            phone_selector = f'#callLogsTable > tbody > tr:nth-child({i}) > td:nth-child(2)'
            duration_selector = f'#callLogsTable > tbody > tr:nth-child({i}) > td:nth-child(4)'

            time_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, time_selector)))

            print("Valeur de time_elem.text:", time_elem.text)

            date_str = time_elem.text
            # Interprétation de la date
            if "AM" in date_str or "PM" in date_str:
                call_time_naive = datetime.datetime.strptime(date_str, "%m/%d/%Y %I:%M:%S %p")
            else:
                call_time_naive = datetime.datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")

            # Conversion de l'heure de UTC vers le fuseau horaire de Paris
            utc_timezone = pytz.timezone('UTC')
            paris_timezone = pytz.timezone('Europe/Paris')
            call_time_utc = utc_timezone.localize(call_time_naive)
            call_time = call_time_utc.astimezone(paris_timezone)

            treat_as_valid_call = False  # Initialisation à False

            phone_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, phone_selector)))
            if phone_elem.text == "Anonymous":
                phone_number = "Appel numéro masqué"
                treat_as_valid_call = True
            elif phone_elem.text in ["non répondu", "Not Answered"]:
                phone_number = "Appel non répondu"
                treat_as_valid_call = True
            else:
                phone_number = re.sub("[^0-9]", "", phone_elem.text)

            duration_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, duration_selector)))
            duration_text = duration_elem.text

            if duration_text in ["Anonymous", "Not Answered"]:
                duration_seconds = 2  # On donne une durée de 2 secondes pour déclencher l'envoi du SMS.
            elif ":" in duration_text:
                duration_parts = duration_text.split(":")
                duration_seconds = int(duration_parts[0]) * 3600 + int(duration_parts[1]) * 60 + int(duration_parts[2])
            else:
                duration_seconds = 0
            if duration_seconds >= 2 and (current_time - call_time).total_seconds() <= 1800:
                last_sent_time = sent_messages_times.get(phone_number)
                if not last_sent_time or (current_time - last_sent_time).total_seconds() > 1800:
                    response = send_sms_via_smspartner(phone_number, call_time)
                    sent_messages_times[phone_number] = current_time
                    print(f"SMS envoyé pour le numéro {phone_number} à {call_time}")  # Log de débogage
                    print(f"Réponse de SMS Partner : {response}")  # Pour voir la réponse de SMS Partner
                else:
                    print(f"SMS déjà envoyé pour le numéro {phone_number} à {call_time}")  # Log de débogage

    except Exception as e:
        error_message = str(e)
        if "exceeded the 1 rps rate limit" in error_message:
            print("Erreur de limite de taux détectée. Attente avant de réessayer...")
            time.sleep(60)
            continue
        else:
            print(f"Erreur détectée : {e}. Tentative de redémarrage du navigateur dans 10 secondes...")
            time.sleep(10)
            browser.quit()
            browser = webdriver.Chrome()
            login()
