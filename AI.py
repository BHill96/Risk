#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

"""
This file manages the AI's actions for the game.
"""

import random
import copy
from Player import *
from Map import *
from War_MC import *

class AI(Player):
    def __init__(self,id,Map,turns):
        super(AI, self).__init__(id,Map,turns)
        self.is_ai=True

    # This calculates the optimal placement strategy by improving the average chance of success for attacks
    # by increasing the number of troops with the lowest odds
    def placement(self):
      print("  AI Placement")
      # self.__find_wars(attack=True)
      wars = self.__find_wars(attack=True)
      wars = sorted(wars, key=lambda war:war[2])
      # While reinforcments > 0:
      troops = self.nb_troops
      # Dict of country name:troops to add
      reinforce = {}
      while troops > 0:
        # For debugging
        #self.__print_wars(wars)
        # Add troop to country with lowest chance
        if wars[0][0].id not in reinforce.keys():
          reinforce[wars[0][0].id] = 0
        reinforce[wars[0][0].id] += 1
        troops -= 1
        # Recalculate odds and re-sort
        wmc = War_MC(wars[0][0].nb_troops+reinforce[wars[0][0].id]-1, wars[0][1].nb_troops)
        wars[0] = (wars[0][0], wars[0][1], wmc.p)
        wars = sorted(wars, key=lambda war:war[2])
      # Return dict of (country, reinforcment) pairs
      print("Reinforcing")
      for k in reinforce.keys():
        print("  {0}::{1}".format(self.__find_country(k).name, reinforce[k]))
      return reinforce

    # for debugging
    def __print_wars(self, wars):
      print("    Wars:")
      for w in wars:
        print("      {0}, {1}, {2}".format(w[0].name, w[1].name, w[2]))

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
      print("  AI deplacement")
      # Find wars and success rates
      wars = self.__find_wars(attack=False)
      wars = sorted(wars, key=lambda war:war[2])
      # Find possible paths within contiguous territory 
      paths = self.__find_deplacement_paths()
      print("Paths:",paths)
      # Find possible deplacement based on most secure country
      tmp1 = []
      for path in paths:
        if wars[-1][0].id in path:
          for war in wars[:len(wars)-1]:
            if war[0].id in path and war[0].id != wars[-1][0].id:
              tmp1 = [wars[-1], war]
              break
      if tmp1:
        gap1 = tmp1[0][2]-tmp1[1][2]
      else:
        gap1 = -1
      # Find possible deplacement based on least secure country
      tmp2 = []
      for path in paths:
        if wars[0][0].id in path:
          for war in wars[0:]:
            if war[0].id in path and war[0].id != wars[0][0].id:
              tmp2 = [wars[0], war]
              break
      if tmp2:
        gap2 = tmp2[1][2]-tmp2[0][2]
      else:
        gap2 = -1
      # Find best deplacement by picking largest success difference
      if gap2 > gap1:
        high = tmp2[1]
        low = tmp2[0]
      elif gap2 < gap1:
        high = tmp1[0]
        low = tmp1[1]
      else:
        # No need to displace troops
        return (None, None, -1)
      # Begin moving troops until success is about equal
      newGap = high[0].nb_troops-1
      amount = 0
      while newGap > 0:
        lowWmc = War_MC(low[1].nb_troops-1, low[0].nb_troops+amount)
        highWmc = War_MC(high[1].nb_troops-1, high[0].nb_troops-amount)
        newGap = highWmc.p - lowWmc.p
        amount += 1
        if amount >= high[0].nb_troops-1:
          amount = high[0].nb_troops-1
          break
      return (high[0].id, low[0].id, amount)

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
          if len(tmp) > 1:
            reachable.append(tmp)
      return reachable

    # Find list of possible wars and their chances of success for attack (if true)
    # or defence (if false)
    def __find_wars(self, attack=True):
      wars = []
      # For each country:
      for c in self.country:
        country = self.__find_country(c)
        # For each enemy neighbor:
        for n in country.neighbor:
          neighbor = self.__find_country(n)
          if country.id_player != neighbor.id_player:
            # Find chance of winning war
            if attack:
              # Success based on attack
              wmc = War_MC(country.nb_troops-1, neighbor.nb_troops)
              success_chance = wmc.p
            else:
              # Success based on defense
              wmc = War_MC(neighbor.nb_troops-1, country.nb_troops)
              success_chance = 1-wmc.p
            # save (neighbor, chance of success)
            wars.append((country, neighbor, success_chance))
      # return list of pairs
      return wars

    def __find_country(self, countryID):
      return next((p for p in self.map.country if p.id == countryID), None)
