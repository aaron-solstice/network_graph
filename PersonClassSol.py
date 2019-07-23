#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:10:06 2019

@author: RyanAlco
"""


#from imdb import IMDb

import requests
from ProjectClassSol import project

class person(object):
    
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
        self.idURL = 'https://api.themoviedb.org/3/person/'+self.id+'/credits?api_key=e448a896945245426e4dece19f7aeca8'     
        self.generalURL = 'https://api.themoviedb.org/3/person/'+self.id+'?api_key=e448a896945245426e4dece19f7aeca8'
        self.get_role()
        self.role
        self.project_list = []
        self.good_project_list = []
        self.set_projects()
        
    def get_id(self):
        payload = "{}"
        response = requests.request("GET", self.personURL, data=payload)
        data = response.json()   
        if (self.known_for != False):
            switch = True
            i = 0
            while switch:
                for curr in data['results'][i].values():
                    if type(curr) == list:
                        l = curr
                #print (l)
                if self.known_for in l[0].values():
                    self.id = str(data['results'][i]['id'])
                    switch = False
                    #print ('here')
                i += 1
                #print (i)
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
        payload = "{}"
        response = requests.request("GET", self.idURL, data=payload)
        data = response.json()
        if self.role != 'Acting':
            for proj in data['crew']:
                self.project_list.append(proj['original_title'])
        if self.role == 'Acting':
            for proj in data['cast']:
                self.project_list.append(proj['original_title'])            
        
    def get_projects(self):
        return self.project_list
    
    def get_good_projects(self):
        if self.project_list == []:
            self.good_project_list = []
        else:
            for proj in self.project_list:
                '''
                proj1 = project(proj)
                if proj1.get_rating() > 7.0:
                    self.good_project_list.append(proj)
                '''
                url = 'https://api.themoviedb.org/3/search/multi?api_key=e448a896945245426e4dece19f7aeca8&query='+proj
                payload = "{}"
                response = requests.request("GET", url, data=payload)
                data = response.json()
                try: 
                    (data['results'])
                    if (data['results'][0]['vote_average'] >= 7.0) and (data['results'][0]['vote_count'] >= 300):
                        self.good_project_list.append(proj)
                except:
                    pass
                
                    
        return self.good_project_list
        
    

#BP = person('Jonah Hill')
#projects = BP.get_projects()        

'''
good = []
for proj in projects:
    BPP = project(proj)
    #print type(BPmovie)
    if (BPP.get_rating() >= 150000000) or (BPP.get_rating() > 7 and BPP.get_rating < 15):
        good.append(BPP)
'''

           



