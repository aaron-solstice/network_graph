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
        self.cut = cut
        self.multi_type = media_type
        self.talent = {}
        self.find_cast()
   
    
    def find_cast(self):
        
        if self.multi_type == 'movie':
            cast_url = 'https://api.themoviedb.org/3/movie/'+self.id+'/credits?api_key=e448a896945245426e4dece19f7aeca8'
        if self.multi_type == 'tv':
            cast_url = 'https://api.themoviedb.org/3/tv/'+self.id+'/credits?api_key=e448a896945245426e4dece19f7aeca8'
        #keep this in case find way to incorporate tv
        payload = "{}"
        response = requests.request("GET", cast_url, data=payload)
        data = response.json()

        actors = {}
        producers = {}
        directors = {}
        writers = {}
        if self.cut:
            for person in data['cast'][:int(len(data['cast'])*self.cut)]:
                #actors.append(str(person['id']))
                actors[str(person['id'])] = person['name']
        else:
            for person in data['cast']:
                actors[str(person['id'])] = person['name']
    
        for person in data['crew']:
            if person['job'] == 'Producer':
                producers[str(person['id'])] = person['name']
        
        for person in data['crew']:
            if person['job'] == 'Director':
                directors[str(person['id'])] = person['name']
        
        for person in data['crew']:
            if person['department'] == 'Writing':
                writers[str(person['id'])] = person['name']
            
        self.talent['Actor'] = actors
        self.talent['Director'] = directors
        self.talent['Producer'] = producers
        self.talent['Writer'] = writers
    

#mov = project('82390', media_type = 'movie', cut = .25)
'''
print madMax.get_people()
print madMax.get_rating()
'''






