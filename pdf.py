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
GRID_Y = TITLE_Y - 735
PDF_PATH = "boxes.pdf"


def draw_grid(c, boxes):
    c.setFont("Times-Roman", 8)
    for i in range(BOXES_SIZE):
        c.drawString(10, PAGE_HEIGHT - (GRID_Y + i * CELL_SIZE + LABEL_OFFSET + GRID_OFFSET + CELL_SIZE // 2), str(i))

    for j in range(BOXES_SIZE):
        c.drawString(j * CELL_SIZE + LABEL_OFFSET + GRID_OFFSET + CELL_SIZE // 2,
                     PAGE_HEIGHT - (GRID_Y + LABEL_OFFSET + GRID_OFFSET + LABEL_GRID_OFFSET),
                     str(j))

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


def generate_pdf(people, boxes, title):
    c = canvas.Canvas(os.path.join(PDF_PATH), pagesize=letter)
    c.setFont("Times-Roman", 14)
    c.setTitle(title)

    title_width = c.stringWidth(title, "Times-Roman", 14)
    title_x = CENTER_X - title_width / 2
    c.drawString(title_x, TITLE_Y, title)

    draw_grid(c, boxes)

    initial_y_position = 145
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
