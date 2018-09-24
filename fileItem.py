# -*- coding: utf8 -*
import pandas as pd
import numpy as np
import traceback
from fileInterface import fileInterface

class rateFile(fileInterface):
    def __init__(self, filePath, fileName):
        self.fileType = 'rate'
        fullPath = filePath + '/' + fileName
        # return
        self.fields, data = fileInterface.loadData(fullPath, 'f,S50,f,S50,S50,f,f,f,f,')

        self.dataf = self.loadDataf(data)

        self.nodesList = sorted(np.unique(data[1]), key=fileInterface.customedSort)
        self.faceList = np.unique(data[3])

        typeIndex = np.isin(self.fields, 'Type').tolist().index(True)
        self.types = np.unique(data[typeIndex]).tolist()
        #for typeName in np.unique(data[typeIndex]):
        #   self.types.append(typeName)

    @staticmethod
    def loadDataf(data):
        dataf = pd.DataFrame(np.transpose(data),
                             columns=['Time', 'Node', 'FaceId', 'FaceDescr', 'Type', 'Packets', 'Kilobytes',
                                      'PacketRaw',
                                      'KilobytesRaw'])
        dataf[['Time']] = dataf[['Time']].astype(float)
        dataf[['Packets']] = dataf[['Packets']].astype(float)
        dataf[['Kilobytes']] = dataf[['Kilobytes']].astype(float)
        dataf[['PacketRaw']] = dataf[['PacketRaw']].astype(float)
        dataf[['KilobytesRaw']] = dataf[['KilobytesRaw']].astype(float)
        return dataf

    def getFieldSummary(self, face, field, typeName):
        fieldSummary = []
        filterData = self.dataf[(self.dataf['Type'] == typeName)]

        if face != '':
            filterData = filterData[(filterData['FaceDescr'] == face)]
        filterData = filterData[['Time', 'Node', field]]
        filterData.sort_values(by=['Node'])
        filterData = filterData.groupby(by=['Time', 'Node']).sum()
        groupeddata = filterData.groupby('Node').mean()

        for node in self.nodesList:
            if node in groupeddata[field]:
                fieldSummary.append(groupeddata[field][node])
        #sumS, minS, outputstr = fileInterface.getSumMinOutputstr(fieldSummary)
        return fieldSummary

    def extractData2(self, face, nodeName, field, typeName):
        LabelText = ""
        statusText = ""
        figdata = []

        fieldSummary = self.getFieldSummary(face, field, typeName)
        self.sum = fileInterface.getFieldSum(fieldSummary)
        self.min = fileInterface.getFieldMin(fieldSummary)
        outputStr = fileInterface.getOutputstr(fieldSummary)

        filterData = self.dataf[['Time', 'Node', 'FaceDescr', 'Type', field]]
        filterData = filterData[(self.dataf['Type'] == typeName)]

        if face != '':
            filterData = filterData[(filterData['FaceDescr'] == face)]
            if len(filterData) == 0:
                return LabelText, statusText, figdata

        if nodeName == 'AllNodes':
            figdata = filterData.groupby(by=['Time', 'Node']).sum()
            LabelText = fileInterface.buildSumMinText(typeName, self.sum, self.min, outputStr)
        else:
            filterData = filterData[(filterData['Node'] == nodeName)]
            figdata = filterData.groupby(by=['Time']).sum()
            if len(figdata) == 0:
                figdata = []
            else:
                ave = sum(figdata[field]) / len(figdata)
                LabelText = LabelText + fileInterface.buildaNodeText(typeName, nodeName, ave)

        return LabelText, statusText, figdata


class delayFile(fileInterface):
    def __init__(self, filePath, fileName):
        self.fileType = 'delay'
        fullPath = filePath + '/' + fileName
        # return
        self.fields, data = fileInterface.loadData(fullPath, 'f,S50,f,f,S50,f,f,f,f')

        self.dataf = self.loadDataf(data)

        self.nodesList = sorted(np.unique(data[1]), key=fileInterface.customedSort)
        self.faceList = np.unique(data[3])

        typeIndex = np.isin(self.fields, 'Type').tolist().index(True)
        self.types = np.unique(data[typeIndex]).tolist()
        #for typeName in np.unique(data[typeIndex]):
        #   self.types.append(typeName)

    @staticmethod
    def loadDataf(data):
        dataf = pd.DataFrame(np.transpose(data),
                             columns=['Time', 'Node', 'AppId', 'SeqNo', 'Type', 'DelayS', 'DelayUS', 'RetxCount',
                                      'HopCount'])
        dataf[['Time']] = dataf[['Time']].astype(float)
        dataf[['DelayS']] = dataf[['DelayS']].astype(float)
        dataf[['DelayUS']] = dataf[['DelayUS']].astype(float)
        dataf[['RetxCount']] = dataf[['RetxCount']].astype(float)
        dataf[['HopCount']] = dataf[['HopCount']].astype(float)
        return dataf

    def getFieldSummary(self, face, field, typeName):
        fieldSummary = []

        filterData = self.dataf[['Time', 'Node', 'Type', field]]
        filterData = filterData[(self.dataf['Type'] == typeName)]
        groupeddata = filterData.groupby('Node').mean()

        for node in self.nodesList:
            if node in groupeddata[field]:
                fieldSummary.append(groupeddata[field][node])
        #sumS, minS, outputstr = fileInterface.getSumMinOutputstr(fieldSummary)
        return fieldSummary

    def extractData2(self, face, nodeName, field, typeName):
        LabelText = ""
        statusText = ""

        fieldSummary = self.getFieldSummary(face, field, typeName)
        self.sum = fileInterface.getFieldSum(fieldSummary)
        self.max = fileInterface.getFieldMax(fieldSummary)
        outputStr = fileInterface.getOutputstr(fieldSummary)

        filterData = self.dataf[['Time', 'Node', 'Type', field]]
        figdata = filterData[(self.dataf['Type'] == typeName)]
        figdata = figdata[[field]]

        if nodeName == 'AllNodes':
            LabelText = fileInterface.buildSumMaxText(typeName, self.sum, self.max, outputStr)
        else:
            figdata = filterData[(filterData['Node'] == nodeName)]
            figdata = figdata[[field]]
            if len(figdata) == 0:
                figdata = []
            else:
                ave = sum(figdata[field]) / len(figdata)
                LabelText = LabelText + fileInterface.buildaNodeText(typeName, nodeName, ave)

        return LabelText, statusText, figdata
