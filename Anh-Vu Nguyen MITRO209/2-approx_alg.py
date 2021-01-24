import time
import csv
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np






def read_file(path) : #Read file, construct list of edges and nodes
    edges=[]
    max_node=-1
    if path.endswith("txt") or path.endswith("edges"):
        file1 = open(path, 'r') 
        lines = file1.readlines()   
        for line in lines:
            
            L=[int(s) for s in line.strip().split()]
           
            if len(L)==2 and L[0]!="#": #ignore self-loops and non formated lines
                    if L[0]!=L[1]:edges+=[L]
                    max_node=max(max_node,max(L[0],L[1]))
    elif path.endswith("csv"):  
        with open(path, newline='') as File:  
            reader = csv.reader(File)
            next(reader)
            for row in reader:
                L=[int(s) for s in row]
               
                if len(L)==2  and L[0]!="#":  #ignore self-loops and non formated lines
                    if L[0]!=L[1]:edges+=[L]
                    max_node=max(max_node,max(L[0],L[1]))
    return edges,max_node

def list_adjacent(edges,max_node): #create list of neighbours for each node
    L=[[] for i in range(max_node+1)]
    
    for edge in edges:
        
        L[edge[0]].append(edge[1])
        L[edge[1]].append(edge[0])
    return L

def degree_function(list_adj): #Create a list of the degree of each node
    D=[]
    for node_neighbours in list_adj:
        D.append(len(node_neighbours))
    return D

def list_nodes_by_degree(D): #create a list of lists of nodes depending on the degree L[i] is a list of nodes of degree i.
    d_max=max(D)
    L=[[] for i in range (max(D)+1)]
    for node in range (len(D)):
        node_degree=D[node]
        L[node_degree].append(node)
    return L

def algo(path):
    ############ Init ##################
    edges,max_node=read_file(path)
    L_adjacent = list_adjacent(edges,max_node)
    deg = degree_function(L_adjacent)
    L_degrees=list_nodes_by_degree(deg)
    
  
    d_max=max(deg) #max degree in the graph
    d_min=min(deg) #min
    removed=[] #list of nodes that will be removed
    binary_removed=[0 for i in range(max_node+1)] #same but coded differently : binary_removed[i]=1 if node i is removed
    e_removed=[] #list of vertices that will be removed

    V = float(max_node+1) #starts at 0 so the number of numbers is the max + 1
    E = float(len(edges)) #V and E will be updated to give the density of H
    d=E/V #density that will be updated with E and V
    number_nodes=max_node+1 #self explanatory, unlike V, this will not be updated (constant)
    
   
    m=0 #length of e_removed
    final_E=0 #final number of edges that will be returned
    ### End of Init #####
    
    ######### LOOP of the greedy algorithm #########
    
    while number_nodes != len(removed) :
        while True: # THIS LINE :  L_degrees[deg[neighbour]-1].append(neighbour) ADD NODES to L_degrees, we need to make sure that the removed node has not been removed already !
            node = L_degrees[d_min].pop()#remove node with min degree
            while  d_min<d_max and not L_degrees[d_min] : #update d_min
                d_min+=1
            if binary_removed[node]==0:#if equals 1 it has already been previously removed, the loop removed another one
                break

        removed.append(node) #add node to removed nodes
        binary_removed[node]=1   #add node to removed nodes
        k=0 #count the number of edges removed to update density d
        for neighbour in L_adjacent[node]:
            if not binary_removed[neighbour] : #if the neighbor had been previously removed, the corresponding edge also : we dont remove twice !
                k+=1.0   
                L_degrees[deg[neighbour]-1].append(neighbour) #update degree list of nodes when we remove the edge
                if deg[neighbour]== d_min : d_min-=1 #update degree function and d_min
                deg[neighbour]-=1
                e_removed+=[[neighbour,node]] #add edge to list of removed edges
                
        #update E and V      
        V-=1.0 
        E-=k
        if V!=0 and float(E/V) > d  :
            #greedy : if it is denser, we momorize the removed edges by saving its current length
            #here, e_removed[m:] = H 
            m=len(e_removed)
            d=E/V
            final_E=E
    ### end of loop ###
            
    return final_E,len(edges),d,e_removed[m:]


def save(graph,path): #save graph to txt file in folder saved_results 
    import os
    if not os.path.exists('saved_results'):
        os.makedirs('saved_results')
    res=""
    for i in graph:
        res+=str(i[0])+" "+str(i[1])+"\n"
    f = open("saved_results/"+path[:-3]+".txt", "w+")
    f.write(res)
    f.close()



def testing():
    print("This program runs the greedy algorithm on all graphs in directory graphs/ \n")
    mypath="graphs/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    time_list=[]
    graph_sizes=[]
    for path in onlyfiles:
        print ("testing : "+str(path))
        

        t0=time.time()
        E,m,d,graph=algo(mypath+path)
        
        save(graph,path)

        
        t1=time.time()
        tot_time=t1-t0
        time_list.append(tot_time)                               
        graph_sizes.append(m)
        print("perf: "+str(tot_time)+"sec and m = "+str(m)+' edges')
        print('RESULT : density = '+ str(d)+" edges: "+str(E))
        print('=======================')
        
    plt.plot(graph_sizes, time_list, 'ro')
    m, b = np.polyfit(graph_sizes, time_list, 1)
    plt.plot(graph_sizes, m*np.array(graph_sizes) + b)
    plt.axis()
    
    plt.xlabel("|E|")
    plt.ylabel("run time (in sec)")
    plt.title("run time  vs. size of graph including reading and saving files")
    plt.show()
testing()
