import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QGraphicsView,
    QToolBar,
    QWidget
)

from PySide6.QtCore import (
    Qt
)

import performance_area
import design_toolbar
import timeline

class UDesign(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UDesign")

        layout = QVBoxLayout()

        self.scene = performance_area.PerformanceArea(parent=self)
        self.view = QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        toolbar = design_toolbar.DesignToolbar(parent=self)
        self.addToolBar(toolbar)

        self.timeline = timeline.Timeline(parent=self)

        # view.show()
        layout.addWidget(self.view)
        layout.addWidget(self.timeline)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def add_performer(self, name):
        self.scene.add_performer(name)


app = QApplication(sys.argv)
window = UDesign()
window.show()
app.exec()