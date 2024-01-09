from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QEvent, QObject
import math

TICK_DIST = 15
DEFAULT_NUM_TICKS = 128

FRAME_RATE = 30
KEYFRAME_CIRCLE_HT = 15


class Timeline(QtWidgets.QScrollArea):
    """
    Custom Qt Widget to show a power bar and dial.
    Demonstrating compound and custom-drawn widget.
    """
    current_time = 0
    tempo = 120

    keyframe_counts = []

    def __init__(self, parent, performance_area):
        super().__init__(parent=parent)

        self.num_counts = DEFAULT_NUM_TICKS

        # Initialize main Timeline Widget components
        self.performance_area = performance_area
        self.layout = QtWidgets.QVBoxLayout()
        self.widget = QtWidgets.QWidget()
        self.setWidget(self.widget)
        self.setMinimumHeight(200)

        # Initialize the slider
        self.slider = QtWidgets.QSlider(parent=self, orientation=Qt.Horizontal)
        self.slider.setTickInterval(1)
        self.slider.setMaximum(self.num_counts)
        self.slider.setFixedWidth(TICK_DIST * self.num_counts)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider_filter = ScrollFilter(self.slider)
        self.slider.installEventFilter(self.slider_filter)

        # Timeline pointer label to show what count you're on
        self.timeline_labels = QtWidgets.QWidget(parent=self.widget)
        self.timeline_label_layout = QtWidgets.QHBoxLayout()
        self.timeline_labels.setLayout(self.timeline_label_layout)
        self.timeline_pointer = QtWidgets.QLabel(parent=self.timeline_labels, text='0')
        self.timeline_label_layout.addWidget(self.timeline_pointer)
        self.keyframe_label = QtWidgets.QLabel(parent=self.timeline_labels)
        self.timeline_label_layout.addWidget(self.keyframe_label)

        # Keyframe label container
        self.keyframe_label_widget = QtWidgets.QLabel(parent=self.widget)
        self.keyframe_label_layout = QtWidgets.QGridLayout()
        self.keyframe_label_widget.setLayout(self.keyframe_label_layout)
        self.draw_empty_keyframe_labels()
        # self.keyframe_labels = QtGui.QImage(self.slider.width(), KEYFRAME_CIRCLE_HT, QtGui.QImage.Format_ARGB32)
        # self.keyframe_label_widget.setPixmap(QtGui.QPixmap(self.keyframe_labels))

        # Add widgets to layout and layout to main Timeline widget
        self.layout.addWidget(self.timeline_labels)
        self.layout.addWidget(self.keyframe_label_widget)
        self.layout.addWidget(self.slider)
        self.widget.setLayout(self.layout)

        print(self.keyframe_label_widget.pos(), self.keyframe_label_widget.size())

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

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

        self.keyframe_counts.append(self.get_current_count())
        self.keyframe_counts = sorted(self.keyframe_counts)
        self.draw_keyframes()

    def draw_new_keyframe(self):
        # Init the painter
        p = QtGui.QPainter(self.keyframe_labels)
        p.setBrush(Qt.red)
        p.setPen(QtGui.QPen(Qt.white, 2.0))

        # Paint the images in the PROPER order: 1, 2, 3, etc
        slider_left, slider_top = self.slider.x(), self.slider.y()
        current_count_x = int(slider_left + (self.slider.value() * TICK_DIST) - (KEYFRAME_CIRCLE_HT / 2))
        current_count_y = int(slider_top - KEYFRAME_CIRCLE_HT)

        print(self.get_current_count(), current_count_x)

        p.drawEllipse(QtCore.QPoint(current_count_x, current_count_y), KEYFRAME_CIRCLE_HT, KEYFRAME_CIRCLE_HT)

        p.end()

    def draw_empty_keyframe_labels(self):
        for i in range(self.num_counts):
            new_label = QtWidgets.QLabel(parent=self.keyframe_label_widget, text=f'')
            new_label.setFixedSize(TICK_DIST, 15)
            self.keyframe_label_layout.addWidget(new_label, 0, i)

    def draw_keyframes(self):
        for i, count in enumerate(self.keyframe_counts):
            self.keyframe_label_layout.itemAtPosition(0, count).widget().setText(f'{i+1}')


class ScrollFilter(QObject):

    def __init__(self, parent):
        super().__init__(parent)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Wheel:
            return True
        return super().eventFilter(watched, event)

