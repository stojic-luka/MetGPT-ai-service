import datetime, random

class TellDate():
    def __init__(self):
        self.responses = [
            "Datum danas je",
            "Danas je",
            "Današnji datum je",
        ]
        self.date_string = f'{datetime.date.today():%A, %d. %B %Y.}'

    def run(self):
        return f"{random.choice(self.responses)} {self.date_string}"

def setup():
    return TellDate() 