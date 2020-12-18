import time
import csv
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np

def read_file(path) :
    vertices=[]
    nodes=[]
    if path.endswith("txt"):
        file1 = open(path, 'r') 
        lines = file1.readlines()   
        for line in lines:
            
            L=[int(s) for s in line.strip().split()]
           
            if len(L)==2 : #ignore self-loops and non formated lines
                    if L[0]!=L[1]:vertices+=[L]
                    nodes+=L 
    elif path.endswith("csv"):  
        with open(path, newline='') as File:  
            reader = csv.reader(File)
            next(reader)
            for row in reader:
                L=[int(s) for s in row]
               
                if len(L)==2 : #ignore self-loops and non formated lines
                    if L[0]!=L[1]:vertices+=[L]
                    nodes+=L 
    return vertices,list(set(nodes))

def list_adjacence(vertices,nodes):
    L=[[] for i in range(max(nodes)+1)]
    
    for vertice in vertices:
    
        L[vertice[0]].append(vertice[1])
        L[vertice[1]].append(vertice[0])
    return L

def degree_function(list_adj,nodes):
    D=[]
    for node_voisins in list_adj:
        D.append(len(node_voisins))
    return D

def list_nodes_by_degree(D):
    d_max=max(D)
    L=[[] for i in range (d_max+1)]
    for node in range (len(D)):
        node_degree=D[node]
        L[node_degree].append(node)
    return L

def algo(path):
    ############ Init ##################
    vertices,nodes=read_file(path)
    #visualize(vertices)
    L_adjacence = list_adjacence(vertices,nodes)
    deg = degree_function(L_adjacence, nodes)
    L_degrees=list_nodes_by_degree(deg)
    V = float(len(nodes))
    E = float(len(vertices))
    d_max=max(deg)
    d_min=min(deg)
    removed=[]
    binary_removed=[0 for i in range(max(nodes)+1)]
    v_removed=[]
    number_nodes=len(nodes)
    p=E/V
    l=0
    m=0
    d=p

    print("init")
    ######### Boucle #########
    while number_nodes != len(removed) :
        while True:
            vertice = L_degrees[d_min].pop()
            while  d_min<d_max and not L_degrees[d_min] :
                d_min+=1
            if binary_removed[vertice]==0:
                break

        removed.append(vertice)
        binary_removed[vertice]=1   
        k=0
        for voisin in L_adjacence[vertice]:
            if not binary_removed[voisin] :
                k+=1.0   
                L_degrees[deg[voisin]-1].append(voisin)
                if deg[voisin]== d_min : d_min-=1
                deg[voisin]-=1
                v_removed+=[[voisin,vertice]]
                
        V-=1.0
        E-=k
        if V!=0 and float(E/V) > d  :
            l=len(removed)
            m=len(v_removed)
            d=E/V
    #print("|nodes| "+str(len(removed[l:])))   
    return len(nodes),len(vertices),d,v_removed[m:]

def visualize(vertices):
    import matplotlib.pyplot as plt
    import networkx as nx
    options = {
    'node_color': 'yellow',
    'node_size': 1,
    'width': 1,
    }
    G = nx.Graph()
    for v in vertices:
        G.add_edge(v[0],v[1])
    plt.subplot(122)
    nx.draw(G,**options)
    plt.show()

def testing():
    mypath="graphs/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    time_list=[]
    n_plus_m=[]
    for path in onlyfiles:
        print ("testing : "+str(path))
        t0=time.time()
        n,m,d,graph=algo(mypath+path)
        t1=time.time()
        tot_time=t1-t0
        time_list.append(tot_time)                               
        n_plus_m.append(n+m)
        print("perf: "+str(tot_time)+" for n= "+str(n)+" and m = "+str(m))
        print('density = '+ str(d))
        print('=======================')
        
    plt.plot(n_plus_m, time_list, 'ro')
    m, b = np.polyfit(n_plus_m, time_list, 1)
    plt.plot(n_plus_m, m*np.array(n_plus_m) + b)
    plt.axis()
    
    plt.xlabel("|E|+|V|")
    plt.ylabel("run time (in sec)")
    plt.title("run time  vs. size of graph")
    plt.show()
testing()
