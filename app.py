import csv
from typing import List;

events: List[dict] = []

class App:
    with open('EVENT_DATA.csv',newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            