from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

application = QApplication([])
window = MainWindow()
application.exec()
