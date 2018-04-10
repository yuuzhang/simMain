import numpy as np


def dijkstra(G, G_Cost, source, sink=-1):
    s = []
    ss = range(0, G.__len__())
    d = [float('inf')] * G.__len__()
    pred = [float('inf')] * G.__len__()
    d[source] = 0
    pred[source] = source

    while ss:
        tmp = [d[index] for index in ss]
        i = ss[tmp.index(min(tmp))]

        if i == sink:
            break

        s.append(i)
        ss.remove(i)
        for x in np.nonzero(G[i])[0]:
            if G[i][x] > 0 and d[x] > d[i] + G_Cost[i][x]:
                d[x] = d[i] + G_Cost[i][x]
                pred[x] = i

    if sink < 0:
        path = [[] for i in range(G.__len__())]
        for i in range(G.__len__()):
            if(pred[i] == float('inf')):
                continue
            if(i != source):
                path[i].append(i)
            i_pred = i
            while(pred[i_pred] != source):
                path[i].append(pred[i_pred])
                i_pred = pred[i_pred]
            path[i].append(source)
            path[i].reverse()
        d = np.array(d)
        path = np.array(path)
    else:
        path = []
        if (pred[i] == float('inf')):
            print("\nError: No route availabel!\n")
            return d[sink], path
        path.append(sink)
        sink_pred = sink
        while(pred[sink_pred] != source):
            path.append(pred[sink_pred])
            sink_pred = pred[sink_pred]
        path.append(source)
        path.reverse()
        d = d[sink]
        path = np.array(path)

    return d, path


'''
from readTopology import *


G, G_Cost = readTopology("16nodes-1.txt")
nodesCount = G.__len__()
DGSpa = [[0 for i in range(nodesCount)] for i in range(nodesCount)]
for item in G_Cost:
    DGSpa[item[0]][item[1]] = item[2]
d, path = dijkstra(DGSpa, DGSpa, 4)
print(d)
'''