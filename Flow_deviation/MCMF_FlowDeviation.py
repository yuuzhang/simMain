import time
from dijkstra import *
from SuccessiveShortestPath import *
from sympy import *
import scipy.optimize
import numpy as np


def fun_lambda_x(xt, G):
    with np.errstate(invalid='ignore'):
        a = np.sum(xt, 0)
        b = a / G
        return np.nanmax(np.sum(xt, 0) / G)


def fun_psi_lambdaex(x, G):
    with np.errstate(invalid='ignore'):
        Lambda_ex = sum(x, 0) / G
    psi_lambdaex = Lambda_ex / (1 - Lambda_ex)
    return psi_lambdaex


def fun3_lambdavh1(lambdavh,lambdawh):
    try:
        singular = (1 - lambdavh) / (lambdawh - lambdavh)
    except:
        pass
    d = np.sort(singular.flatten())
    firstSingular = d[np.where(d > 0)[0][0]]
    if(firstSingular > 1):
        firstSingular = 1
    else:
        firstSingular = firstSingular
    return firstSingular


#def MCMF_FlowDeviation(G, nodesCount, DEM):

from readTopology import *

isUndirectedGraph = True

G, G_Cost = readTopology("300Nodes.txt")
nodesCount = G.__len__()
DGSpa = np.zeros((nodesCount, nodesCount))
for item in G_Cost:
    DGSpa[item[0]][item[1]] = item[2]
K = int(np.floor(nodesCount / 2))
Demand = np.zeros((K, 3), dtype=int)
for k in range(K):
    Demand[k] = [k, K + k, 1]
DEM = np.zeros((nodesCount, nodesCount), dtype=int)
for dem in Demand:
    DEM[dem[0]][dem[1]] = dem[2]

G = DGSpa + DGSpa.transpose().dot(isUndirectedGraph)


startTime = time.time()
m = np.sum(np.where(G > 0, 1, 0))
epsilon = 0.1
q = np.ceil(-np.log2(epsilon))
with np.errstate(divide='ignore'):
    G_length = np.float(1) / G
source = np.where(DEM > 0)[0]
sink = np.where(DEM > 0)[1]
z = np.zeros((np.size(source), nodesCount, nodesCount))
for k in range(np.size(source)):
    dist, paths = dijkstra(G, G_length,source[k],sink[k])
    if dist == float('inf'):
        print("\nError: DEM not feasible!\n")
        # return
    for i in range(np.size(paths) - 1):
        z[k][paths[i]][paths[i + 1]] = DEM[source[k]][sink[k]]
#with np.errstate(divide='ignore'):
with np.errstate(invalid='ignore'):
    lambda_ex = np.true_divide(np.sum(z, 0), G)

lambda_z = np.nanmax(lambda_ex)

t = 0
xt = 1 / (2 * lambda_z) * z
gamma=1 / (2 * lambda_z)

while(True):
    lambda_xt = fun_lambda_x(xt, G)
    u = (1 - 0.5 * (1 - lambda_xt)) / lambda_xt
    yt = u * xt
    vh = yt
    vh1 = yt
    gamma = u * gamma
    lambdaex_symbol = Symbol("lambdaex_symbol")
    psi_lambdaex = lambdaex_symbol / (1 - lambdaex_symbol)
    gradpsi = simplify(diff(psi_lambdaex))
    gradCapitalpsi = gradpsi * 1 # ?
    h = 0
    while(True):
        vh = vh1
        with np.errstate(invalid='ignore'):
            lambdaex = sum(vh, 0) / G
            f_func = lambdify(lambdaex_symbol, gradCapitalpsi)
            G_Cost = f_func(lambdaex) / G

        w = np.zeros((np.size(source), nodesCount, nodesCount))
        for k in range(np.size(source)):
            DEMTemp = np.zeros((nodesCount, nodesCount))
            DEMTemp[source[k]][[sink[k]]] = gamma * DEM[source[k]][[sink[k]]]
            MiniCost, Flow = SuccessiveShortestPath(G, G_Cost, DEMTemp, nodesCount)

            w[k] = Flow

        with np.errstate(invalid='ignore'):
            lambdav = np.sum(vh, 0) / G
            lambdaw = np.sum(w, 0) / G
        lambdav[np.isnan(lambdav)] = 0
        lambdav[np.isinf(lambdav)] = 0
        lambdaw[np.isnan(lambdaw)] = 0
        lambdaw[np.isinf(lambdaw)] = 0


        def fun_Capitalpsi_v(sigma):
            vh1 = (1 - sigma) * lambdav + sigma * lambdaw
            psi_v = vh1 / (1 - vh1)
            Capitalpsi_v = np.sum(psi_v)
            return Capitalpsi_v

        domain = fun3_lambdavh1(lambdav, lambdaw)
        sigma = scipy.optimize.fminbound(fun_Capitalpsi_v, 0, domain)
        vh1 = (1 - sigma) * vh + sigma * w

        psivh = fun_psi_lambdaex(vh, G)
        psivh[np.isnan(psivh)] = 0
        psih = np.sum(psivh)

        psivh1 = fun_psi_lambdaex(vh1, G)
        psivh1[np.isnan(psivh1)] = 0
        psih1 = np.sum(psivh1)

        if (psih - psih1) < psih**2 / (128 * (psih**3 + m)):
            t = t + 1
            xt = vh1
            break
        h = h + 1

        if h > 50000:
            print("\nToo many iterations\n")

    psiLambdaex = fun_psi_lambdaex(xt, G)
    psiLambdaex[np.isnan(psiLambdaex)] = 0
    CapitalpsiXt = np.sum(psiLambdaex)
    lambda_xt = fun_lambda_x(xt, G)
    if (lambda_xt >= 1 - epsilon / (2*m)) or (CapitalpsiXt >= m * 2**(q+2)):
        break
    print(gamma)

endTime = time.time()
print("END ")
print(endTime - startTime)