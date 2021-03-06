# -*- coding: utf8 -*
'''
Created on 2017年10月11日
Different from the simMain_Converted.py, using loadUiType to read ui file directely, to avoid the boring process of convert ui to py
放弃了袁炜佳论文中使用的多线程，而使用多进程，Python中只有多进程才能充分利用多核CPU
@author: zhangyu
'''
import sys,os,time,string
from PyQt5 import  QtWidgets, QtCore,uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QFileInfo
import subprocess
from multiprocessing import Pool
from posix import strerror
from fileinput import filename
import psutil

qtCreatorFile = "mainwindow.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

def runJob(shellCmd,directory):
    startTime=time.time()
    my_env = os.environ.copy()
    # ZhangYu 必须设置环境变量保证使用正确的python版本，才能使得./waf正确执行，否则导致在eclipse中运行出错，而在bash中执行用命令行python simMain.py就OK的现象
    my_env["PATH"] = "/opt/local/bin:/opt/local:/usr/bin:" + my_env["PATH"]
    try:
        proc = subprocess.Popen(shellCmd, shell = True, cwd = directory, env=my_env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    except OSError:
        print("subprocess.Popen 出错了")
        print(OSError(strerror,filename))   #只找到了这些输出
    try:
        #proc.wait()    #似乎不需要也是阻塞方式的
        stdoutResults, stderrResults = proc.communicate()
    except:
        proc.kill()
    retval=proc.returncode
    retstr=""
    if(retval==0):
        elapsedTime=time.time()-startTime
        retstr+= stdoutResults
        retstr+=shellCmd+" 完成  ----总共耗费时间： %f  秒" % elapsedTime
    else:
        retstr+= stderrResults
    #print retstr
    return retstr

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    sig=QtCore.pyqtSignal('QString')
    exepath=os.environ['HOME']+"/ndnSIM20170130/ns-3/"

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.lnEdit_Prog.setText(self.exepath+"src/ndnSIM/examples/ndn-zhangyu-scip-routing.py")
        self.lnEdit_loadStart.setText('50')
        self.lnEdit_loadEnd.setText('52')
        self.lnEdit_loadStep.setText('2')
        self.cmBox_RoutingName.addItems(["Flooding","BestRoute","k-shortest-2","k-shortest-3","MultiPathPairFirst","SCIP"])
        self.cmBox_RoutingName.setCurrentIndex(2)
        self.cmBox_SimulationSpan.addItems(["15000","100","150","200","300","500","1000","2000","3000","5000"])
    
        self.spinBox_processes.setRange(2,16)
        self.spinBox_processes.setSingleStep(2)
        self.spinBox_processes.setValue(6)
        
        #2017-10-10 ZhangYu Events
        self.pBtn_Run.clicked.connect(self.pBtn_RunClicked)
        self.pBtn_file.clicked.connect(self.pBtn_fileClicked)
        self.refreshGUI("")
        self.sig.connect(self.refreshGUI)


    def pBtn_fileClicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName,_ = QFileDialog.getOpenFileName(None, '', self.exepath+'src/ndnSIM/examples/', 'All Files (*);;Python Files (*.py);;cpp Files （*.cpp)', '', options)
        if fileName:
            self.lnEdit_Prog.setText(fileName)
    def pBtn_RunClicked(self):
        fi=QFileInfo(self.lnEdit_Prog.text())
        #runName=fi.baseName()
        ns3path=os.path.dirname(fi.dir().path())
        ns3path=os.path.dirname(ns3path)
        self.exepath=os.path.dirname(ns3path)
        routingName=self.cmBox_RoutingName.currentText()
        simSpan=self.cmBox_SimulationSpan.currentText()
        pool = Pool(processes=self.spinBox_processes.value())
        cmds={}
        for traffic in range(string.atoi(self.lnEdit_loadStart.text()),string.atoi(self.lnEdit_loadEnd.text()),
                             string.atoi(self.lnEdit_loadStep.text())):
            if fi.suffix()=="cpp":
                cmds[traffic]="./waf --run='{1} --routingName={3} --simulationSpan={2} --InterestsPerSec={0}'".format(traffic,fi.baseName(),simSpan,routingName)
            else:
                cmds[traffic]="./waf --pyrun='{1} --routingName={3} --simulationSpan={2} --InterestsPerSec={0}'".format(traffic,'src/ndnSIM/examples/'+fi.fileName(),simSpan,routingName)
            res=pool.apply_async(runJob,args=(cmds[traffic],self.exepath),callback=self.invokeRefresh)
            self.listWidget_activeProg.addItem(cmds[traffic])
            #res.wait()
            #print(res.get())       
        pool.close()    #关闭线程池，不再接收新任务

        #proc=Process(target=ajob.runJob, args=("./waf --run='ndn-zhangyu-multipath --simulationSpan=50 --InterestsPerSec=50'", os.environ['HOME']+"/ndnSIM20170130/ns-3/"))
        #proc.start()
        #proc.join()
        self.refreshGUI("")
    
    '''
    2017-10-15，pool.apply_async调用的函数必须是外部的全局函数，无论是self.runJob或者是其他 anyclass.runJob都不能执行，而给全局函数runJob传递窗体或控件都会出错，导致无法在子进程内建立信号和窗体控件的链接
    使用callback是退而求其次的方法，因为并没有能力在子进程内更新GUI，子进程结束后才更新GUI，但即使这样也报错，网上查原因是“it appears you're trying to access QtGui classes from a thread other than the main thread”
    不过这里使用signal就容易多了
    '''    
    def invokeRefresh(self,result):
        self.sig.emit(result)
        
    def refreshGUI(self,result):
        cpuload=psutil.cpu_percent()
        self.label_10.setText(format(cpuload)+"%")
        self.label_10.setFont(QFont( "Times" , 36 , QFont.Bold) )
        self.label_10.setStyleSheet("color:#50a2e2") #文本颜色
        #self.label_10.setStyleSheet("background-color:red");//背景色
        self.QtxtBroOutput.append(format(result))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())        
