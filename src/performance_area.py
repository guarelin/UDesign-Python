from typing import Union
import PySide6
from PySide6.QtWidgets import (QGraphicsScene, QGraphicsPixmapItem)
from PySide6.QtCore import (QRectF, QLineF, Qt)
from PySide6.QtGui import (QPixmap, QImage, QPainter, QBrush, QPen, QColor, QScreen)

DEFAULT_BG = 'images/Background.png'

import performer

class PerformanceArea(QGraphicsScene):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background_img = QImage(DEFAULT_BG)

        self.feet_width = 70
        self.feet_height = 50
        self.feet_grid = 8

        # w = self.background_img.size().width()
        # h = self.background_img.size().height()

        # w = QScreen().size().width() * 0.5
        w = 750
        h = (w / self.feet_width) * self.feet_height
        print(w, h)
        self.setSceneRect(0, 0, w, h)

    def drawBackground(self, painter: PySide6.QtGui.QPainter, rect: Union[PySide6.QtCore.QRectF, PySide6.QtCore.QRect]) -> None:
        self.draw_minor_grid(painter)
        self.draw_major_grid(painter)
        self.draw_border(painter)

        # painter.drawImage(rect, self.background_img)

    def draw_major_grid(self, painter):
        w, h = self.sceneRect().width(), self.sceneRect().height()
        left, top = self.sceneRect().x(), self.sceneRect().y()

        center = left + (w/2)
        middle = top + (h/2)

        px_per_ft = min(w // self.feet_width, h // self.feet_height)

        floor_left, floor_right = center - (px_per_ft * (self.feet_width // 2)), center + (px_per_ft * (self.feet_width // 2))
        floor_top, floor_bottom = middle - (px_per_ft * (self.feet_height // 2)), middle + (px_per_ft * (self.feet_height // 2))

        count_vlines = self.feet_width / self.feet_grid
        count_hlines = self.feet_height / self.feet_grid

        vline_dist = self.feet_grid * px_per_ft
        hline_dist = self.feet_grid * px_per_ft

        major_grid_pen = QPen(QColor('black'))
        major_grid_pen.setWidth(3)
        painter.setPen(major_grid_pen)

        vlines = [QLineF(center, floor_bottom, center, floor_top)]
        for i in range(int(count_vlines // 2)):
            offset = i * vline_dist
            vlines.append(QLineF(center + offset, floor_bottom, center + offset, floor_top))
            vlines.append(QLineF(center - offset, floor_bottom, center - offset, floor_top))

        painter.drawLines(vlines)

        hlines = [QLineF(floor_left, middle, floor_right, middle)]
        for i in range(int(count_hlines // 2)):
            offset = i * hline_dist
            hlines.append(QLineF(floor_left, middle + offset, floor_right, middle + offset))
            hlines.append(QLineF(floor_left, middle - offset, floor_right, middle - offset))

        painter.drawLines(hlines)

    def draw_minor_grid(self, painter):
        w, h = self.sceneRect().width(), self.sceneRect().height()
        left, top = self.sceneRect().x(), self.sceneRect().y()

        center = left + (w/2)
        middle = top + (h/2)

        px_per_ft = min(w // self.feet_width, h // self.feet_height)

        floor_left, floor_right = center - (px_per_ft * (self.feet_width // 2)), center + (px_per_ft * (self.feet_width // 2))
        floor_top, floor_bottom = middle - (px_per_ft * (self.feet_height // 2)), middle + (px_per_ft * (self.feet_height // 2))

        vline_dist = (self.feet_grid / 4) * px_per_ft
        hline_dist = (self.feet_grid / 4) * px_per_ft

        minor_grid_pen = QPen(QColor('gray'))
        minor_grid_pen.setWidth(1)
        painter.setPen(minor_grid_pen)

        vlines = []
        current_x = center
        while current_x < floor_right:
            vlines.append(QLineF(current_x, floor_bottom, current_x, floor_top))
            current_x += vline_dist

        current_x = center
        while current_x > floor_left:
            vlines.append(QLineF(current_x, floor_bottom, current_x, floor_top))
            current_x -= vline_dist

        painter.drawLines(vlines)

        hlines = []
        current_y = middle
        while current_y < floor_bottom:
            hlines.append(QLineF(floor_left, current_y, floor_right, current_y))
            current_y += hline_dist

        current_y = middle
        while current_y > floor_top:
            hlines.append(QLineF(floor_left, current_y, floor_right, current_y))
            current_y -= hline_dist

        painter.drawLines(hlines)


    def draw_border(self, painter):
        w, h = self.sceneRect().width(), self.sceneRect().height()
        left, top = self.sceneRect().x(), self.sceneRect().y()

        center = left + (w/2)
        middle = top + (h/2)

        px_per_ft = min(w // self.feet_width, h // self.feet_height)

        floor_left, floor_right = center - (px_per_ft * (self.feet_width // 2)), center + (px_per_ft * (self.feet_width // 2))
        floor_top, floor_bottom = middle - (px_per_ft * (self.feet_height // 2)), middle + (px_per_ft * (self.feet_height // 2))

        borderlines = [
            QLineF(floor_left, floor_bottom, floor_left, floor_top),  # left border
            QLineF(floor_right, floor_bottom, floor_right, floor_top),  # right border
            QLineF(floor_left, floor_top, floor_right, floor_top),  # top border
            QLineF(floor_left, floor_bottom, floor_right, floor_bottom),  # bottom border
        ]

        border_pen = QPen(QColor('black'))
        border_pen.setWidth(10)
        painter.setPen(border_pen)
        painter.drawLines(borderlines)

    def add_performer(self, name):
        self.addItem(performer.Performer(name=name))