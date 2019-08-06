#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:10:06 2019

@author: RyanAlco
"""


#from imdb import IMDb

import requests
#from ProjectClassSol import project

class person(object):
    
    ''' A person object is initiated from someone's name(including what they are known for if
    multiple people share the same name) or someone's TMDB id. For each person, their primary
    role is obtained(actor/crew) and then their 'good' projects are found based on a TMDB rating.
    Id's and URLs are used to gather data from TMDB's API
    '''
    
    def __init__(self, name = '', known_for = False, idnum = False):
        self.known_for = known_for
        self.name = name
        self.personURL = 'https://api.themoviedb.org/3/search/person?api_key=e448a896945245426e4dece19f7aeca8&query='+name   
        if (idnum):
            self.id = idnum
            IDURL = 'http://api.themoviedb.org/3/person/'+self.id+'?api_key=e448a896945245426e4dece19f7aeca8'
            payload = "{}"
            response = requests.request("GET", IDURL, data=payload)
            data = response.json()
            self.name = data['name']
        if (not idnum):
            self.get_id()
        self.id
        self.idURL = 'https://api.themoviedb.org/3/person/'+self.id+'/combined_credits?api_key=e448a896945245426e4dece19f7aeca8'
        #'https://api.themoviedb.org/3/person/'+self.id+'/credits?api_key=e448a896945245426e4dece19f7aeca8'     
        self.generalURL = 'https://api.themoviedb.org/3/person/'+self.id+'?api_key=e448a896945245426e4dece19f7aeca8'
        self.get_role()
        self.role
        self.project_dic = {}
        self.set_projects()
        
    def get_id(self):
        payload = "{}"
        response = requests.request("GET", self.personURL, data=payload)
        data = response.json()   
        if (self.known_for != False):
            switch = True
            out = 0
            while switch:
                size = len(data['results'][out]['known_for'])
                inside = 0
                while (inside < size) and (switch):
                    if self.known_for in data['results'][out]['known_for'][inside].values():
                        self.id = str(data['results'][out]['id'])
                        switch = False
                    inside += 1
                out += 1
            
        else: 
            try:#[0]['id']):
                (data['results'])
                self.id = str(data['results'][0]['id'])
            except:
                self.id = ''
                
        
    def get_role(self):
        payload = "{}"
        response = requests.request("GET", self.generalURL, data=payload)
        data = response.json()
        self.role = data['known_for_department']
    
    def set_projects(self):
        #change here to make it not have to do with what the role is
        payload = "{}"
        response = requests.request("GET", self.idURL, data=payload)
        data = response.json()
        if self.role != 'Acting':
            for proj in data['crew']:
                if (proj['vote_average'] >= 6.0) and (proj['vote_count'] >= 300):
                    self.project_dic[str(proj['id'])] = [proj['original_title'], proj['vote_average'], proj['media_type']]
        if self.role == 'Acting':
            for proj in data['cast']:
                if (proj['vote_average'] >= 6.0) and (proj['vote_count'] >= 300):
                    if proj['media_type'] == 'movie':
                        self.project_dic[str(proj['id'])] = [proj['original_title'], proj['vote_average'], proj['media_type']]
                    if proj['media_type'] == 'tv':
                        self.project_dic[str(proj['id'])] = [proj['original_name'], proj['vote_average'], proj['media_type']]
        
    def get_projects(self):
        return self.project_dic
    '''
    def get_good_projects(self):
        good_project_dic = {}
        if self.project_dic != {}:
            for proj in self.project_dic.values():
                url = 'https://api.themoviedb.org/3/search/multi?api_key=e448a896945245426e4dece19f7aeca8&query='+proj
                #url = 'https://api.themoviedb.org/3/movie/'+proj+'?api_key=e448a896945245426e4dece19f7aeca8'
                payload = "{}"
                response = requests.request("GET", url, data=payload)
                data = response.json()
                
                try:
                    if (data['vote_average'] >= 6.0) and (data['vote_count'] >= 300):
                        good_project_dic[proj] = self.project_dic[proj]
                except:
                    print(proj)
                
                
                try: 
                    (data['results'])
                    if (data['results'][0]['vote_average'] >= 6.0) and (data['results'][0]['vote_count'] >= 300):
                        good_project_dic[proj] = self.project_dic[proj]
                except:
                    pass
        
        return good_project_dic
        '''
    

#BP = person('Daniel Kaluuya')
#projects = BP.get_projects()        


           



