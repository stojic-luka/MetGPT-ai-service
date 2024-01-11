import datetime, random

class TellTime():
    def __init__(self):
        self.responses = [
            "Trenutno vreme je",
            "Trenutno je",
            "Vreme je",
            "Sada je",
        ]
        self.time_string = f'{datetime.datetime.now():%H:%M:%S}'

    def run(self):
        return f"{random.choice(self.responses)} {self.time_string}"

def setup():
    return TellTime() 