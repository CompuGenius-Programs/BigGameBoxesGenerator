import datetime
import json
import random

import roman

from gui import app
from pdf import generate_pdf

BOXES_SIZE = 10
SPOTS = 100

PEOPLE_FILE = "people.json"

boxes = [["" for _ in range(BOXES_SIZE)] for _ in range(BOXES_SIZE)]
available_spots = list(range(SPOTS))


def assign_boxes(people):
    for person in people:
        for _ in range(int(person[1])):
            spot = random.choice(available_spots)
            available_spots.remove(spot)
            x = spot % BOXES_SIZE
            y = spot // BOXES_SIZE
            boxes[x][y] = person[0]


def get_date_and_number():
    now = datetime.datetime.now()
    current_date = get_date(now.year, 2, 1)
    year = now.year - 1966 if now.date() <= current_date else now.year - 1965
    next_date = get_date(now.year if now.date() <= current_date else now.year + 1, 2, 1)
    return next_date, roman.toRoman(year)


def get_date(year, month, day):
    first_date = datetime.date(year, month, day)
    first_day = first_date.weekday()
    day_inc = 13 + (7 if first_day > 13 else 0) - first_day
    return first_date + datetime.timedelta(days=day_inc)


def main():
    try:
        people_json = json.loads(open(PEOPLE_FILE).read())["people"]
        people = [(person["name"], person["amount"]) for person in people_json]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        app.mainloop()
        people = app.people

    assign_boxes(people)

    date, roman_year = get_date_and_number()
    title = f"Big Game {roman_year} Boxes - {date.strftime('%A, %B %d, %Y')}"
    generate_pdf(people, boxes, title)


if __name__ == "__main__":
    main()
