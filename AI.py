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
from time import perf_counter

class AI(Player):
    def __init__(self, id, Map, turns, time=5, threshhold=0.51):
        super(AI, self).__init__(id, Map, turns)
        self.is_ai = True
        self.time = time
        # When planning an attack, ignore attacks with success rates below threshhold
        self.threshhold = threshhold

    # This calculates the optimal placement strategy by improving the average chance of success for attacks
    # by increasing the number of troops with the lowest odds
    def placement(self):
      print("  AI Placement")
      # self.__find_wars(attack=True)
      wars = []
      for c in self.country:
        tmp = self.__find_wars(c, attack=True)
        for t in tmp:
          wars.append(t)
      #wars = self.__find_wars(attack=True)
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

    def __UCB1(self, node):
      return node.result+np.sqrt(4*np.log(node.parent.visits)/np.log(node.visits))

    # Explores the tree for MCTS
    def __tree_policy(self):
      print("  Tree Policy")
      node = self.MCTS
      while len(node.possChildren) == 0 and len(node.children) != 0:
        print("    possible children::{0}".format(len(node.possChildren)))
        bestChild = node.children[0]
        bestScore = self.__UCB1(bestChild)
        for child in node.children[1:]:
          score = self.__UCB1(child)
          if score > bestScore:
            bestScore = score
            bestChild = child
        oldNode = node
        node = bestChild
      return node

    def __expand(self, node):
      print("  In expand::{0}".format(len(node.possChildren)))
      if len(node.possChildren) != 0:
        i = random.randrange(0, len(node.possChildren), 1)
        # possChildren stores wars. This needs to be converted to a new node.
        node = node.create_child(i, link=True, thresh=self.threshhold)
      return node

    def __simulate(self, node):
      print("  In Simulate")
      while len(node.possChildren) != 0:
        i = random.randrange(0, len(node.possChildren), 1)
        node = node.create_child(i, link=False, thresh=self.threshhold)
      # Find average chance of surviving an attack
      result = 0
      count = 0
      # print("    Calculating result...")
      for c in node.countries:
        newWars = self.__find_wars(c, attack=False)
        for nw in newWars:
          count += 1
          result += nw[2]
      return result/count

    def __backtrack(self, node, result):
      print("    In backtrack")
      while node.parent:
        node.result = (node.result*node.visits+result)/(node.visits+1)
        node.visits += 1
        node = node.parent
 
    def attack(self):
      print("  Attack")
      # create list of wars from self.__find_wars(attack=True)
      self.MCTS = Node(self.map, self.country, None, thresh=self.threshhold)
      # while time:
      iterations = 0
      startTime = perf_counter()
      while perf_counter()-startTime < self.time:
        # Find current best path to explore
        node = self.__tree_policy()
        # Create new child
        node = self.__expand(node)
        # Simulate rest of attack sequence
        result = self.__simulate(node)
        # backtrack
        self.__backtrack(node, result)
        iterations += 1

      # return path
      path = []
      node = self.MCTS
      print("    Picking Best path...")
      print("    number of children::{0}".format(len(node.children)))
      while len(node.children) != 0:
        score = 0
        bestChild = None
        for child in node.children:
          tmpScore = child.result
          if score < tmpScore:
            score = tmpScore
            bestChild = child
          print("  best score::{0} move::{1}::{2}".format(score, bestChild.move[0].name, bestChild.move[1].name))
        path.append(bestChild.move)
        node = bestChild
       

      self.MCTS = None
      print("  AI attack took {0} iterations".format(iterations))
      return path

    def deplacement(self):
      print("  AI deplacement")
      # Find wars and success rates
      wars = []
      for c in self.country:
        tmp = self.__find_wars(c, attack=False)
        for t in tmp:
          wars.append(t)
      # wars = self.__find_wars(attack=False)
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
    # or defence (if false) for a country
    def __find_wars(self, c, attack=True):
      wars = []
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

    def __find_wars_attack(self):
      wars = self.__find_wars(attack=True)
      remove = []
      # trim wars based on threshhold
      for i in range(0, len(wars)):
        if war[i][2] < self.threshhold:
          remove.append(i)
      for i in remove[::-1]:
        del wars[i]
      return wars

    def __find_country(self, countryID):
      return next((p for p in self.map.country if p.id == countryID), None)

class Node():
  def __init__(self, Map, countries, move, thresh):
    print("  In Node Init")
    # List of Nodes
    self.children = []
    self.parent = None
    self.visits = 0
    # The result to be backtracked is the average chance of success defending an attack
    self.result = 0
    self.map = copy.deepcopy(Map)
    self.countries = copy.deepcopy(countries)
    # The war which created this node
    # (our country, enemy country, attack success rate)
    self.move = move
    if move:
      #print("    move::{0}::{1}::{2}::{3}".format(move[0].name, move[0].nb_troops, move[1].name, move[1].nb_troops))
      # initiate move
      atkCountry = self.__find_country(move[0].id)
      newCountry = self.__find_country(move[1].id)
      wmc = War_MC(atkCountry.nb_troops-1, newCountry.nb_troops)
      #print("    Number of atk lost {0}, number of Def lost {1}".format(wmc.expected_loss_atk(), wmc.expected_loss_def()))
      dedAtkrs = int(round(wmc.expected_loss_atk()))
      if dedAtkrs > atkCountry.nb_troops:
       raise ValueError("ERROR::ATTACKING COUNTRY LOST {0} TROOPS BUT ONLY HAD {1}".format(dedAtkrs, atkCountry.nb_troops))
      atkCountry.nb_troops -= dedAtkrs
      newCountry.nb_troops = atkCountry.nb_troops-1
      atkCountry.nb_troops = 1
      newCountry.id_player = atkCountry.id_player
      self.countries.append(newCountry.id)
    # List of (our country, enemy country, attack success rate)
    wars = []
    #print("    # of countries::{0}".format(len(self.countries)))
    for c in self.countries:
      tmp = self.__find_wars(c, attack=True)
      for t in tmp:
        wars.append(t)
    #print("    Init # of wars::{0}".format(len(wars)))
    remove = []
    for i in range(0, len(wars)):
      #print("      {0}::{1}::{2}".format(wars[i][0].name, wars[i][1].name, wars[i][2]))
      if wars[i][2] < thresh:
        remove.append(i)
    for i in remove[::-1]:
      del wars[i]
    #print("    Final # of wars::{0}".format(len(wars)))
    self.possChildren = wars
    #print("    Final # of wars::{0}".format(len(self.possChildren)))

  def create_child(self, i, thresh, link=False):
    #print("    in create_child::{0}".format(link))
    newNode = Node(self.map, self.countries, self.possChildren.pop(i), thresh)
    if link:
      newNode.parent = self
      self.children.append(newNode)
    return newNode
    
  # Find list of possible wars and their chances of success for attack (if true)
  # or defence (if false) for a country
  def __find_wars(self, c, attack=True):
    wars = []
    # For each country:
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
