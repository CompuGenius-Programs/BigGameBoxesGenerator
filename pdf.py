import os
import subprocess

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

BOXES_SIZE = 10
SPOTS = 100
CELL_SIZE = 55
LABEL_OFFSET = 20
GRID_OFFSET = 20
LABEL_GRID_OFFSET = -20
PAGE_HEIGHT = letter[1]
CENTER_X = letter[0] // 2
TITLE_Y = PAGE_HEIGHT - 25
GRID_Y = TITLE_Y - 715
PDF_PATH = "boxes.pdf"


def draw_grid(c, boxes, teams_scores):
    c.setFont("Times-Roman", 8)

    teams = teams_scores[0] if teams_scores[0] else ["Away", "Home"]

    c.setFont("Times-Roman", 14)
    team1_width = c.stringWidth(teams[0], "Times-Roman", 14)
    team1_x = CENTER_X - team1_width / 2
    c.drawString(CENTER_X - c.stringWidth(teams[0], "Times-Roman", 14) / 2,
                 PAGE_HEIGHT - (GRID_Y + LABEL_OFFSET + GRID_OFFSET + LABEL_GRID_OFFSET - 20), teams[0])
    c.line(team1_x, PAGE_HEIGHT - (GRID_Y + LABEL_OFFSET + GRID_OFFSET + LABEL_GRID_OFFSET - 20) - 2,
           team1_x + team1_width, PAGE_HEIGHT - (GRID_Y + LABEL_OFFSET + GRID_OFFSET + LABEL_GRID_OFFSET - 20) - 2)

    letter_height = 20
    total_height = len(teams[1]) * letter_height
    offset = (BOXES_SIZE * CELL_SIZE - total_height) / 2

    for i, team_name_letter in enumerate(teams[1]):
        c.drawString(10,
                     PAGE_HEIGHT - (GRID_Y + offset + i * letter_height + LABEL_OFFSET + GRID_OFFSET + CELL_SIZE // 2),
                     team_name_letter)

    line_start_y = PAGE_HEIGHT - (GRID_Y + offset + LABEL_OFFSET + GRID_OFFSET + CELL_SIZE // 2) + 10
    line_end_y = line_start_y - total_height + 5
    c.line(22, line_start_y, 22, line_end_y)

    c.setFont("Times-Roman", 8)
    for i in range(BOXES_SIZE):
        c.drawString(30, PAGE_HEIGHT - (GRID_Y + i * CELL_SIZE + LABEL_OFFSET + GRID_OFFSET + CELL_SIZE // 2), str(i))

    for j in range(BOXES_SIZE):
        c.drawString(j * CELL_SIZE + LABEL_OFFSET + GRID_OFFSET + CELL_SIZE // 2,
                     PAGE_HEIGHT - (GRID_Y + LABEL_OFFSET + GRID_OFFSET + LABEL_GRID_OFFSET),
                     str(j))

    scores = teams_scores[1]
    if scores:
        winning_quarters = {}
        for quarter in range(len(scores[0])):
            team1_ones = scores[0][quarter] % 10
            team2_ones = scores[1][quarter] % 10

            winning_box = (team1_ones, team2_ones)
            if winning_box not in winning_quarters:
                winning_quarters[winning_box] = []
            winning_quarters[winning_box].append(quarter)

            c.setFillGray(0.75)
            c.rect(team1_ones * CELL_SIZE + LABEL_OFFSET + GRID_OFFSET,
                   PAGE_HEIGHT - (GRID_Y + team2_ones * CELL_SIZE + LABEL_OFFSET + GRID_OFFSET + CELL_SIZE),
                   CELL_SIZE, CELL_SIZE, fill=1)
            c.setFillGray(0)

        for i in range(BOXES_SIZE):
            for j in range(BOXES_SIZE):
                c.rect(j * CELL_SIZE + LABEL_OFFSET + GRID_OFFSET,
                       PAGE_HEIGHT - (GRID_Y + i * CELL_SIZE + LABEL_OFFSET + GRID_OFFSET + CELL_SIZE),
                       CELL_SIZE, CELL_SIZE)
                if (j, i) in winning_quarters:
                    quarters = ', '.join(
                        map(str, [quarter + 1 for quarter in winning_quarters[(j, i)]]))
                    c.drawString(j * CELL_SIZE + LABEL_OFFSET + GRID_OFFSET + 5,
                                 PAGE_HEIGHT - (GRID_Y + i * CELL_SIZE + CELL_SIZE - 10 + LABEL_OFFSET + GRID_OFFSET),
                                 quarters)

    for i in range(BOXES_SIZE):
        for j in range(BOXES_SIZE):
            c.rect(j * CELL_SIZE + LABEL_OFFSET + GRID_OFFSET,
                   PAGE_HEIGHT - (GRID_Y + i * CELL_SIZE + LABEL_OFFSET + GRID_OFFSET + CELL_SIZE),
                   CELL_SIZE, CELL_SIZE)
            text = boxes[i][j].split()
            for k in range(len(text)):
                c.drawString(j * CELL_SIZE + 10 + LABEL_OFFSET + GRID_OFFSET,
                             PAGE_HEIGHT - (GRID_Y + i * CELL_SIZE + 20 + LABEL_OFFSET + GRID_OFFSET + k * 10),
                             text[k])


def generate_pdf(people, boxes, title, teams_scores):
    c = canvas.Canvas(os.path.join(PDF_PATH), pagesize=letter)
    c.setFont("Times-Roman", 14)
    c.setTitle(title)

    title_width = c.stringWidth(title, "Times-Roman", 14)
    title_x = CENTER_X - title_width / 2
    c.drawString(title_x, TITLE_Y, title)

    draw_grid(c, boxes, teams_scores)

    initial_y_position = 135
    y_position = initial_y_position
    x_position = 10
    column_threshold = 0
    column_width = 205

    c.setFont("Times-Roman", 10)

    names_boxes = {}

    for i in range(BOXES_SIZE):
        for j in range(BOXES_SIZE):
            name = boxes[i][j]
            if name and name not in names_boxes:
                names_boxes[name] = []
            if name:
                names_boxes[name].append((j, i))

    names_boxes = {name: names_boxes[name] for name, _ in people if name in names_boxes}

    for name, box_list in names_boxes.items():
        box_list = sorted(box_list, key=lambda box: (box[0], box[1]))
        box_list_str = ', '.join([f'({x}, {y})' for x, y in box_list])
        c.drawString(x_position, y_position, f'{name}: {box_list_str}')
        y_position -= 15

        if y_position <= column_threshold:
            y_position = initial_y_position
            x_position += column_width

    c.save()

    subprocess.Popen([os.path.join(PDF_PATH)], shell=True)
