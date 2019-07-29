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


Gr = nx.Graph()

def create_network(name = '', known_for = False, idnum = False, roles = 'Actors', every = False, layers = 0, cut = 0):
    #print ('here1')
    talent = person(name = name, known_for = known_for, idnum = idnum)
    best_projs = talent.get_good_projects()
    
    for bp in best_projs:
        bp = project(bp, cut)
        
        for role, per in bp.talent.items():
            if (role in roles) or (every == True):
                for p in per:
                    Gr.add_nodes_from([(p, {bp.title : role})])
                    if p != talent.name:
                        Gr.add_edges_from([(talent.name, p, {bp.title : bp.rating})])
                    if layers > 1:
                        create_network(name = p, roles = roles, every = every, layers = layers - 1, cut = cut)
        Gr.add_nodes_from([(talent.name, {bp.title : talent.role})])
            
    return Gr
            


def visualize(g, para, labels = False):
    
    eigenvec = nx.eigenvector_centrality(g)
    print (type(eigenvec))
     
    for node in list(g.nodes()):
        if eigenvec[node] < para:
            g.remove_node(node)
    px = nx.spring_layout(g)
    nx.draw(g, pos = px, with_labels = labels)
    plt.show()


    
            
    
#test 2 = matt damon graph
#test 3 = mark gill
#test4 = create_network('Daniel Kaluuya', layers = 2, cut = .25)
print (visualize(g = test4, para = .01, labels = True))
#px = nx.spring_layout(test3)
#nx.draw(test3, pos = px, with_labels = True)
#plt.show()
    
             
#what if multiple movies/edges together ->solved           
#edge thickness varies depending on total rank over projects
#Figure out which characters from the cast to include ->solved
#At some point stop adding layers and start making connections for when c_o = True
#Create graph first and then visualize WITH PARAMETER
#dictionary node info ->solved
#graph by id not name -.solved
            

