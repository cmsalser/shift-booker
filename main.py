from scrapper import Scrapper
from database import DB
from logger import Logger
from mailer import Mailer
import time 

class App():
    def __init__(self):
        self.logger = Logger()
        self.db = DB()
        self.mailer = Mailer()

    
    def run(self):
        self.logger.log("App running...")
        while True:
            scrapper = Scrapper()
            shifts = scrapper.find_shifts()
            if len(shifts) > 0:
                for shift in shifts:
                    exists = self.db.handel_shift(shift)
                    if not exists:
                        self.mailer.send_message(shift)
            scrapper.close()
            time.sleep(600)

if __name__ == "__main__":
    app = App()
    app.run()