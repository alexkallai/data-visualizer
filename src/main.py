from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
import sys

def main():
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    main()