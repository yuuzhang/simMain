import numpy as np
from dijkstra import *

'''
G = [[0, 4, 2, 0],
     [0, 0, 2, 3],
     [0, 0, 0, 5],
     [0, 0, 0, 0]]
G_Cost = [[0, 2, 2, 0],
     [0, 0, 1, 3],
     [0, 0, 0, 1],
     [0, 0, 0, 0]]
DEM = [[0, 0, 0, 4],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]
'''
'''
G=[[0,15,9,0,0,0],
[0,0,0,7,4,0],
[0,3,0,5,6,0],
[0,0,0,0,0,11],
[0,0,0,0,0,10],
[0,0,0,0,0,0,]]
G_Cost=[[0,2,6,0,0,0],
[0,0,0,8,9,0],
[ 0,3,0,5,3,0],
[0,0,0,0,0,3],
[0,0,0,0,0,1],
[0,0,0,0,0,0]]
DEM=[[0,0,0,0,0,11],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]]
'''

'''
G=[[0,3,0,0,3,0],
    [0,0,2,0,0,3],
    [0,3,0,3,0,0],
    [0,0,0,0,0,0],
    [0,0,3,0,0,0],
    [0,0,0,3,0,0]]
G_Cost=[[0,2,0,0,3,0],
    [0,0,2,0,0,3],
    [0,3,0,2,0,0],
    [0,0,0,0,0,0],
    [0,0,3,0,0,0],
    [0,0,0,3,0,0]]
DEM=[[0,0,0,5,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]]
nodesNumber=6

G = np.array(G)
G_Cost = np.array(G_Cost)
DEM = np.array(DEM)
nodesNumber = 6
'''

def SuccessiveShortestPath(G, G_Cost, DEM, nodesNumber):
    x = G.dot(0)
    pi = [0 for i in range(nodesNumber)]

    e = (DEM.transpose() - DEM).sum(0)
    E = np.where(e > 0)[0]
    D = np.where(e < 0)[0]
    RG_ReduceCost = G_Cost
    RG_Capacity = G.copy()
    originalReverseCapacity = G.dot(0)
    originalReverseCost = G.dot(0)

    cycleNo = 0
    flow = x
    while E.size != 0:
        i = 0
        dist, paths = dijkstra(RG_Capacity,RG_ReduceCost,E[0])

        p = paths[D[i]]
        if(not p):
            print("\n p is null! \n")
            break
        pi = pi - dist
        rij = np.zeros((1, np.size(p) - 1), dtype=int)[0]
        for j in range(0, np.size(p) - 1):
            rij[j] = RG_Capacity[p[j]][p[j+1]]
        delta = np.min([e[E[i]], -e[D[i]], min(rij)])
        x = x.dot(0)
        for j in range(0, np.size(p) - 1):
            x[p[j]][p[j + 1]] = delta
        flow += x
        e = e + x.sum(0) - x.sum(1).transpose()
        E = np.where(e > 0)[0]
        D = np.where(e < 0)[0]

        ones1 = np.ones((1, nodesNumber), dtype=int)[0]
        ones2 = np.ones((nodesNumber, 1), dtype=int)
        ones1.shape = (1, nodesNumber)
        ones2.shape = (nodesNumber,1)
        dist.shape = (1,nodesNumber)
        RG_ReduceCost = RG_ReduceCost + ((dist.transpose().dot(ones1) - (ones2.dot(dist))))

        # Set minus numbers to zero, to be improved
        #RG_ReduceCost = RG_ReduceCost * np.where(RG_ReduceCost > 0, 1, 0)

        RG_ReduceCost = RG_ReduceCost * np.where(RG_Capacity > 0, 1, 0)
        originalReverseCost = originalReverseCost - dist.transpose().dot(ones1) + ones2.dot(dist);
        originalReverseCost=originalReverseCost * np.where(originalReverseCapacity > 0, 1, 0)

        for j in range(0, np.size(p) - 1):
            pj = p[j]
            pj1 = p[j + 1]
            RG_Capacity[pj][pj1] = RG_Capacity[pj][pj1] - delta
            if RG_ReduceCost[pj1][pj] > 0:
                originalReverseCapacity[pj1][pj] = RG_Capacity[pj1][pj]
                originalReverseCost[pj1][pj] = RG_ReduceCost[pj1][pj]
                RG_Capacity[pj1][pj] = 0
            RG_Capacity[pj1][pj] = RG_Capacity[pj1][pj] + delta
            RG_ReduceCost[pj1][pj] = 0

            '''
            if RG_Capacity[pj][pj1] == 0:
                if originalReverseCapacity[pj1][pj] > 0:
                    RG_Capacity[pj1][pj] = originalReverseCapacity[pj1][pj]
                    originalReverseCapacity[pj1][pj] = 0
                    RG_ReduceCost[pj1][pj] = originalReverseCost[pj1][pj]
                    originalReverseCost[pj1][pj] = 0
            '''

            if RG_Capacity[pj][pj1] == 0:
                if originalReverseCapacity[pj][pj1] > 0:
                    RG_Capacity[pj][pj1] = originalReverseCapacity[pj][pj1]
                    originalReverseCapacity[pj][pj1] = 0
                    RG_ReduceCost[pj][pj1] = originalReverseCost[pj][pj1]
                    originalReverseCost[pj][pj1] = 0
            if RG_ReduceCost[pj1][pj] < 0:
                print("\nError, RG_ReduceCost < 0\n")

        cycleNo = cycleNo + 1
        if cycleNo > 10000:
            print("\nIterations more than 10000!\n")
            break

    flow = flow - flow.transpose()
    flow = flow * np.where(flow < 0, 0, 1)
    MiniCost = sum(sum(np.nan_to_num(G_Cost) * flow))

    return MiniCost, flow
