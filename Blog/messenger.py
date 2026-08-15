import os
from dotenv import load_dotenv
import smtplib
load_dotenv()

class NotificationManager:
    def __init__(self):
        self.email = os.getenv('EMAIL_ADDRESS')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.address = os.getenv('SMTP_ADDRESS')

    def send_email(self,to_email_address,text):
        with smtplib.SMTP(self.address, port=587) as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.password)
            connection.sendmail(from_addr=self.email,
                                to_addrs=to_email_address,
                                msg=text)