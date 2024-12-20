import sys
from PyQt5.QtWidgets import QApplication
from ui import WhiteBackgroundRemoverApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WhiteBackgroundRemoverApp()
    window.show()
    sys.exit(app.exec_())