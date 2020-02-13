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


Gr = nx.Graph() 
seen = [] 

def create_network(name = '', known_for = False, idnum = False, roles = 'Actors', every = False, layers = 0, cut = 0):
#Function for creating the graph
#roles determines which types of people to fill the graph with (can set every to true and all roles are received)
#layers determines how many series of connections to view
    talent = person(name = name, known_for = known_for, idnum = idnum) #creates person object based on inputed variables 
    seen.append(idnum)
    best_projs = talent.get_projects() 
    
    for first, second in best_projs.items():  
        proj = project(first, second[2], cut) 
        
        for role, per in proj.talent.items(): 
            if (role in roles) or (every == True): 
                for p in per: 
                    Gr.add_nodes_from([(per[p], {second[0] : role})]) 
                    if per[p] != talent.name: 
                        Gr.add_edges_from([(talent.name, per[p], {second[0] : second[1]})]) 
                    if layers > 1 and p not in seen: 
                        create_network(idnum = p, roles = roles, every = every, layers = layers - 1, cut = cut)              
        Gr.add_nodes_from([(talent.name, {second[0] : talent.role})]) 
        
    return Gr 

#NOTE: networkx will automatically not recreate a node/edge for someone it has already created one for. 
#Programmed it so that for nodes/edges already created, their dictionary info is updated to convey additional projects
#Also note that the above function does NOT present the network visually       


def visualize(g, para, labels = False, loose_ends = False):
#function for visualizing graph
    graph = nx.Graph()
    graph = g
    eigenvec = nx.eigenvector_centrality(graph)  
    
    first = list(graph.nodes())[0]
    
    for node in list(graph.nodes()): 
        if (eigenvec[node] < para) or (loose_ends and g.degree(node) < 2): 
            graph.remove_node(node) 
    
    node_list = []
    for node in graph.nodes(): 
        path = nx.shortest_path(graph, first, node)
        if len(path) >= 3:
            node_list.append('blue')
        if len(path) == 2:
            node_list.append('yellow')
        if len(path) == 1:
            node_list.append('r')
    
    px = nx.spring_layout(graph) 
    nx.draw_networkx_nodes(graph, pos = px, node_color = [p for p in node_list], alpha = .9)
    nx.draw_networkx_edges(graph, pos = px, edge_color = 'grey', alpha = .25)
    if labels:
        nx.draw_networkx_labels(graph, pos = px)
    #nx.draw(graph, pos = px, with_labels = labels, node_color = [p for p in node_list], edge_color = 'grey')
    plt.axis('off')
    plt.show()

    #spring layout means presenting nodes such that to the greatest extent possible: edges are of similar length and as few edges crossing as poss

def score(graph, people):
#Computes the 'score' for a path of names in shortest path function
#Score is based off of number of movies people in the path have done together 
    total = 0
    size = len(people) - 1
    for i in range(size):
        total += len(graph.get_edge_data(people[i], people[i+1]))
    return total

def find(graph, people):
#Function for finding the average movie rating in a path of people
    total = 0
    num = 0
    size = len(people) - 1
    for i in range(size):
        total += sum(graph.get_edge_data(people[i], people[i+1]).values())
        num += len(graph.get_edge_data(people[i], people[i+1]))
    return total / num


def show_projects(graph, people):
#Function for printing out shortest path of people with the most movies in between coworkers
    s = people[0]
    size = len(people) - 1
    for i in range(size):
        s += ' -> '
        s += str(list(graph.get_edge_data(people[i], people[i+1]).keys()))
        s += ' -> '
        s += people[i+1]
    return s


def find_path(graph, person1, person2, num_movies = False, centrality = False, rating = False):
#Function to find the shortest path between two people
#Options for type of shortest path to return based off of different weights
#Option for number of movies and option for centrality level of people 
    try:
        paths = [p for p in nx.all_shortest_paths(graph, person1, person2)]
        if centrality:
            eigenvec = nx.eigenvector_centrality(graph)
            d = {}
            for path in paths:
                total = []
                [total.append(eigenvec[person]) for person in path[1:-1]]
                sum_total = sum(total)
                d[sum_total] = path
            return show_projects(graph, d[max(d.keys())])
        if num_movies:
            l = []
            for path in paths:
                l.append(score(graph, path))
            final = [show_projects(graph, paths[i]) for i in range(len(l)) if l[i] == max(l)]
            return final
        if rating:
            num = 0
            for path in paths:
                val = find(graph, path)
                if val > num:
                    num = val
                    l = path
            return show_projects(graph, l)
        else:
            return paths
    except:
        return 'No path between those two people exists in this graph'

          
    
    
ng = create_network('Mark Gill', roles = 'Actors Producers Directors', layers = 2, cut = .20)
#visualize(ng, para = .035, labels = True, loose_ends = False)
            

