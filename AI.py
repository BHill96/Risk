#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

"""
This file manages the AI's actions for the game.
"""

import random
import copy
from Player import *

class AI(Player):
    def __init__(self,id,Map,turns):
        super(AI, self).__init__(id,Map,turns)
        self.is_ai=True

    # This calculates the optimal placement strategy by improving the average chance of success for attacks
    # by increasing the number of troops with the lowest odds
    def placement(self):
      # self.__find_wars(attack=True)
      wars = self.__find_wars(attack=True)
      wars = sorted(wars, key=lambda war:war[2])
      # While reinforcments > 0:
      troops = self.nb_troops
      # Dict of country name:troops to add
      reinforce = {}
      while troops > 0:
        # Add troop to country with lowest chance
        if wars[0][0].id != reinforce.keys():
          reinforce[wars[0][0].id] = 0
        reinforce[wars[0][0].id] += 1
        print("Added 1 to {0}".format(wars[0][0].name))
        troops -= 1
        # Recalculate odds and re-sort
        wars[0] = (wars[0][0], wars[0][1], wars[0][2]+0.01)
        wars = sorted(wars, key=lambda war:war[2])
      # Return dict of (country, reinforcment) pairs
      return reinforce

    def attack(self):
      """
      create list of wars from self.__find_wars(attack=True)
      while time:
        remove wars with low success rates
        Use UCB1 to select a path leading to new node
        ** We can copy the origional list, 
           remove the war which just happened, 
           Add wars with new neighbors **
        simulate rest of wars until no good success rates
        backtrack
      return path
      ** should terminate early if a battle is lost in actual game
      """

    def deplacement(self):
      """
      self.__find_wars(attack=False)
      Find country with highest and lowest chances
      Split reinforcments between the two
      Return pair of (country, reinforcments) pairs
      """

    # Find list of possible wars and their chances of success for attack (if true)
    # or defence (if false)
    def __find_wars(self, attack=True):
      wars = []
      # For each country:
      for c in self.country:
        country=self.__find_country(c)
        print(country.name)
        # For each enemy neighbor:
        for n in country.neighbor:
          neighbor=self.__find_country(n)
          if country.id_player != neighbor.id_player:
            # Find chance of winning war
            success_chance = random.uniform(0,1)
            # save (neighbor, chance of success)
            print("  {2}::{0}::{1}".format(neighbor.name, success_chance, n))
            wars.append((country, neighbor, success_chance))
      # return list of pairs
      return wars

    def __find_country(self, countryID):
      return next((p for p in self.map.country if p.id == countryID), None)
