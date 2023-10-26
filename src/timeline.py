from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt


class Timeline(QtWidgets.QWidget):
    """
    Custom Qt Widget to show a power bar and dial.
    Demonstrating compound and custom-drawn widget.
    """

    def __init__(self, steps=5, *args, **kwargs):
        super().__init__()

        layout = QtWidgets.QVBoxLayout()

        self.slider = QtWidgets.QSlider(parent=self, orientation=Qt.Horizontal)
        self.slider.setTickInterval(1)
        self.slider.setMaximum(10)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        layout.addWidget(self.slider)

        self.setLayout(layout)
