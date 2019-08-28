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


Gr = nx.Graph() #Creates a new epmty graph 
seen = [] #list of seen people prevents loop connections

def create_network(name = '', known_for = False, idnum = False, roles = 'Actors', every = False, layers = 0, cut = 0):
    #Function for creating the graph
    #roles determines which types of people to fill the graph with (can set every to true and all roles are received)
    #layers determines how many series of connections to view
    talent = person(name = name, known_for = known_for, idnum = idnum) #creates person object based on inputed variables 
    seen.append(idnum)
    best_projs = talent.get_projects() #gets only the good projects from that person for size/runtime purposes
    
    for first, second in best_projs.items(): #loop through this person's good projects  
        proj = project(first, second[2], cut) #for each project create a project object
        
        for role, per in proj.talent.items(): #loop through the cast in a project 
            if (role in roles) or (every == True): #based on which roles desired:
                for p in per: #loop through the people in a certain role
                    Gr.add_nodes_from([(per[p], {second[0] : role})]) #add a node for each person with info about the movie they're in and the role they play
                    if per[p] != talent.name: #check to see if original person and person in projet are same person
                        Gr.add_edges_from([(talent.name, per[p], {second[0] : second[1]})]) #add edge between the above two with info on the movie they're in and the movie's rating
                    if layers > 1 and p not in seen: #check number of layers of connections wanted
                        create_network(idnum = p, roles = roles, every = every, layers = layers - 1, cut = cut) #if want another layer, call function again with new central person from original person's projects cast and layers-1             
        Gr.add_nodes_from([(talent.name, {second[0] : talent.role})]) #add a node for central person if their role is not one chosen in original parameters
        
    return Gr #return graph data

    #NOTE: networkx will automatically not recreate a node/edge for someone it has already created one for. 
    #Programmed it so that for nodes/edges already created, their dictionary info is updated to convey additional projects
    #Also note that the above function does NOT present the network visually       


def visualize(g, para, labels = False, loose_ends = False):
    #function for visualizing graph
    graph = nx.Graph()
    graph = g
    eigenvec = nx.eigenvector_centrality(g) #dictionary for every node in the graph assign it centrality value based on node's eigenvector: node centrality is based on centrality of neighboring nodes 
    
    first = list(g.nodes())[0]
    
    for node in list(graph.nodes()): #loop through nodes from graph g
        if (eigenvec[node] < para) or (loose_ends and g.degree(node) < 2): #the the centrality value of the node is less than selected parameter
            graph.remove_node(node) #remove the node (this also removes any edges connected to it)
    
    node_list = []
    for node in graph.nodes(): #for coloring nodes of different layers
        path = nx.shortest_path(graph, first, node)
        if len(path) >= 3:
            node_list.append('orange')
        if len(path) == 2:
            node_list.append('yellow')
        if len(path) == 1:
            node_list.append('r')
    
    px = nx.spring_layout(graph) #present the graph in a 'spring' layout w/wo labels
    nx.draw_networkx_nodes(graph, pos = px, node_color = [p for p in node_list], alpha = .9)
    nx.draw_networkx_edges(graph, pos = px, edge_color = 'grey', alpha = .25)
    if labels:
        nx.draw_networkx_labels(graph, pos = px)
    #nx.draw(graph, pos = px, with_labels = labels, node_color = [p for p in node_list], edge_color = 'grey')
    limits=plt.axis('off')
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

          
    
    
ng = create_network('Russell Crowe', roles = 'Actors Producers Directors', layers = 2, cut = .20)

            

