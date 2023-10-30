from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QEvent, QObject
import math

TICK_DIST = 15
DEFAULT_NUM_TICKS = 128

FRAME_RATE = 30

class Timeline(QtWidgets.QScrollArea):
    """
    Custom Qt Widget to show a power bar and dial.
    Demonstrating compound and custom-drawn widget.
    """
    current_time = 0
    tempo = 120

    def __init__(self, parent, performance_area):
        super().__init__(parent=parent)

        self.num_counts = DEFAULT_NUM_TICKS

        self.performance_area = performance_area

        self.layout = QtWidgets.QVBoxLayout()
        self.widget = QtWidgets.QWidget()
        self.setWidget(self.widget)
        self.setMinimumHeight(100)

        self.slider = QtWidgets.QSlider(parent=self, orientation=Qt.Horizontal)
        self.slider.setTickInterval(1)
        self.slider.setMaximum(self.num_counts)
        self.slider.setFixedWidth(TICK_DIST * self.num_counts)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)

        self.slider_filter = ScrollFilter(self.slider)
        self.slider.installEventFilter(self.slider_filter)

        self.timeline_labels = QtWidgets.QWidget(parent=self.widget)
        self.timeline_label_layout = QtWidgets.QHBoxLayout()
        self.timeline_labels.setLayout(self.timeline_label_layout)

        self.timeline_pointer = QtWidgets.QLabel(parent=self.timeline_labels, text='0')
        self.timeline_label_layout.addWidget(self.timeline_pointer)
        self.keyframe_label = QtWidgets.QLabel(parent=self.timeline_labels)
        self.timeline_label_layout.addWidget(self.keyframe_label)

        self.layout.addWidget(self.timeline_labels)
        self.layout.addWidget(self.slider)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.widget.setLayout(self.layout)

        self.slider.valueChanged.connect(self.slider_moved)

    def slider_moved(self):
        self.current_time = (self.get_current_count() / self.tempo) * 60
        self.timeline_pointer.setText(f'Count: {self.slider.value()}\nTime: {self.current_time}')
        self.update_channels()

    def get_current_count(self):
        return self.slider.value()

    def get_current_frame(self):
        return round(self.current_time * FRAME_RATE)
    def get_current_time(self):
        return self.current_time

    def set_current_time(self, t):
        self.current_time = t
        self.slider.setValue(math.floor(self.tempo * (self.current_time / 60)))


    def update_channels(self):
        for performer in self.performance_area.performers:
            performer.position_channel.set_frame(self.get_current_frame())

    def add_keyframe(self):
        new_keyframe_label = QtWidgets.QLabel(parent=self.timeline_labels, text=str(self.slider.value()))
        self.timeline_label_layout.addWidget(new_keyframe_label)
        for performer in self.performance_area.performers:
            performer.set_keyframe()
        self.draw_keyframes()

    def draw_keyframes(self):
        if len(self.performance_area.performers) > 0:
            k_str = self.performance_area.performers[0].position_channel.draw_keyframes()
            self.keyframe_label.setText(k_str)


class ScrollFilter(QObject):

    def __init__(self, parent):
        super().__init__(parent)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Wheel:
            return True
        return super().eventFilter(watched, event)
