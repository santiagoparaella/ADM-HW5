#!/usr/bin/env python
# coding: utf-8

import pandas as pd, networkx as nx
import matplotlib.pyplot
import folium
# Loading files as a panda data frame
nodeInfo = pd.read_csv('nodeInfo.co', skiprows = 7, sep = " ", delimiter = " ",
                         names = ["Character", "ID_Node", "Longitude", "Latitude"])
nodeInfo.drop(columns = ["Character"], inplace = True)

physical_dist = pd.read_csv('distance.gr', skiprows = 7, sep = " ", delimiter = " ",
                         names = ["Character", "Node_1", "Node_2", "Physical_distance"])
physical_dist.drop(columns = ["Character"], inplace = True)

nodes = list(nodeInfo['ID_Node']) # list of all nodes

# making graph from the pandas dataframe 
G = nx.from_pandas_edgelist(physical_dist, 'Node_1', 'Node_2', ['Physical_distance'], create_using = nx.DiGraph())

# this function returns a dic of node's coordinates
def getpos(nodes):
    pos=dict()
    for node in nodes:
        pos[node]=[nodeInfo.loc[node-1,'Longitude'], nodeInfo.loc[node-1,'Latitude']]
    return pos

# this function visualize the result using folium map and save it as a html file(also it can be displayed on jupyter notebook)
def visualize(pos, start):
    
    m = folium.Map(location = [nodeInfo.loc[start-1,'Latitude']/1000000, 
                           nodeInfo.loc[start-1,'Longitude']/1000000], 
                           zoom_start = 17,tiles = 'openstreetmap')
    locations=[]
    locations.append((nodeInfo.loc[start-1,'Latitude']/1000000,nodeInfo.loc[start-1,'Longitude']/1000000))
    folium.Marker(location=[nodeInfo.loc[start-1,'Latitude']/1000000, 
                           nodeInfo.loc[start-1,'Longitude']/1000000],
                          icon=folium.Icon(color = 'green',icon='leaf'),
                          popup='<strong>Start</strong>').add_to(m) # Start point
    for node in list(pos.keys()):
        folium.Marker(location = (pos[node][1]/1000000, 
                                  pos[node][0]/1000000), 
                      radius = 5, line_color = '#3186cc', icon=folium.Icon(color = 'red'), 
                      fill_color = '#FFFFFF', 
                      fill_opacity = 0.7, fill = True).add_to(m)
        
        locations.append((pos[node][1]/1000000, pos[node][0]/1000000))
    folium.PolyLine(locations).add_to(m)
    #display(m)
    m.save('index.html')


def func_1():
    v = int(input('Enter a node: '))  # the initial node
    d = int(input('Enter a distance threshold: '))  #the distance threshold
    start = v # for visualization
    # The algorithm for this part is BFS with a distance
    # The visited state is a list that: if visit_state[i] = True it means the i-th node was visited
    # The dist is an array that will contain the distances of all visited nodes from the initial node
    visit_state = [False]*(len(nodes)+1) 
    dist = [0]*(len(nodes)+1) 
    visited = set() # inorder to return the neighbor nodes
    queue = []
    queue.append(v)
    visit_state[v] = True
    visedge = [] # To save the edges of neighbors(not necessary)
    while queue:
        s = queue.pop()
        n = [j for j in G.neighbors(s)] # n is the neighbors of s
        for i in n:
            if visit_state[i] == False:
                temp = int(G.edges[(s,i)]['Physical_distance']) + dist[s]
                if temp <= d:
                    queue.append(i)
                    visit_state[i]=True
                    visited.add(i)
                    dist[i]=temp
                    visedge.append((s,i))
    if not visited:
        return "Nothing with this distance!"
    else:
        pos = getpos(visited)
        print("\nAll the neighbors you can go from,",start,", within your input distance:\n",visited,'\nAnd wait for the map to create!')
        return visualize(pos,start)


func_1()
