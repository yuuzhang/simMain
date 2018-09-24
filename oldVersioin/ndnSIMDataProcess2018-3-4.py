#!/usr/bin/env python
# -*- coding: utf8 -*
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import matplotlib as mpl
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
#教程：https://liam0205.me/2014/09/11/matplotlib-tutorial-zh-cn/
# http://python.jobbole.com/85106/
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import numpy as np
import glob
import warnings
from warnings import catch_warnings
from xml.dom.minicompat import NodeList

qtCreatorFile = "ndnSIMDataProcess.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

warnings.filterwarnings("ignore")


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    global data
    data = None
    isRateTrace = None
    typeIndex = None
    fields = None
    global nodesList
    nodesList = []
    global currentfieldsIndex,currenttypesIndex
    currentfieldsIndex=5
    currenttypesIndex=5
    global minFieldsValue
    minFieldsValue=[]

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        ## 2018-2-24 为了控制图形的title和tick fontsize，找到的方法
        # qt designer中设置的部件可以提升为canvas，如本代码。这里的canvas受到matplotlib的设置控制
        # 具体可用参数参考：https://matplotlib.org/users/customizing.html
        #matplotlib.rc('xtick', labelsize=5) 
        #matplotlib.rc('ytick', labelsize=5) 
        mpl.rcParams.update({'font.size': 9})
        mpl.rcParams['lines.linewidth'] = 0.5
        mpl.rcParams['figure.dpi']=100
        mpl.rcParams['ytick.major.pad']=1
        mpl.rcParams['xtick.major.pad']=1
        #mpl.rcParams['boxplot.boxprops.linewidth']=0.1
        #mpl.rcParams['boxplot.flierprops.linewidth']=0.5
        mpl.rcParams['axes.linewidth']=0.3
        
        self.dirButton.clicked.connect(self.chooseDir)
        self.filesListBox.doubleClicked.connect(self.filesListBoxdoubleClicked)
        self.filesListBox.currentItemChanged.connect(self.filesListBoxValueChanged)
        self.fieldsListBox.currentRowChanged.connect(self.fieldsListBoxValueChanged)
        self.typesListBox.currentRowChanged.connect(self.typesListBoxValueChanged)
        self.faceCheckBox.stateChanged.connect(self.faceCheckBoxValueChanged)
        self.faceDropDown.currentIndexChanged.connect(self.faceDropDownValueChanged)
        self.DropDown_1.currentIndexChanged.connect(self.DropDown_1ValueChanged)
        self.DropDown_2.currentIndexChanged.connect(self.DropDown_2ValueChanged)
        self.DropDown_3.currentIndexChanged.connect(self.DropDown_3ValueChanged)
        self.DropDown_4.currentIndexChanged.connect(self.DropDown_4ValueChanged)
        self.autoNodeCheckBox.stateChanged.connect(self.autoNodeCheckBoxChanged)
        

        self.getFileList('./')
        self.filesListBox.setSortingEnabled(True)


    def chooseDir(self):
        datadir = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if(datadir != ''):
            self.dirField.setText(datadir)
            self.getFileList(datadir)

    def getFileList(self, datadir):
        os.chdir(datadir)
        self.filesListBox.clear()
        for afile in glob.glob('*.txt'):
            self.filesListBox.addItem(afile)
        self.filesListBox.setCurrentRow(0)

                    
    def filesListBoxValueChanged(self):
        global data
        global isRateTrace
        global typeIndex
        global fields
        global nodesList
        try:
            fileName = self.filesListBox.currentItem().text()
        except:
            return
            
        fid = open(self.dirField.text()+'/'+fileName, 'r')
        # Get fields
        headline = fid.readline()
        fields = headline.split('\t')
        del fields[-1]  # Remove "\n"
        self.fieldsListBox.currentRowChanged.disconnect(self.fieldsListBoxValueChanged)
        self.fieldsListBox.clear()
        self.fieldsListBox.currentRowChanged.connect(self.fieldsListBoxValueChanged)
        for field in fields:
            self.fieldsListBox.addItem(field)

        isRateTrace = False
        if 'rate' in fileName:
            isRateTrace = True
            data = np.loadtxt(fid, delimiter='\t', unpack=True, dtype='f,S50,f,S50,S50,f,f,f,f,')
        elif 'drop' in fileName:
            data = np.loadtxt(fid, delimiter='\t', unpack=True, dtype='f,S50,S50,S50,f,f,f,f')
        elif 'cs' in fileName:
            data = np.loadtxt(fid, delimiter='\t', unpack=True, dtype='f,S50,S50,f')
        else:
            self.fieldsListBox.setEnabled(False)
            self.typesListBox.setEnabled(False)
            return
        self.fieldsListBox.setEnabled(True)
        self.typesListBox.setEnabled(True)

        # Get the index of 'Type'
        typeIndex = np.in1d(fields, 'Type').tolist().index(True)
        self.typesListBox.currentRowChanged.disconnect(self.typesListBoxValueChanged)
        self.typesListBox.clear()
        self.typesListBox.currentRowChanged.connect(self.typesListBoxValueChanged)
        for typeName in np.unique(data[typeIndex]):
            self.typesListBox.addItem(typeName)

        self.faceCheckBox.setEnabled(isRateTrace)

        self.fieldsListBox.currentRowChanged.disconnect(self.fieldsListBoxValueChanged)
        try:
            self.fieldsListBox.setCurrentRow(currentfieldsIndex)
        except:
            self.fieldsListBox.setCurrentRow(0)
        self.fieldsListBox.currentRowChanged.connect(self.fieldsListBoxValueChanged)
        try:
            self.typesListBox.setCurrentRow(currenttypesIndex)
        except:
            self.typesListBox.setCurrentRow(0)
        
        # Update nodesList 
        self.DropDown_1.clear()
        self.DropDown_2.clear()
        self.DropDown_3.clear()
        self.DropDown_4.clear()
        nodesList = np.unique(data[1])
        self.DropDown_1.addItems(nodesList)
        self.DropDown_2.addItems(nodesList)
        self.DropDown_3.addItems(nodesList)
        self.DropDown_4.addItems(nodesList)
        
        self.averageTextEdit.setText('')
        self.DropDown_1ValueChanged()
        self.setNodeNumber(0)
        
        # use the following to guarrentee update the minValue, must after all the
        self.getMinFieldsValue()
        self.extractData('AllNodes')
    
    def fieldsListBoxValueChanged(self):
        self.typesListBoxValueChanged()
        #currentfieldsIndex=self.fieldsListBox.currentRow()
        #print currentfieldsIndex

    def typesListBoxValueChanged(self):
        #currenttypesIndex=self.typesListBox.currentRow()
        #print currenttypesIndex
        
        self.averageTextEdit.setText('')
        self.DropDown_1ValueChanged()
        self.DropDown_2ValueChanged()
        self.DropDown_3ValueChanged()
        self.DropDown_4ValueChanged()
        
        #self.getMinFieldsValue()
        self.extractData('AllNodes')
        
    def DropDown_1ValueChanged(self):
        value = self.DropDown_1.currentText()
        if(value != ''):
            
            #self.Canvas_1.figure.add_argument(dpi=80)
            # 下面的axisbg控制绘图的背景色
            ax = self.Canvas_1.figure.add_subplot(111,axisbg=(1,1,1),)
            ax.axis('auto')
            ax.cla()
            figData = self.extractData(value)
            if figData != None:
                ax.plot(range(1,len(figData)+1), figData, color="blue")
                self.Canvas_1.figure.suptitle(self.typesListBox.currentItem().text(), fontsize=5)
                self.Canvas_1.draw()
                
            self.setNodeNumber(self.DropDown_1.currentIndex())

    def DropDown_2ValueChanged(self):
        value = self.DropDown_2.currentText()
        if (value != ''):
            ax = self.Canvas_2.figure.add_subplot(111)
            ax.cla()
            figData = self.extractData(value)
            if figData != None:
                ax.plot(range(1, len(figData) + 1), figData, color="blue")
                #ax.set_title(self.typesListBox.currentItem().text())
                self.Canvas_2.figure.suptitle(self.typesListBox.currentItem().text(), fontsize=5)
                self.Canvas_2.draw()

    def DropDown_3ValueChanged(self):
        value = self.DropDown_3.currentText()
        if (value != ''):
            ax = self.Canvas_3.figure.add_subplot(111)
            ax.cla()
            figData = self.extractData(value)
            if figData != None:
                ax.plot(range(1, len(figData) + 1), figData, color="blue")
                #ax.set_title(self.typesListBox.currentItem().text())
                self.Canvas_3.figure.suptitle(self.typesListBox.currentItem().text(), fontsize=5)
                self.Canvas_3.draw()

    def DropDown_4ValueChanged(self):
        value = self.DropDown_4.currentText()
        if (value != ''):
            ax = self.Canvas_4.figure.add_subplot(111)
            ax.cla()
            figData = self.extractData(value)
            if figData != None:
                ax.plot(range(1, len(figData) + 1), figData, color="blue")
                #ax.set_title(self.typesListBox.currentItem().text())
                self.Canvas_4.figure.suptitle(self.typesListBox.currentItem().text(), fontsize=5)                
                self.Canvas_4.draw()

    def extractData(self, nodeName):
        global data
        global isRateTrace
        global typeIndex
        global fields
        value = self.fieldsListBox.currentItem().text()
        valueIndex = np.in1d(fields, str(value)).tolist().index(True)

        if(data[valueIndex][0].dtype != 'float32'):
            return

        typeName = self.typesListBox.currentItem().text()
        nodeFilter = []
        if(nodeName == 'AllNodes'):
            nodeFilter = np.ones(len(data[1]), dtype=np.int)
        else:
            for s in data[1]:
                if s == nodeName:
                    nodeFilter.append(1)
                else:
                    nodeFilter.append(0)

        typeFilter = []
        for s in data[typeIndex]:
            if s == typeName:
                typeFilter.append(1)
            else:
                typeFilter.append(0)

        if isRateTrace and self.faceCheckBox.isChecked():
            tempstr = self.faceDropDown.currentText()
            faceFilter = []
            for s in data[3]:
                if s == tempstr:
                    faceFilter.append(1)
                else:
                    faceFilter.append(0)
            typeFilter = np.array(typeFilter) & np.array(faceFilter)
            #typeFilter = [a and b for a,b in zip(typeFilter,faceFilter)]
        curTime = data[0][0]
        j = 0;
        figData = []
        figData.append(0)
        figData[0] = 0;
        for i in range(0,len(data[1])):
            if(nodeFilter[i] and typeFilter[i]):
                if(curTime == data[0][i]):
                    figData[j] = figData[j] + data[valueIndex][i]
                else:
                    curTime=data[0][i]
                    j+=1
                    figData.append(0)
                    figData[j]=data[valueIndex][i]
        global minFieldsValue
        m=np.inf
        for v in minFieldsValue:
            if v>0:
                if v<m:
                    m=v 
        if(nodeName == 'AllNodes'):
            self.sumLabel.setText("\nSum of " + str(typeName) + " of All nodes is: " + str(sum(figData)/len(figData))+
                                  "\nMin of " + str(typeName) + " of All nodes is: " +str(m)+
                                  "\nEach of " + str(typeName) + " is: " +str(minFieldsValue))
        else:
            self.averageTextEdit.setText(self.averageTextEdit.toPlainText() + "\nSum of " + str(typeName) + 
                                         " of " + str(nodeName) + " is: " + str(sum(figData)/len(figData)))

        return figData

    def getMinFieldsValue(self):
        global data
        global isRateTrace
        global typeIndex
        global fields
        global minFieldsValue
        minFieldsValue[:]=[]
        
        filed = self.fieldsListBox.currentItem().text()
        fieldIndex = np.in1d(fields, str(filed)).tolist().index(True)
        if(data[fieldIndex][0].dtype != 'float32'):
            return

        typeName = self.typesListBox.currentItem().text()
        global nodesList
        for nodeName in nodesList:
            nodeFilter = []
            for s in data[1]:
                if s == nodeName:
                    nodeFilter.append(1)
                else:
                    nodeFilter.append(0)
    
            typeFilter = []
            for s in data[typeIndex]:
                if s == typeName:
                    typeFilter.append(1)
                else:
                    typeFilter.append(0)
    
            if isRateTrace and self.faceCheckBox.isChecked():
                tempstr = self.faceDropDown.currentText()
                faceFilter = []
                for s in data[3]:
                    if s == tempstr:
                        faceFilter.append(1)
                    else:
                        faceFilter.append(0)
                typeFilter = np.array(typeFilter) & np.array(faceFilter)
                #typeFilter = [a and b for a,b in zip(typeFilter,faceFilter)]
            curTime = data[0][0]
            j = 0;
            figData = []
            figData.append(0)
            figData[0] = 0;
            for i in range(0,len(data[1])):
                if(nodeFilter[i] and typeFilter[i]):
                    if(curTime == data[0][i]):
                        figData[j] = figData[j] + data[fieldIndex][i]
                    else:
                        curTime=data[0][i]
                        j+=1
                        figData.append(0)
                        figData[j]=data[fieldIndex][i]
    
            minFieldsValue.append(sum(figData)/len(figData))
        return figData

    def setNodeNumber(self,startNumber):
        global nodesList
        if self.autoNodeCheckBox.isChecked():
            if(len(nodesList)-startNumber - 1 >= 1):
                self.DropDown_2.setCurrentIndex(startNumber+1)
            if (len(nodesList) - startNumber - 1 >= 2):
                self.DropDown_3.setCurrentIndex(startNumber + 2)
            if (len(nodesList) - startNumber - 1 >= 3):
                self.DropDown_4.setCurrentIndex(startNumber + 3)

    def valueChanged(self):
        pass

    def autoNodeCheckBoxChanged(self):
        self.setNodeNumber(0)
    
    def faceCheckBoxValueChanged(self):
        global data
        if self.faceCheckBox.isChecked():
            self.faceDropDown.addItems(np.unique(data[3]))
        else:
            self.faceDropDown.clear()
            self.typesListBoxValueChanged()
        self.faceDropDownValueChanged();

    def faceDropDownValueChanged(self):
        value = self.faceDropDown.currentText()
        self.typesListBoxValueChanged();

    def filesListBoxdoubleClicked(self):
        datadir = self.dirField.text()
        if(datadir != ''):
            self.getFileList(datadir)
         
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

exit(0)
