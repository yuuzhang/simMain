# -*- coding: utf8 -*
import sys,os,time,string,signal
from PyQt5 import  QtWidgets, QtCore,uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QFileInfo, QObject,pyqtSignal
import subprocess
from multiprocessing import Pool,Process,Pipe
from posix import strerror, pipe
from fileinput import filename
import psutil

qtCreatorFile = "mainwindow.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class proInfo(QObject):
    progressUpdated=pyqtSignal(int)
    def createProcess(self):
        pool=Pool()
        for i in range(4):
            #res=pool.apply_async(runJob,args=(format(i)),callback=self.refreshCPU(format(i)))
            res=pool.apply_async(self.run,args=(format(i)))            
        pool.close()

    def emitSignal(self):
        print "aProcess class run"
        self.progressUpdated.emit(555)

    def run(self,resStr):
        #time.sleep(1)
        print "aProcess run"
        #proinfo.eimitSignal()

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    res=""           
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        #2017-10-10 ZhangYu Events
        self.pBtn_Run.clicked.connect(self.pBtn_RunClicked)

    def pBtn_RunClicked(self):
        proinfo=proInfo()
        proinfo.progressUpdated.connect(self.refreshCPU)
        proinfo.createProcess()
    
    def refreshCPU(self,result):
        self.QtxtBroOutput.append(format(result))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())        
