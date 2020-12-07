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
      self.__find_wars(attack=True)
      """
      While reinforcments > 0:
        Add troop to country with lowest chance 
        Recalculate odds and re-sort
      Return list of (country, reinforcment) pairs?
      """

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
      # For each country:
      for c in self.country:
        print(c)
        # For each enemy neighbor:
          # save (neighbor, chance of success)
      # return list of pairs
