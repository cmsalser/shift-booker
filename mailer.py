from settings import TARGET_EMAIL
from creds import EMAIL_PASSWORD, EMAIL_USERNAME
from logger import Logger
from email.message import EmailMessage
import smtplib

def format_tuple(tuple):
    message = '===========\nDay: {0[0]}\nDate: {0[1]}\nTime: {0[2]}\nUnit: {0[3]}\nGrade: {0[4]}\n==========='.format(tuple)
    return message

class Mailer:

    def __init__(self):
        self.port = 587
        self.smtp = "smtp.gmail.com"
        self.logger = Logger("Mailer")
    
    def send_message(self, message):
        msg = EmailMessage()
        msg['From'] = EMAIL_USERNAME
        msg['To']  = TARGET_EMAIL
        msg['Subject']  = "Shift Found!"
        pretty_message = format_tuple(message)
        msg.set_content(pretty_message)

        try:
            server = smtplib.SMTP(self.smtp, self.port)
            server.ehlo()
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
            server.close()
            self.logger.log("Email successfully sent")
        except Exception as e:
            self.logger.log("Error - email may not have sent")
            self.logger.log(e)
