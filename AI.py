#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

"""
This file manages the AI's actions for the game.
"""

import random
import copy
from Player import *
from Map import *

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
        if wars[0][0].id not in reinforce.keys():
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
      print("AI deplacement")
      # Find wars and success rates
      wars = self.__find_wars(attack=False)
      wars = sorted(wars, key=lambda war:war[2])
      # Find possible paths within contiguous territory 
      paths = self.__find_deplacement_paths()
      print("Paths:",paths)
      return None

      """# Find country with highest and lowest chances
      high = wars[0]
      low = wars[-1]
      m = Map('Terre')
      print("deplacement", high[0].name, low[0].name)
      i = 1
      while not m.chemin_exist(self.country, high[0], low[0]) and i < len(wars):
        high = wars[i]
        i += 1
      if high[2] < threshold:
        high = wars[0]
        i = len(wars-2)
        while not m.chemin_exist(self.country, high[0], low[0]) and i > 0:
          low = wars[i]
          i -= 1

      print("Moving from {0} to {1}".format(high[0].name, low[0].name))
      # Split reinforcments between the two
      oldDiff = abs(high[2]-low[2])
      move = [high[0].id, 1, low[0].id]
      high, low = (high[0], high[1], high[2]-0.1), (low[0], low[1], low[2]+0.1)
      newDiff = abs(high[2]-low[2])
      print("  equalized odds from {0} to {1}".format(oldDiff, newDiff))
      while newDiff < oldDiff:
        oldDiff = newDiff
        move[1] += 1
        high, low = (high[0], high[1], high[2]-0.1), (low[0], low[1], low[2]+0.1)
        newDiff = abs(high[2]-low[2])
        print("  equalized odds from {0} to {1}".format(oldDiff, newDiff))
      # Return pair of (country, reinforcments) pairs
      return move"""

    # Finds paths within contiguous country groups
    def __find_deplacement_paths(self):
      reachable = []
      used = []
      for c in self.country:
        if c not in used:
          used.append(c)
          country = self.__find_country(c)
          tmp = [c]
          for n in self.country:
            if n != c and self.map.chemin_exist(self.country, country, self.__find_country(n)):
              tmp.append(n)
              used.append(n)
            else:
          if len(tmp) > 1:
            reachable.append(tmp)
      return reachable

    # Find list of possible wars and their chances of success for attack (if true)
    # or defence (if false)
    def __find_wars(self, attack=True):
      wars = []
      # For each country:
      for c in self.country:
        country=self.__find_country(c)
        # For each enemy neighbor:
        for n in country.neighbor:
          neighbor=self.__find_country(n)
          if country.id_player != neighbor.id_player:
            # Find chance of winning war
            if attack:
              # Success based on attack
              success_chance = random.uniform(0,1)
            else:
              # Success based on defense
              success_chance = random.uniform(0,1)
            # save (neighbor, chance of success)
            wars.append((country, neighbor, success_chance))
      # return list of pairs
      return wars

    def __find_country(self, countryID):
      return next((p for p in self.map.country if p.id == countryID), None)
