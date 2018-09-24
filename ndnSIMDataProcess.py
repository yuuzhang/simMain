# -*- coding: utf8 -*
import sys,time
import os
from PyQt5 import QtWidgets, uic
import matplotlib as mpl
import glob
from fileItem import *
import traceback

''' <程序结构简介>

'''

qtCreatorFile = "ndnSIMDataProcess.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        mpl.rcParams.update({'font.size': 9})
        mpl.rcParams['lines.linewidth'] = 0.5
        mpl.rcParams['figure.dpi'] = 10
        mpl.rcParams['ytick.major.pad'] = 1
        mpl.rcParams['xtick.major.pad'] = 1
        mpl.rcParams['xtick.labelsize']=5
        mpl.rcParams['ytick.labelsize']=5
        # mpl.rcParams['boxplot.boxprops.linewidth']=0.1
        # mpl.rcParams['boxplot.flierprops.linewidth']=0.5
        mpl.rcParams['axes.linewidth'] = 0.3

        self.dict = {}
        self.connectEvents()
        
        #datadir = "/home/chenyx/Dropbox/workspace/python/ndnSIMDataProcess/data"
        datadir=os.environ['HOME']+'/ndnSIM20180908/ns-3/Results'
        self.dirField.setText(datadir)
        self.getFileList(datadir)
        self.filesListBox.setSortingEnabled(True)
        self.tabWidget.setCurrentIndex(0)
        self.dict = {}

    @staticmethod
    def getFileObject(path, fileName):
        if 'rate' in fileName:
            return rateFile(path, fileName)
        elif 'delay' in fileName:
            return delayFile(path, fileName)
        else:
            print "File Name Error\n"
            exit(-3)
    
    # 文件多选处理
    def filesListBoxSelectionChanged(self):
        curSelections=self.filesListBox.selectedItems()
        if len(curSelections)<2:
            return
        else:
            if self.tabWidget.currentIndex() == 0:
                self.tabWidget.setCurrentIndex(1)

        curSelections=sorted(curSelections)
        self.sumFieldTextEdit.setText("")
        self.minFieldTextEdit.setText("")
        if self.fieldsListBox.count() == 0 or self.typesListBox.count() == 0:
            self.sumFieldTextEdit.append("Select field and type first")
            return
        face = self.faceDropDown.currentText() if self.faceCheckBox.isChecked() else ''
        nodeName = "AllNodes"
        field = self.fieldsListBox.currentItem().text()
        typeName = self.typesListBox.currentItem().text()
        for item in curSelections:
            startTime=time.time()
            fileName = item.text()
            if not self.dict.has_key(fileName):
                self.ifile = self.getFileObject(self.dirField.text(), fileName)
                self.dict[fileName] = self.ifile
            else:
                self.ifile = self.dict[fileName]
            try:
                self.ifile.extractData2(face, nodeName, field, typeName)
            except:
                return
            self.sumFieldTextEdit.append(str(self.ifile.getSum()))
            self.minFieldTextEdit.insertPlainText(str(self.ifile.getMin()))
            self.minFieldTextEdit.insertPlainText(str(self.ifile.getMax()))
            self.minFieldTextEdit.append('')
            #print self.filesListBox.currentItem().text()
            self.statusTextEdit.append("文件"+ str(fileName) + " 显示完成！ 耗时：%.2f s" %(time.time()-startTime))


    # 数据文件单选处理
    def filesListBoxValueChanged(self):
        startTime=time.time()
        if self.filesListBox.currentRow() < 0 or self.dirField.text() == '':
            return
        if self.tabWidget.currentIndex() == 1:
            self.tabWidget.setCurrentIndex(0)
        fileName = self.filesListBox.currentItem().text()
        # 陈延祥添加了dict，期望能再次打开时速度快的，但结果用处也不大
        if not self.dict.has_key(fileName):
            self.ifile = self.getFileObject(self.dirField.text(), fileName)
            self.dict[fileName] = self.ifile
        else:
            self.ifile = self.dict[fileName]
            
        self.fieldsListBox.currentRowChanged.disconnect(self.fieldsListBoxValueChanged)
        self.fieldsListBox.clear()
        for field in self.ifile.getFields():
            self.fieldsListBox.addItem(field)
        self.fieldsListBox.currentRowChanged.connect(self.fieldsListBoxValueChanged)

        type = self.ifile.getFileType()
        if 'rate' == type:
            currentfieldsIndex = 5
            currenttypesIndex = 5
            self.minLabel.setText("Min")
            self.faceCheckBox.setEnabled(True)
        elif 'delay' == type:
            currentfieldsIndex = 5
            currenttypesIndex = 0
            self.minLabel.setText("Max")
            self.faceCheckBox.setEnabled(False)
        else:
            currentfieldsIndex = 0
            currenttypesIndex = 0

        self.nodesList = self.ifile.getNodesList()

        self.typesListBox.currentRowChanged.disconnect(self.typesListBoxValueChanged)
        self.typesListBox.clear()
        for typeName in self.ifile.getTypes():
            self.typesListBox.addItem(typeName)
        # 画图可以在typeListBoxValueChanged中触发的DropDown_ValueChanged中执行的
        try:
            self.typesListBox.setCurrentRow(currenttypesIndex)
        except:
            self.typesListBox.setCurrentRow(0)
        self.typesListBox.currentRowChanged.connect(self.typesListBoxValueChanged)

        self.fieldsListBox.currentRowChanged.disconnect(self.fieldsListBoxValueChanged)
        try:
            self.fieldsListBox.setCurrentRow(currentfieldsIndex)
        except:
            self.fieldsListBox.setCurrentRow(0)
        self.fieldsListBox.currentRowChanged.connect(self.fieldsListBoxValueChanged)

        # Update nodesList
        self.DropDown_1.currentIndexChanged.disconnect(self.DropDown_1ValueChanged)        
        self.DropDown_2.currentIndexChanged.disconnect(self.DropDown_2ValueChanged)        
        self.DropDown_3.currentIndexChanged.disconnect(self.DropDown_3ValueChanged)        
        self.DropDown_4.currentIndexChanged.disconnect(self.DropDown_4ValueChanged)        
        self.DropDown_1.clear()
        self.DropDown_2.clear()
        self.DropDown_3.clear()
        self.DropDown_4.clear()
        self.autoNodeCheckBox.setChecked(True)

        self.DropDown_1.addItems(self.nodesList)
        self.DropDown_2.addItems(self.nodesList)
        self.DropDown_3.addItems(self.nodesList)
        self.DropDown_4.addItems(self.nodesList)
        self.DropDown_1.currentIndexChanged.connect(self.DropDown_1ValueChanged)
        self.DropDown_2.currentIndexChanged.connect(self.DropDown_2ValueChanged)
        self.DropDown_3.currentIndexChanged.connect(self.DropDown_3ValueChanged)
        self.DropDown_4.currentIndexChanged.connect(self.DropDown_4ValueChanged)
        
        #self.DropDown_1.setCurrentIndex(0)
        self.DropDown_1ValueChanged()

        # 下面显得多余的调用是为了显示dataSummaryLabel，和DropDown_ValueChanged的调用有点重复，但只有此处可以设置AllNodes
        face = self.faceDropDown.currentText() if self.faceCheckBox.isChecked() else ''
        nodeName = "AllNodes"
        field = self.fieldsListBox.currentItem().text()
        typeName = self.typesListBox.currentItem().text()
        self.extractData2(face, nodeName, field, typeName)
        self.statusTextEdit.append("文件"+ str(fileName) + " 显示完成！ 耗时：%.2f s" %(time.time()-startTime))
        
    def extractData2(self, face, nodeName, field, typeName):
        try:
            LabelText, statusText, figData = self.ifile.extractData2(face, nodeName, field, typeName)
        except:
            return []
        self.dataSummaryLabel.setText(LabelText)
        self.statusTextEdit.setText(statusText)
        return figData

    def getFileList(self, datadir):
        if datadir == '':
            return
        try:
            os.chdir(datadir)
        except:
            return
        
        self.filesListBox.clear()
        for afile in glob.glob('*.txt'):
            self.filesListBox.addItem(afile)
        self.filesListBox.setCurrentRow(0)

    def fieldsListBoxValueChanged(self):
        self.typesListBoxValueChanged()

    def typesListBoxValueChanged(self):
        # currenttypesIndex=self.typesListBox.currentRow()
        # print currenttypesIndex
        face = self.faceDropDown.currentText() if self.faceCheckBox.isChecked() else ''
        field = self.fieldsListBox.currentItem().text()
        typeName = self.typesListBox.currentItem().text()
        self.extractData2(face, 'AllNodes', field, typeName)

        self.dataSummaryLabel.setText('')
        self.DropDown_1ValueChanged()
        self.DropDown_2ValueChanged()
        self.DropDown_3ValueChanged()
        self.DropDown_4ValueChanged()

    def chooseDir(self):
        datadir = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if datadir != '':
            self.dirField.setText(datadir)
            self.getFileList(datadir)

    def reloadFilesList(self):
        datadir = self.dirField.text()
        self.dict.clear()
        self.fieldsListBox.currentRowChanged.disconnect(self.fieldsListBoxValueChanged)
        self.fieldsListBox.clear()
        self.fieldsListBox.currentRowChanged.connect(self.fieldsListBoxValueChanged)
        self.typesListBox.currentRowChanged.disconnect(self.typesListBoxValueChanged)
        self.typesListBox.clear()
        self.typesListBox.currentRowChanged.connect(self.typesListBoxValueChanged)
        if datadir != '':
            self.getFileList(datadir)
    
    #  数据曲线图在DropDown_?ValueChange中画出
    def DropDown_1ValueChanged(self):
        face = self.faceDropDown.currentText() if self.faceCheckBox.isChecked() else ''
        nodeName = self.DropDown_1.currentText()
        field = self.fieldsListBox.currentItem().text()
        typeName = self.typesListBox.currentItem().text()
        if nodeName != '':

            # self.Canvas_1.figure.add_argument(dpi=80)
            # 下面的axisbg控制绘图的背景色
            # ax = self.Canvas_1.figure.add_subplot(111,axisbg=(1,1,1),)
            ax = self.Canvas_1.figure.add_subplot(111, facecolor='w', )
            ax.axis('auto')
            ax.cla()
            #figData = []
            figData = self.extractData2(face, nodeName, field, typeName)

            if figData is not None:
                ax.plot(range(1, len(figData) + 1), figData, color="blue")
                self.Canvas_1.figure.suptitle(self.typesListBox.currentItem().text(), fontsize=5)
            self.Canvas_1.draw()
            self.setNodeNumber(self.DropDown_1.currentIndex())

    def DropDown_2ValueChanged(self):
        face = self.faceDropDown.currentText() if self.faceCheckBox.isChecked() else ''
        nodeName = self.DropDown_2.currentText()
        field = self.fieldsListBox.currentItem().text()
        typeName = self.typesListBox.currentItem().text()
        if nodeName != '':
            ax = self.Canvas_2.figure.add_subplot(111)
            ax.cla()
            figData = self.extractData2(face, nodeName, field, typeName)
            if figData is not None:
                ax.plot(range(1, len(figData) + 1), figData, color="blue")
                # ax.set_title(self.typesListBox.currentItem().text())
                self.Canvas_2.figure.suptitle(self.typesListBox.currentItem().text(), fontsize=5)
            self.Canvas_2.draw()

    def DropDown_3ValueChanged(self):
        face = self.faceDropDown.currentText() if self.faceCheckBox.isChecked() else ''
        nodeName = self.DropDown_3.currentText()
        field = self.fieldsListBox.currentItem().text()
        typeName = self.typesListBox.currentItem().text()
        if nodeName != '':
            ax = self.Canvas_3.figure.add_subplot(111)
            ax.cla()
            figData = self.extractData2(face, nodeName, field, typeName)
            if figData is not None:
                ax.plot(range(1, len(figData) + 1), figData, color="blue")
                # ax.set_title(self.typesListBox.currentItem().text())
                self.Canvas_3.figure.suptitle(self.typesListBox.currentItem().text(), fontsize=5)
            self.Canvas_3.draw()

    def DropDown_4ValueChanged(self):
        face = self.faceDropDown.currentText() if self.faceCheckBox.isChecked() else ''
        nodeName = self.DropDown_4.currentText()
        field = self.fieldsListBox.currentItem().text()
        typeName = self.typesListBox.currentItem().text()
        if nodeName != '':
            ax = self.Canvas_4.figure.add_subplot(111)
            ax.cla()
            figData = self.extractData2(face, nodeName, field, typeName)
            if figData is not None:
                ax.plot(range(1, len(figData) + 1), figData, color="blue")
                # ax.set_title(self.typesListBox.currentItem().text())
                self.Canvas_4.figure.suptitle(self.typesListBox.currentItem().text(), fontsize=5)
            self.Canvas_4.draw()

    def setNodeNumber(self, startNumber):
        if self.autoNodeCheckBox.isChecked():
            if len(self.nodesList) - startNumber - 1 >= 1:
                self.DropDown_2.setCurrentIndex(startNumber + 1)
            if len(self.nodesList) - startNumber - 1 >= 2:
                self.DropDown_3.setCurrentIndex(startNumber + 2)
            if len(self.nodesList) - startNumber - 1 >= 3:
                self.DropDown_4.setCurrentIndex(startNumber + 3)

    def autoNodeCheckBoxChanged(self):
        self.setNodeNumber(0)

    def faceCheckBoxValueChanged(self):
        if self.faceCheckBox.isChecked():
            faceList = self.ifile.getFaceList()
            if len(faceList) > 0:
                self.faceDropDown.addItems(faceList)
        else:
            self.faceDropDown.clear()
            self.typesListBoxValueChanged()
        self.faceDropDownValueChanged()

    def faceDropDownValueChanged(self):
        self.typesListBoxValueChanged()


    def connectEvents(self):
        self.dirButton.clicked.connect(self.chooseDir)
        self.reloadBtn.clicked.connect(self.reloadFilesList)
        self.filesListBox.currentItemChanged.connect(self.filesListBoxValueChanged)
        self.filesListBox.itemSelectionChanged.connect(self.filesListBoxSelectionChanged)
        self.fieldsListBox.currentRowChanged.connect(self.fieldsListBoxValueChanged)
        self.typesListBox.currentRowChanged.connect(self.typesListBoxValueChanged)
        self.faceCheckBox.stateChanged.connect(self.faceCheckBoxValueChanged)
        self.faceDropDown.currentIndexChanged.connect(self.faceDropDownValueChanged)
        self.DropDown_1.currentIndexChanged.connect(self.DropDown_1ValueChanged)
        self.DropDown_2.currentIndexChanged.connect(self.DropDown_2ValueChanged)
        self.DropDown_3.currentIndexChanged.connect(self.DropDown_3ValueChanged)
        self.DropDown_4.currentIndexChanged.connect(self.DropDown_4ValueChanged)
        self.autoNodeCheckBox.stateChanged.connect(self.autoNodeCheckBoxChanged)
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

exit(0)
