from scrapper import Scrapper
from logger import Logger
from mailer import Mailer
import time 

class App():
    def __init__(self):
        self.logger = Logger()
        self.mailer = Mailer()

    
    def run(self):
        self.logger.log("App running...")
        while True:
            scrapper = Scrapper()
            shifts = scrapper.find_shifts()
            if len(shifts) > 0:
                for message in shifts:
                    self.mailer.send_message(message)
            scrapper.close()
            time.sleep(300)

if __name__ == "__main__":
    app = App()
    app.run()