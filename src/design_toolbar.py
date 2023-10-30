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

        add_keyframe_action = QAction('Add Keyframe', self.parent())
        add_keyframe_action.triggered.connect(self.add_keyframe)
        self.addAction(add_keyframe_action)

    def onMyToolBarButtonClick(self, signal):
        print("click", signal)

    def add_performer(self, signal):
        dlg = QInputDialog(self.parent())
        name, ok = dlg.getText(self, "Add Performer", "Name")
        if ok:
            self.parent().add_performer(name)

    def add_keyframe(self, signal):
        self.parent().add_keyframe()