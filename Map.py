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
            self.continents.append(Continent(['Congo','East Africa','Egypt','Madagascar','North Africa','South Africa']
                                            ,3,'Africa',self))
            self.continents.append(Continent(['Alaska','Alberta','Central America','Eastern States','Greenland','North-West Territories','Ontario','Quebec','Western States']
                                            ,5,'North America',self))
            self.continents.append(Continent(['Venezuela','Brazil','Peru','Argentina']
                                            ,2,'South America',self))
            self.continents.append(Continent(['Afghanistan','China','India','Irkutsk','Japan','Kamchatka','Middle East','Mongolia','Siam','Siberia','Urals','Yakutia']
                                            ,7,'Asia',self))
            self.continents.append(Continent(['Great Britian','Iceland','Northern Europe','Scandinavia','Southern Europe','Ukraine','Western Europe']
                                            ,5,'Europe',self))
            self.continents.append(Continent(['East Australia','Indonesia','New Guinea','West Australia']
                                            ,2,'Oceanic',self))
            self.continents[0].country[0].neighbor=[2,5,6]
            self.continents[0].country[1].neighbor=[1,3,4,5,26]
            self.continents[0].country[2].neighbor=[2,5,36,26]
            self.continents[0].country[3].neighbor=[2,6]
            self.continents[0].country[4].neighbor=[1,2,3,17,36,38]
            self.continents[0].country[5].neighbor=[1,2,4]
            self.continents[1].country[0].neighbor=[8,12,25]
            self.continents[1].country[1].neighbor=[7,12,13,15]
            self.continents[1].country[2].neighbor=[15,10,19] # Central
            self.continents[1].country[3].neighbor=[9,15,13,14] # 10?
            self.continents[1].country[4].neighbor=[12,13,14,33]
            self.continents[1].country[5].neighbor=[7,8,13,11]
            self.continents[1].country[6].neighbor=[8,15,10,14,11,12]
            self.continents[1].country[7].neighbor=[10,13,11]
            self.continents[1].country[8].neighbor=[9,10,8,13,12]
            self.continents[2].country[0].neighbor=[17,18]
            self.continents[2].country[1].neighbor=[16,18,19,5]
            self.continents[2].country[2].neighbor=[16,17,19]
            self.continents[2].country[3].neighbor=[18,17,9] # Argentine
            self.continents[3].country[0].neighbor=[21,22,26,30,37] # 20
            self.continents[3].country[1].neighbor=[20,22,28,27,29,30]
            self.continents[3].country[2].neighbor=[20,21,26,28]
            self.continents[3].country[3].neighbor=[29,27,25,31]
            self.continents[3].country[4].neighbor=[27,25]
            self.continents[3].country[5].neighbor=[31,23,27,24,7]
            self.continents[3].country[6].neighbor=[20,22,37,2,3]
            self.continents[3].country[7].neighbor=[24,21,29,25,23]
            self.continents[3].country[8].neighbor=[21,22,40]
            self.continents[3].country[9].neighbor=[30,21,23,31,27]
            self.continents[3].country[10].neighbor=[20,21,29,37] # 30
            self.continents[3].country[11].neighbor=[29,23,25]
            self.continents[4].country[0].neighbor=[33,35,34,38]
            self.continents[4].country[1].neighbor=[32,35,11]
            self.continents[4].country[2].neighbor=[32,35,37,36,38]
            self.continents[4].country[3].neighbor=[37,32,33,34]
            self.continents[4].country[4].neighbor=[38,34,37,3,26,5]
            self.continents[4].country[5].neighbor=[35,34,36,20,26,30]
            self.continents[4].country[6].neighbor=[32,34,36,5]
            self.continents[5].country[0].neighbor=[42,41]
            self.continents[5].country[1].neighbor=[42,41,28] # 40
            self.continents[5].country[2].neighbor=[42,40,39]
            self.continents[5].country[3].neighbor=[39,41,40]

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
