import cpuUsageGui
import sys
import sysInfo
from PyQt5 import QtCore

"""Main window setup"""
app = cpuUsageGui.QtWidgets.QApplication(sys.argv)
Form = cpuUsageGui.QtWidgets.QWidget()
ui = cpuUsageGui.Ui_Form()
ui.setupUi(Form)

def updateProgBar(val):
    ui.progressBar.setValue(val)

class ThreadClass(QtCore.QThread):
    def run(self):
        while True:
            val = sysInfo.getCpu()
            self.emit(QtCore.pyqtSignal('CPUVALUE'), val)

threadclass = ThreadClass()

# This section does not work
connect(threadclass, QtCore.pyqtSignal('CPUVALUE'), updateProgBar)
# This section does not work

if __name__ == "__main__":
    threadclass.start()
    Form.show()
    sys.exit(app.exec_())
