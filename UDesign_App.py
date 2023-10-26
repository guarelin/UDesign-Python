import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QGraphicsView,
    QToolBar
)

from PySide6.QtCore import (
    Qt
)

import performance_area
import design_toolbar

class UDesign(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UDesign")

        layout = QVBoxLayout()

        self.scene = performance_area.PerformanceArea(parent=self)
        view = QGraphicsView(self.scene)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        toolbar = design_toolbar.DesignToolbar(parent=self)
        self.addToolBar(toolbar)

        # view.show()
        # layout.addWidget(view)

        # central_widget = QWidget()
        # central_widget.setLayout(layout)

        self.setCentralWidget(view)

    def add_performer(self, name):
        self.scene.add_performer(name)


app = QApplication(sys.argv)
window = UDesign()
window.show()
app.exec()