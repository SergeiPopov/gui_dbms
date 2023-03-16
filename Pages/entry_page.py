from PySide6.QtWidgets import *

from Layouts.Layout import Layout


class EntryPage(QGridLayout):
    def __init__(self, parent=None):
        super(EntryPage, self).__init__(parent)

        # Слой для основных функциональных кнопок
        self.functional_layout = Layout(QBoxLayout.Direction.TopToBottom, parent)

        # Основные функциональные кнопки
        self.table_info_main_btn = QPushButton("Работа с таблицами")
        self.crud_rows_main_btn = QPushButton("Работа с записями")
        self.hand_main_btn = QPushButton("Ручное управление")

        self.functional_layout.append(self.table_info_main_btn)
        self.functional_layout.append(self.crud_rows_main_btn)
        self.functional_layout.append(self.hand_main_btn)

        # Отображение функционального слоя на странице
        self.addLayout(self.functional_layout, 0, 0)




#
# import sys
# app = QApplication([])
# w = QWidget()
# main_win = EntryPage()
#
# w.setLayout(main_win)
# w.show()
# sys.exit(app.exec())

