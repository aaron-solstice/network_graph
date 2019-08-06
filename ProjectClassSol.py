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
    
    ''' Initializes a project object from the project title, which contains various pieces of info about a project(movie/tv)
    that a person has been involved in. A rating of the project is gathered in order to filter
    the number of projects returned for a person. The cast of the project is also gathered with a
    'cut' value to determine which portion of the acting cast to include in the network. Various 
    id's are included with different calls to the TMDB API in order to find all of this info based 
    off of only the title of a project
    '''
    
    def __init__(self, idnum, media_type, cut = 0):
        self.id = idnum
        #self.title = title
        self.cut = cut
        #self.multi_url = 'https://api.themoviedb.org/3/search/multi?api_key=e448a896945245426e4dece19f7aeca8&query='+self.title
        #self.find_id()
        self.multi_type = media_type
        
        self.talent = {}
        #self.rating = 0
        #self.find_rating()
        self.find_cast()
    '''    
    def find_id(self):
        payload = "{}"
        response = requests.request("GET", self.multi_url, data=payload)
        data = response.json()
        self.id = str(data['results'][0]['id'])
        self.multi_type = data['results'][0]['media_type']
    '''
    
    def find_cast(self):
        
        if self.multi_type == 'movie':
            cast_url = 'https://api.themoviedb.org/3/movie/'+self.id+'/credits?api_key=e448a896945245426e4dece19f7aeca8'
        if self.multi_type == 'tv':
            cast_url = 'https://api.themoviedb.org/3/tv/'+self.id+'/credits?api_key=e448a896945245426e4dece19f7aeca8'
        #keep this in case find way to incorporate tv
        payload = "{}"
        response = requests.request("GET", cast_url, data=payload)
        data = response.json()

        actors = []
        producers = []
        directors = []
        writers = []
        if self.cut:
            for person in data['cast'][:int(len(data['cast'])*self.cut)]:
                actors.append(str(person['id']))
        else:
            for person in data['cast']:
                actors.append(person['id'])
    
        for person in data['crew']:
            if person['department'] == 'Production':
                producers.append(str(person['id']))
        
        for person in data['crew']:
            if person['department'] == 'Directing':
                directors.append(str(person['id']))
        
        for person in data['crew']:
            if person['department'] == 'Writing':
                writers.append(str(person['id']))
            
        self.talent['Actor'] = actors
        self.talent['Director'] = directors
        self.talent['Producer'] = producers
        self.talent['Writer'] = writers
    '''    
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
    '''
'''    
    def get_people(self):
        return self.talent
    
    def get_rating(self):
        return self.rating 
'''

#madMax = project('419430', media_type = 'movie', cut = .25)
'''
print madMax.get_people()
print madMax.get_rating()
'''






