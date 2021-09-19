from datetime import datetime
from logger import Logger
import sqlite3

def get_dates(date, time):
        start = datetime.strptime(date + " " + time.split(' ')[0], "%d %b %Y %H:%M")
        end = datetime.strptime(date + " " + time.split(' ')[2], "%d %b %Y %H:%M")
        return (start, end)

class DB:
    def __init__(self):
        self.logger = Logger()
        self.db = sqlite3.connect('shifts.db')
        self.cur = self.db.cursor()
        self.cur.execute('''
            CREATE table IF NOT EXISTS shifts(day TEXT, start TEXT, end TEXT, unit TEXT, grade TEXT); 
        ''')
        self.db.commit()

    #data as tuple(day, date, time, unit, grade)
    def insert_shift(self, data):
        times = get_dates(data[1], data[2])
        to_insert = (data[0], times[0], times[1], data[3], data[4])
        self.cur.execute('''
            INSERT INTO shifts(day, start, end, unit, grade) VALUES (?, ?, ?, ?, ?)
        ''', to_insert)
        self.db.commit()

    #data as tuple(day, date, time, unit, grade)
    def find_shift(self, data):
        self.cur.execute('''
            SELECT * FROM shifts WHERE day = ? AND start = ? AND end = ? AND unit = ? AND grade = ?
        ''', data)
        row = self.cur.fetchone()
        if not row:
            self.logger.log("Shift not in table -- adding shift")
            return False
        else:
            return True

    #data as tuple(day, date, time, unit, grade)
    #return false if shift is in table, true otherwise
    def handel_shift(self, data):
        if not self.find_shift(data):
            self.insert_shift(data)
            return True
        else:
            return False