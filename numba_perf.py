import time
import csv
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np
from numba import jit,njit
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings

warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)


def read_file(path) :#43ms
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
    return np.array(vertices, dtype = np.int64, order='C'),np.array(list(set(nodes)),dtype = np.int64, order='C')


def list_adjacence(vertices,nodes):#15
    L = np.empty(max(nodes)+1, dtype=np.object)
    L[:]=[[] for i in range(max(nodes)+1)]

    
    for vertice in vertices:
    
        L[vertice[0]].append(vertice[1])
        L[vertice[1]].append(vertice[0])
    return np.array(L,dtype=object)
  

def degree_function(list_adj,nodes):
    D=np.zeros((len(list_adj)), np.int64)
    for i in range(len(list_adj)):
        D[i]=len(list_adj[i])
    return D

def list_nodes_by_degree(D):
    d_max=max(D)
    L=[[] for i in range (d_max+1)]
    for node in range (len(D)):
        node_degree=D[node]
        L[node_degree].append(node)
    return L
@jit
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
    number_nodes=len(nodes)
    removed=np.zeros(number_nodes, np.int64)
    length_removed=0
    binary_removed=np.zeros(max(nodes)+1,np.int64)
    v_removed=np.zeros((len(vertices),2), np.int64)
    len_v_removed=0
    
    p=E/V
    l=0
    m=0
    d=p

    print("init")
    ######### Boucle #########
    while number_nodes != length_removed :
        while 1:
            vertice = L_degrees[d_min].pop()
            while  d_min<d_max and len(L_degrees[d_min])==0 :
                d_min+=1
            if binary_removed[vertice]==0:
                break
        removed[length_removed]=vertice
        length_removed+=1
        binary_removed[vertice]=1
       
        k=0
        for i in range(len(L_adjacence[vertice])):
            voisin =L_adjacence[vertice][i]
            if  binary_removed[voisin]==0 :
                k+=1.0   
                L_degrees[deg[voisin]-1].append(voisin)
                if deg[voisin]== d_min : d_min-=1
                deg[voisin]-=1
                v_removed[len_v_removed]=[voisin,vertice]
                len_v_removed+=1
             
                
        V-=1.0
        E-=k
      
        if V!=0 and float(E/V) > d  :
            l=length_removed
            m=len_v_removed
            d=E/V
        
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
    mypath="graphs/test/"
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
        
##    plt.plot(n_plus_m, time_list, 'ro')
##    m, b = np.polyfit(n_plus_m, time_list, 1)
##    plt.plot(n_plus_m, m*np.array(n_plus_m) + b)
##    plt.axis()
##    
##    plt.xlabel("|E|+|V|")
##    plt.ylabel("run time (in sec)")
##    plt.title("run time  vs. size of graph")
##    plt.show()
testing()
