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

        self.timeline = timeline.Timeline(parent=self, performance_area=self.scene)
        self.scene.set_timeline(self.timeline)

        # view.show()
        layout.addWidget(self.view)
        layout.addWidget(self.timeline)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def update_performer_positions(self, count):
        self.scene.update_performer_positions(count)

    def add_performer(self, name):
        self.scene.add_performer(name)

    def add_keyframe(self):
        self.timeline.add_keyframe()

app = QApplication(sys.argv)
window = UDesign()
window.show()
app.exec()