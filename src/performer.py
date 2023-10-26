from PySide6.QtWidgets import (QGraphicsItemGroup, QGraphicsSimpleTextItem, QGraphicsItem)
import PySide6
from typing import Optional

class Performer(QGraphicsItemGroup):

    def __init__(self, name="Performer"):
        super().__init__()

        start_coord_x, start_coord_y = 100, 100

        name_item = QGraphicsSimpleTextItem()
        name_item.setText(name)
        name_item.setFont("sans serif")
        name_item.setScale(1)
        name_item.setPos(start_coord_x, start_coord_y)

        name_scene_rect = name_item.mapRectToScene(name_item.boundingRect())

        name_width = name_scene_rect.width()
        name_center = start_coord_x + (name_width / 2)

        x_item = QGraphicsSimpleTextItem()
        x_item.setText("X")
        x_item.setFont("sans serif")
        x_item.setScale(2)
        x_item.setPos(start_coord_x, start_coord_y)

        x_scene_rect = x_item.mapRectToScene(x_item.boundingRect())

        x_width = x_scene_rect.width()
        x_height = x_scene_rect.height()
        x_left = name_center - (x_width / 2)
        x_top = start_coord_y - x_height

        x_item.setPos(x_left, x_top)

        print(name_item.pos())
        print(name_width, name_center)
        print(x_item.pos())
        print(x_width, x_height, x_left, x_top)

        self.addToGroup(name_item)
        self.addToGroup(x_item)

        self.setX(100)
        self.setY(100)

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
