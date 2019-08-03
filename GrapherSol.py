#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 12:29:48 2019

@author: RyanAlco
"""

import networkx as nx
import matplotlib.pyplot as plt

from ProjectClassSol import project
from PersonClassSol import person
#import requests


Gr = nx.Graph() #Creates a new epmty graph 

def create_network(name = '', known_for = False, idnum = False, roles = 'Actors', every = False, layers = 0, cut = 0):
    #roles determines which types of people to fill the graph with
    #layers determines how many series of connections to view
    talent = person(name = name, known_for = known_for, idnum = idnum) #creates person object based on inputed variables 
    best_projs = talent.get_good_projects() #gets only the good projects from that person for size/runtime purposes
    
    for bp in best_projs.keys(): #loop through this person's good projects  
        proj = project(bp, cut) #for each project create a project object
        
        for role, per in proj.talent.items(): #loop through the cast in a project 
            if (role in roles) or (every == True): #based on which roles desired:
                for p in per: #loop through the people in a certain role
                    Gr.add_nodes_from([(p, {best_projs[bp] : role})]) #add a node for each person with info about the movie they're in and the role they play
                    if p != talent.name: #check to see if original person and person in projet are same person
                        Gr.add_edges_from([(talent.name, p, {best_projs[bp] : proj.rating})]) #add edge between the above two with info on the movie they're in and the movie's rating
                    if layers > 1: #check number of layers of connections wanted
                        #print ('here')
                        create_network(name = p, roles = roles, every = every, layers = layers - 1, cut = cut) #if want another layer, call function again with new central person from original person's projects cast and layers-1             
        Gr.add_nodes_from([(talent.name, {best_projs[bp] : talent.role})]) #add a node for central person if their role is not one chosen in original parameters
            
    return Gr #return graph data

    #NOTE: networkx will automatically not recreate a node/edge for someone it has already created one for. 
    #Programmed it so that for nodes/edges already created, their dictionary info is updated to convey additional projects
    #Also note that the above function does NOT present the network visually       


def visualize(g, para, labels = False, loose_ends = False):
    #function for visualizing graph
    #Remove edges from a new graph not old one
    graph = g
    
    eigenvec = nx.eigenvector_centrality(g) #dictionary for every node in the graph assign it centrality value based on node's eigenvector: node centrality is based on centrality of neighboring nodes 

    #print (type(eigenvec))
     
    for node in list(g.nodes()): #loop through nodes from graph g
        if (eigenvec[node] < para) or (loose_ends and g.degree(node) < 2): #the the centrality value of the node is less than selected parameter
            graph.remove_node(node) #remove the node (this also removes any edges connected to it)
    px = nx.spring_layout(graph) #present the graph in a 'spring' layout w/wo labels
    nx.draw(graph, pos = px, with_labels = labels)
    plt.show()

    #spring layout means presenting nodes such that to the greatest extent possible: edges are of similar length and as few edges crossing as poss


def find_path(graph, person1, person2):
    path = [p for p in nx.all_shortest_paths(graph, person1, person2)]
    if (path):
        return path
    else:
        return 'No path between those two people exists in this graph'


    
            
    
#test 2 = matt damon graph
#test 3 = mark gill
#test 4 = Daniel Kaluuya    
test5 = create_network('Charlie Chaplin', roles = 'Actors', layers = 2, cut = .20)
#visualize(test5, para = 0.0, labels = True)
#px = nx.spring_layout(test3)
#nx.draw(test3, pos = px, with_labels = True)
#plt.show()
#[p for p in nx.all_shortest_paths(test3, 'Mark Gill', 'Mark Gill')]
             
#what if multiple movies/edges together ->solved           
#edge thickness varies depending on total rank over projects
#Figure out which characters from the cast to include ->solved
#At some point stop adding layers and start making connections for when c_o = True ->solved
#Create graph first and then visualize WITH PARAMETER ->solved
#dictionary node info ->solved
#graph by id not name -.solved
#enter two people's names and create graph until target person is found?

#function for finding paths between people in graph

            

