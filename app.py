Since Google Cloud Run requires a billing credit card, I want to deploy my Python Flask webhook on a completely free alternative like Render.com.

Here is my code for `app.py`:

import imaplib
import email
from flask import Flask

app = Flask(__name__)

EMAIL_ACCOUNT = "Ivanatamrat@gmail.com"
APP_PASSWORD = "zqeynlscgwnxemnc"

last_signal = "NO_SIGNAL"

def check_tradingview_emails():
    global last_signal
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
        mail.select('inbox')
        
        status, messages = mail.search(None, '(UNSEEN FROM "noreply@tradingview.com")')
        
        if status == 'OK':
            email_ids = messages[0].split()
            for e_id in email_ids:
                res, msg_data = mail.fetch(e_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            last_signal = part.get_payload(decode=True).decode().strip()
                else:
                    last_signal = msg.get_payload(decode=True).decode().strip()
                    
        mail.close()
        mail.logout()
    except Exception as e:
        print("Error checking emails:", e)

@app.route('/get_signal')
def get_signal():
    check_tradingview_emails()
    return last_signal

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

Please do the following:
1. Provide the `requirements.txt` file (I need gunicorn and Flask).
2. Give me the easiest, step-by-step instructions on how to host this code for free on Render.com (using Web Services) without needing a credit card.
3. Show me how to set the Start Command (e.g., gunicorn app:app) so I can get my live URL for my MT4 EA.
