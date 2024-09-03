import math
from qtpy import QtCore
from qtpy.QtCore import Signal
from PyQt6.QtGui import QPainter, QFont, QFontMetrics
from qtpy.QtWidgets import QComboBox, QStyleOptionComboBox


class CountryDropdown(QComboBox):

    show_popup = Signal()
    hide_popup = Signal()
    geometry_changed = Signal()

    def __init__(self, parent=None):
        super(CountryDropdown, self).__init__(parent)

        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.__style_option = QStyleOptionComboBox()
        self.initStyleOption(self.__style_option)
        self.__style_option.currentText = ''

        self.__input_font = self.font()
        self.__font_metrics_input = QFontMetrics(self.font())
        self.__icon_size = 0
        self.popup_open = False
        self.__current_country_code = ''

        self.__calculate_geometry()
        self.__calculate_country_code()

        self.currentTextChanged.connect(self.__calculate_country_code)
        self.currentTextChanged.connect(self.__calculate_geometry)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.__input_font)

        if self.count() > 0:
            x_start = (self.height() - self.__icon_size) // 2 + self.__border_width - 1
            buffer_left = (self.height() - self.__icon_size) // 2
            painter.drawPixmap(x_start, buffer_left, self.itemIcon(
                self.currentIndex()).pixmap(self.__icon_size, self.__icon_size))
            painter.drawText(x_start + self.__icon_size + buffer_left // 2,
                             self.height() - math.ceil((self.height() - self.__font_metrics_input.tightBoundingRect(
                                 self.__current_country_code).height()) / 2),
                             self.__current_country_code)

    def showPopup(self):
        super().showPopup()
        self.show_popup.emit()
        self.popup_open = True
        
    def hidePopup(self):
        super().hidePopup()
        self.hide_popup.emit()
        self.popup_open = False

    def resizeEvent(self, event):
        self.__calculate_geometry()

    def setBorderWidth(self, width: int):
        self.__border_width = width
        self.__calculate_geometry()
        self.update()

    def setInputFont(self, font: QFont):
        self.__input_font = font
        self.__calculate_geometry()
        self.update()

    def __calculate_geometry(self):
        self.__font_metrics_input = QFontMetrics(self.__input_font)
        self.__icon_size = int(self.height() * 0.7)
        buffer_left = (self.height() - self.__icon_size) // 2
        self.setFixedWidth(self.height() + self.__font_metrics_input.tightBoundingRect(self.__current_country_code).width() + buffer_left // 2)
        self.geometry_changed.emit()
        self.update()

    def __calculate_country_code(self):
        if self.count() > 0:
            self.__current_country_code = self.currentText().split('(')[1].split(')')[0]
            print(self.__current_country_code)
