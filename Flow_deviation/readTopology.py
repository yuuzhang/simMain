import numpy as np
import re
import StringIO


def readTopology(filename):
    topology_flag = 0
    nodes = []
    edges = []

    fid = open(filename, 'r')
    lines = fid.readlines()
    for line in lines:
        line = re.split('\t?\n', line)[0]
        if line == "" or line[0] == '#':
            continue
        elif line == "router":
            topology_flag = 1;
            continue;
        elif line == "link":
            topology_flag = 2;
            continue;

        if topology_flag == 1:
            nodeCell = np.loadtxt(StringIO.StringIO(line), delimiter="\t", dtype='S50,S50,i,i,i')
            nodes.append(list(nodeCell.tolist()))
        if topology_flag == 2:
            nodeCell = re.findall(r"\d+[.]?\d*", line)
            nodeCell = [float(i) for i in nodeCell]
            nodeCell = [int(i) for i in nodeCell]
            edges.append(nodeCell)
    nodes = np.array(nodes)
    edges = np.array(edges)
    return nodes, edges


#readTopology("16nodes-1.txt")