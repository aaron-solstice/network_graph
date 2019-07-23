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
import requests

'''  
class Grapher(object):
    def __init__(self, name = '', known_for = False, idnum = False, layers = 0, connections_only = False, people_pop = False):
        self.name = name
        self.known_for = known_for
        self.idnum = idnum
        self.layers = layers
        self.connections_only = connections_only
        self.people_pop = people_pop
        self.best_projs
        self.G = nx.Graph()
        self.get_best()
      
    def get_best(self):
        #put this in the person class
        talent = person(self.name, self.known_for, self.idnum)
        projects = talent.get_projects()
        good = []
        for proj in projects:
            url = 'https://api.themoviedb.org/3/search/multi?api_key=e448a896945245426e4dece19f7aeca8&query='+proj
            payload = "{}"
            response = requests.request("GET", url, data=payload)
            data = response.json()
            if (data['results'][0]['vote_average'] >= 6.0) and (data['results'][0]['vote_count'] >= 300):
                personproj = project(proj)
                good.append(personproj)
        self.best_projs = good
        
#best = get_best(idnum = '287')
'''
'''
    def create_network(self, **kwargs):
        #best_projs = self.get_best(name, known_for, idnum) #best_projs is a list of project class objects
        for bp in self.best_projs:
            if (self.people_pop):
                ppl = bp.get_people_pop()
            else:
                ppl = bp.get_people() #ppl is a dictionary of the people and their roles in project
            for per in ppl['Actors']:
                self.G.add_node(per, Actor=bp.title)
                if layers > 1:
                    self.create_network(per = self.name, layers - 1)
            for per in ppl['Directors']:
                self.G.add_node(per, Director=bp.title)
                if layers > 1:
                    self.create_network(per, layers - 1)
            for per in ppl['Producers']:
                self.G.add_node(per, Producer=bp.title)
                if layers > 1:
                    self.create_network(per, layers - 1)
            for per in ppl['Writers']:
                self.G.add_node(per, Writer=bp.title)
                if layers > 1:
                    self.create_network(per, layers - 1)   
            for node in self.G.nodes():
                self.G.add_edge(name, node)
        
        self.G.remove_edge(name, name)
'''
Gr = nx.Graph()
   
def create_network(name = '', known_for = False, idnum = False, var1 = 'Actors', var2 = False, var3 = False, every = False, layers = 0, cut = 0):
    #print ('here1')
    talent = person(name = name, known_for = known_for, idnum = idnum)
    best_projs = talent.get_good_projects()
    
    for bp in best_projs:
        bp = project(bp, cut)
        ppl = bp.get_people()
        #print ('here')
        if 'Actors' in [var1, var2, var3]:
            for per in ppl['Actors']:
                Gr.add_node(per, Actor=bp.title)
                Gr.add_edge(talent.name, per)#, rating = bp.get_rating())
                if layers > 1:
                #print (per, ': actor ', layers)
                    create_network(name = per, var1 = var1, var2 = var2, var3 = var3, every = every, layers = layers - 1, cut = cut)
                #print (1)
        if ('Directors' in [var1, var2, var3]) or (every):        
            for per in ppl['Directors']:
                Gr.add_node(per, Director=bp.title)
                Gr.add_edge(talent.name, per)#, rating = bp.get_rating())
                if layers > 1:
                #print (per, ': director ', layers)
                    create_network(name = per, var1 = var1, var2 = var2, var3 = var3, every = every, layers = layers - 1, cut = cut)
                #print (2)
        if ('Producers' in [var1, var2, var3]) or (every):
            for per in ppl['Producers']:
                Gr.add_node(per, Producer=bp.title)
                Gr.add_edge(talent.name, per)#, rating = bp.get_rating())
                if layers > 1:
                #print (per, ': producer ', layers)
                    create_network(name = per, var1 = var1, var2 = var2, var3 = var3, every = every, layers = layers - 1, cut = cut)
                #print (3)
        if ('Writers' in [var1, var2, var3]) or (every):
            for per in ppl['Writers']:
                Gr.add_node(per, Writer=bp.title)
                Gr.add_edge(talent.name, per)#, rating = bp.get_rating())
                if layers > 1:
                #print (per, ': writer ', layers)
                    create_network(name = per, var1 = var1, var2 = var2, var3 = var3, every = every, layers = layers - 1, cut = cut)
                #print (4)
                
    return Gr
            
    
#guy = create_network(name = 'Daniel Kaluuya')
   #256 
test2 = create_network('Matt Damon', layers = 2, cut = .25)
#px = nx.spring_layout(test1)
#nx.draw(test1, pos = px, with_labels = True)
#plt.show()
    


#nx.draw_circular(test1)

#DOES NOT UPDATE NODE DICTIONARY WITH MULTIPLE MOVIES 
#Test line for Git
git = 5

             
            
#edge thickness varies depending on total rank over projects
#Figure out which characters from the cast to include ->solved
#At some point stop adding layers and start making connections for when c_o = True
#Create graph first and then visualize WITH PARAMETER
#dictionary node info ->solved
#graph by id not name -.solved
            

