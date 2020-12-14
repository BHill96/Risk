#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

"""
This file manages the game board
"""

class Map():
    def __init__(self,name):
        self.name=name
        self.country=[]  
        self.continents=[]
        self.nb_country=0
        if name=='Terre':
            # Label Countries by continent
            self.continents.append(Continent(['Alaska','Alberta','Central America','Eastern States','Greenland','Northwest Territories',
                                              'Ontario','Quebec','Western States'],5,'North America',self))
            self.continents.append(Continent(['Argentina','Brazil','Peru','Venezuela'],2,'South America',self))
            self.continents.append(Continent(['Great Britian','Iceland','Northern Europe','Scandinavia','Southern Europe','Ukraine',
                                              'Western Europe'],5,'Europe',self))
            self.continents.append(Continent(['Congo','East Africa','Egypt','Madagascar','North Africa','South Africa']
                                              ,3,'Africa',self))
            self.continents.append(Continent(['Afghanistan','China','India','Irkutsk','Japan','Kamchatka','Middle East','Mongolia','Siam',
                                              'Siberia','Urals','Yakutsk'],7,'Asia',self))
            self.continents.append(Continent(['East Australia','Indonesia','New Guinea','West Australia'],2,'Australia',self))
            # Create Neighbors
            self.continents[0].country[0].neighbor=[2,6,32] # N. America
            self.continents[0].country[1].neighbor=[1,6,7,9]
            self.continents[0].country[2].neighbor=[4,9,13]
            self.continents[0].country[3].neighbor=[3,7,8,9]
            self.continents[0].country[4].neighbor=[6,7,8,15]
            self.continents[0].country[5].neighbor=[1,2,5,7]
            self.continents[0].country[6].neighbor=[2,4,5,6,8,9]
            self.continents[0].country[7].neighbor=[2,5,7]
            self.continents[0].country[8].neighbor=[2,3,4,7]
            self.continents[1].country[0].neighbor=[11,12] # S. America
            self.continents[1].country[1].neighbor=[10,12,13,25]
            self.continents[1].country[2].neighbor=[10,11,13]
            self.continents[1].country[3].neighbor=[3,11,12]
            self.continents[2].country[0].neighbor=[15,16,17,20] # Europe
            self.continents[2].country[1].neighbor=[5,14,17]
            self.continents[2].country[2].neighbor=[14,17,18,19,20]
            self.continents[2].country[3].neighbor=[13,14,15,18]
            self.continents[2].country[4].neighbor=[16,19,20,23,25]
            self.continents[2].country[5].neighbor=[16,17,18,27,33,37]
            self.continents[2].country[6].neighbor=[13,15,17,25]
            self.continents[3].country[0].neighbor=[22,25,26] # Africa
            self.continents[3].country[1].neighbor=[21,23,24,25,26,33]
            self.continents[3].country[2].neighbor=[18,22,25,33]
            self.continents[3].country[3].neighbor=[22,26]
            self.continents[3].country[4].neighbor=[11,18,20,21,22,23]
            self.continents[3].country[5].neighbor=[21,22,24]
            self.continents[4].country[0].neighbor=[19,28,29,33,37] # Asia
            self.continents[4].country[1].neighbor=[27,30,32,35,36,37,38]
            self.continents[4].country[2].neighbor=[27,28,33,35]
            self.continents[4].country[3].neighbor=[32,34,36,38]
            self.continents[4].country[4].neighbor=[32,34]
            self.continents[4].country[5].neighbor=[1,30,31,34,38]
            self.continents[4].country[6].neighbor=[18,19,22,23,27,29]
            self.continents[4].country[7].neighbor=[28,30,31,32,36]
            self.continents[4].country[8].neighbor=[28,29,40]
            self.continents[4].country[9].neighbor=[28,30,34,37,38]
            self.continents[4].country[10].neighbor=[19,27,28,36]
            self.continents[4].country[11].neighbor=[30,32,36]
            self.continents[5].country[0].neighbor=[41,42] # Australia
            self.continents[5].country[1].neighbor=[35,41,42]
            self.continents[5].country[2].neighbor=[39,40,42]
            self.continents[5].country[3].neighbor=[39,40,41]

    def print_country(self):
        for country in self.country:
            country.print_carac()

    def chemin_exist(self,country_player,country1,country2):
        country_reachable=[]
        if country1.id in country_player:
            country_reachable.append(country1.id)
            self.path_length(country1,country_player,country_reachable)
            if country2.id in country_reachable:
                return True
            else:
                return False
        else:
            print('The countryn\' is not the player')
            return False

    def path_length(self,country,country_player,country_reachable):
        for p_id in country.neighbor:
            if p_id in country_player and p_id not in country_reachable:
                country_reachable.append(p_id)
                self.path_length(self.country[p_id-1],country_player,country_reachable)

# Manages group of countries
class Continent():
    def __init__(self,country,bonus,name,Map):
        self.bonus=bonus
        self.name=name
        self.country=[]
        for p in country:
            P=Country(p,name,Map)
            self.country.append(P)
            Map.country.append(P)
        self.nb_country=len(self.country)

# Manages a country
class Country():
    def __init__(self,name,continent,Map):
        Map.nb_country=Map.nb_country+1
        self.id=Map.nb_country
        self.name=name
        self.continent=continent
        self.id_player=0
        self.nb_troops=0
        self.neighbor=[]

    def neighbor(self,country):
        for p in country:
            self.neighbor.append(p)

    def print_carac(self):
        print(self.id,self.name,self.continent,self.id_player,self.nb_troops,self.neighbor)
