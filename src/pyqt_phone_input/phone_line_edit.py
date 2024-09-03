from qtpy.QtCore import Signal, QRegularExpression
from qtpy.QtGui import QPainter, QColor, QRegularExpressionValidator
from qtpy.QtWidgets import QLineEdit
from .country_dropdown import CountryDropdown


class PhoneLineEdit(QLineEdit):

    focus_in = Signal()
    focus_out = Signal()

    def __init__(self, parent=None):
        super(PhoneLineEdit, self).__init__(parent)

        self.__country_dropdown = None

        self.setValidator(QRegularExpressionValidator(QRegularExpression('[0-9 ]*')))

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.__country_dropdown:
            painter = QPainter(self)
            painter.setPen(self.__border_color_current)
            x = self.__country_dropdown.width() + self.__border_width * 2

            for i in range(self.__border_width):
                painter.drawLine(x + i, 0, x + i, self.height() - 1)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focus_in.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.focus_out.emit()

    def getCountryDropdown(self) -> CountryDropdown:
        return self.__country_dropdown

    def setCountryDropdown(self, country_dropdown: CountryDropdown):
        self.__country_dropdown = country_dropdown

    def getCurrentBorderColor(self) -> QColor:
        return self.__border_color_current

    def setCurrentBorderColor(self, color: QColor):
        self.__border_color_current = color
        self.update()

    def getBorderWidth(self) -> int:
        return self.__border_width

    def setBorderWidth(self, width: int):
        self.__border_width = width
        self.update()
