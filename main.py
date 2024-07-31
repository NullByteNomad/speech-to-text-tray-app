import sys
from PyQt5 import QtWidgets
from tray_app import TrayApp

def main():
    app = QtWidgets.QApplication(sys.argv)
    tray = TrayApp()
    tray.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()