import sys
from PySide6.QtWidgets import QApplication, QWidget, QSlider, QLabel
from PySide6.QtCore import Qt


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        #change1: change w(third argument) from 100 to 120
        self.slider.setGeometry(30, 40, 118, 30)
        self.slider.valueChanged[int].connect(self.changeValue)
        self.label = QLabel(self)
        self.label.setText("50")
        self.label.setGeometry(140, 40, 30, 30)
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QSlider')
        self.show()
        #change2: Set the initial position of the label above the slider
        self.label.move(self.slider.x() + 50, self.slider.y() - 30)

    def changeValue(self, value):
        self.label.setText(str(value))
        #change3: move label position up(20 to 30)
        self.label.move(self.slider.x() + value, self.slider.y() - 30)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    sys.exit(app.exec())