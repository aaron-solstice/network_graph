#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:09:05 2019

@author: RyanAlco
"""

#import json
#from imdb import IMDb

import requests

class project(object):
    
    def __init__(self, title, cut = 0):
        self.title = title
        self.cut = cut
        self.multi_url = 'https://api.themoviedb.org/3/search/multi?api_key=e448a896945245426e4dece19f7aeca8&query='+self.title
        self.find_id()
        self.multi_type
        self.id
        self.talent = {}
        self.rating = 0
        self.find_rating()
        self.find_cast()
        #make a function to return only the relevant actors 
        #self.people_pop()
        
    def find_id(self):
        payload = "{}"
        response = requests.request("GET", self.multi_url, data=payload)
        data = response.json()
        self.id = str(data['results'][0]['id'])
        self.multi_type = data['results'][0]['media_type']
    
    def find_cast(self):
        if self.multi_type == 'movie':
            cast_url = 'https://api.themoviedb.org/3/movie/'+self.id+'/credits?api_key=e448a896945245426e4dece19f7aeca8'
        if self.multi_type == 'tv':
            cast_url = 'https://api.themoviedb.org/3/tv/'+self.id+'/credits?api_key=e448a896945245426e4dece19f7aeca8'
        
        payload = "{}"
        response = requests.request("GET", cast_url, data=payload)
        data = response.json()

        actors = set()
        producers = set()
        directors = set()
        writers = set()
        if self.cut:
            for person in data['cast'][:int(len(data['cast'])*self.cut)]:
                actors.add(person['name'])
        else:
            for person in data['cast']:
                actors.add(person['name'])
    
        for person in data['crew']:
            if person['department'] == 'Production':
                producers.add(person['name'])
        
        for person in data['crew']:
            if person['department'] == 'Directing':
                directors.add(person['name'])
        
        for person in data['crew']:
            if person['department'] == 'Writing':
                writers.add(person['name'])
            
        self.talent['Actor'] = list(actors)
        self.talent['Director'] = list(directors)
        self.talent['Producer'] = list(producers)
        self.talent['Writer'] = list(writers)
        
    def find_rating(self):
        if self.multi_type == 'movie':
            box_url = 'https://api.themoviedb.org/3/movie/'+self.id+'?api_key=e448a896945245426e4dece19f7aeca8'
            payload = "{}"
            response = requests.request("GET", box_url, data=payload)
            data = response.json()
            self.rating = data['revenue']
            
        if self.multi_type == 'tv':
            box_url = 'https://api.themoviedb.org/3/tv/'+self.id+'?api_key=e448a896945245426e4dece19f7aeca8'
            payload = "{}"
            response = requests.request("GET", box_url, data=payload)
            data = response.json()
            self.rating = data['vote_average']
        
    def get_people(self):
        return self.talent
    
    def get_rating(self):
        return self.rating 


madMax = project('Mad Max Fury Road', cut = .25)
'''
print madMax.get_people()
print madMax.get_rating()
'''

#Pseudocode for graph created through movie path
'''
for movie in movie_list:
    for person in movie:
        if person node does not exist:
            add person node with info about job{movie: role}
        if person does exist:
            add to person node dictionary{movie: role}
        for otherpeople in movie:
            add edge bewtween person and otherpeople with info about box office
        remove edge between person and person

'''






