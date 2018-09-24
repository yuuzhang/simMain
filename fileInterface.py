import re
import numpy as np
import traceback


class fileInterface(object):
    def __init__(self):
        pass

    def getFieldSummary(self, face, field, typeName):
        pass

    def extractData2(self, face, nodeName, field, typeName):
        pass

    @staticmethod
    def loadData(path, datatype):
        try:
            fid = open(path, 'r')
            headline = fid.readline()
            fields = headline.split('\t')
            del fields[-1]  # Remove "\n"
            data = np.loadtxt(fid, delimiter='\t', unpack=True, dtype=datatype)
        except:
            traceback.print_stack()
            exit(-1)
        return fields, data

    @staticmethod
    def getFieldSum(fieldSummary):
        return sum(fieldSummary)

    @staticmethod
    def getFieldMin(fieldSummary):
        m = np.inf
        for v in fieldSummary:
            if (v > 0) & (v < m):
                m = v
        return m

    @staticmethod
    def getFieldMax(fieldSummary):
        m = 0
        for v in fieldSummary:
            if v > m:
                m = v
        return m

    @staticmethod
    def getOutputstr(fieldSummary):
        outputStr = ""
        for v in fieldSummary:
            outputStr = outputStr + "{:.3f} ---".format(v)

        return outputStr

    @staticmethod
    def buildSumMinText(typeName, s, m, outputStr):
        return "\nSum of " + str(typeName) + " of All nodes is: " + str(s) + \
               "\nMin of " + str(typeName) + " of All nodes is: " + str(m) + \
               "\nEach of " + str(typeName) + " is: " + outputStr

    @staticmethod
    def buildSumMaxText(typeName, s, m, outputStr):
        return "\nSum of " + str(typeName) + " of All nodes is: " + str(s) + \
               "\nMax of " + str(typeName) + " of All nodes is: " + str(m) + \
               "\nEach of " + str(typeName) + " is: " + outputStr

    @staticmethod
    def buildaNodeText(typeName, nodeName, ave):
        return "\nSum of " + str(typeName) + \
               " of " + str(nodeName) + " is: %.3f" % (ave)

    @staticmethod
    def customedSort(nodeName):
        return int(re.findall("\d+", nodeName)[0])

    def getFields(self):
        return self.fields

    def getTypes(self):
        return self.types

    def getFullPath(self):
        return self.fullPath

    def getFileType(self):
        return self.fileType

    def getNodesList(self):
        return self.nodesList

    def getFaceList(self):
        return self.faceList

    def getSum(self):
        return self.sum

    def getMin(self):
        try:
            return self.min
        except:
            return ''

    def getMax(self):
        try:
            return self.max
        except:
            return ''
