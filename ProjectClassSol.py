#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:09:05 2019

@author: RyanAlco
"""


import requests

class project(object):
    
    ''' Initializes a project object from the project id number, which contains info about the cast of a project(movie/tv)
    that a person has been involved in. The cast of the project is gathered with a
    'cut' value to determine which portion of the acting cast to include in the network. Actors, directors, producers,
    and writers are the four type of people gathered from the cast.
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
        response = requests.get(cast_url)
        data = response.json()

        actors = {}
        producers = {}
        directors = {}
        writers = {}
        if self.cut:
            for person in data['cast'][:int(len(data['cast'])*self.cut)]:
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
    




