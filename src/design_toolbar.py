from PySide6.QtWidgets import (
    QToolBar,
    QDialog,
    QInputDialog
)

from PySide6.QtGui import QAction

class DesignToolbar(QToolBar):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setWindowTitle("Design Toolbar")

        button_action = QAction("Your button", self.parent())
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        self.addAction(button_action)

        add_perfomer_action = QAction("Add Performer", self.parent())
        add_perfomer_action.triggered.connect(self.add_performer)
        self.addAction(add_perfomer_action)

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    def add_performer(self, s):
        dlg = QInputDialog(self.parent())
        name, ok = dlg.getText(self, "Add Performer", "Name")
        if ok:
            self.parent().add_performer(name)
