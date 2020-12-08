#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

"""
This file manages the probabilistic nature of the wars fought in Risk.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import random as rm

class War_MC():
  def __init__(self, a = 0, d = 0):
    self.attacker = a # number of attacker
    self.defender = d # number of defneder
    self.t_states = [] # transition states
    self.ab_states = [] # absorbing states
    self.q = [] # matrix Q
    self.r = [] # matrix R
    self.F = [] # matrix F = (I-Q)^-1 *R
    self.i = [] # Identity matrix
    self.p = 0 # probaility that the attacker wins
    self.l = [] # number of lossing attacker and defender from each states 
                # to absorbing states
    self.EdefL = 0 # Expected number of lossing defenders
    self.EatkL = 0 # Expected number of lossing attackers

  def get_data(self):
    print('Test("%s","%s","%s")' % (self.q, self.r, self.F ))

  # create list of transition states and absorbing states.
  def cal_states(self):
    def_arr = np.arange(self.defender+1)
    atk_arr = np.arange(self.attacker+1)
    states_arr = list(itertools.product(atk_arr, def_arr))
    for (a,b) in states_arr:
      if a == 0 and b >=1:
        self.ab_states.append((a, b))
      elif a>=1 and b == 0:
        self.ab_states.append((a, b))
      elif a >= 1 and b>=1:
        self.t_states.append((a, b))

  # Create matrix Q, R, I and F
  def cal_mx(self): 
    self.q = self.__cal_prob(self.t_states, self.t_states)
    self.r = self.__cal_prob(self.t_states, self.ab_states)
    self.i = np.eye(len(self.t_states))
    self.F = pd.DataFrame(np.matmul(np.linalg.inv(self.i-self.q.values), self.r ),
                          columns = self.ab_states, index=self.t_states)

  # Calculate proability that the attakcer wins
  def cal_p(self):
    self.p = sum(self.F.iloc[self.attacker*self.defender-1]
                 [len(self.F.iloc[self.attacker*self.defender-1])-self.attacker:])
    
  def losses(self): 
    for (x,y) in self.ab_states:
      self.l.append((self.attacker-x, self.defender-y))

  # Calculate the expected of lossing defender.
  def e_def_loss(self):
      d_l = []
      for (x,y) in self.l:
        d_l.append(y)
      pb = list(self.F.iloc[self.attacker*self.defender-1])
      self.EdefL = np.dot(d_l,pb)

  # Calculate the expected fo lossing attacker
  def e_atk_loss(self):
    d_l = []
    for (x,y) in self.l:
       d_l.append(x)
    pb = list(self.F.iloc[self.attacker*self.defender-1])
    self.EatkL = np.dot(d_l,pb)

  # Creates transition matrix
  def __cal_prob(states1, states2):
    prob = []
    for (a,b) in states1:
     for (c,d) in states2:
       if a>=3 and b>=2:
         if a-c==2 and b-d==0:
          prob.append(0.293)
         elif a-c==0 and b-d ==2:
          prob.append(0.372)
         elif a-c==1 and b-d ==1:
          prob.append(0.336)
         else:
          prob.append(0)
       elif a >= 3 and b==1:
         if a-c==1 and b-d == 0:
          prob.append(0.34)
         elif a-c==0 and b-d ==1:
          prob.append(0.66)
         else:
          prob.append(0)
       elif a== 2 and b >=2:
         if a-c==2 and b-d==0:
          prob.append(0.448)
         elif a-c==0 and b-d ==2:
          prob.append(0.228)
         elif a-c==1 and b-d ==1:
          prob.append(0.324)
         else:
          prob.append(0)
       elif a==2 and b==1:
          if a-c==1 and b-d == 0:
           prob.append(0.421)
          elif a-c==0 and b-d ==1:
           prob.append(0.579)
          else:
           prob.append(0)
       elif a==1 and b>=2:
          if a-c==1 and b-d == 0:
           prob.append(0.745)
          elif a-c==0 and b-d ==1:
           prob.append(0.255)
          else:
           prob.append(0)
       elif a==1 and b==1:
          if a-c==1 and b-d == 0:
           prob.append(0.583)
          elif a-c==0 and b-d ==1:
           prob.append(0.417)
          else:
           prob.append(0)
       else:
         prob.append(0)
   
    return pd.DataFrame(np.reshape(prob, (len(states1),len(states2))), 
                        columns= states2, index = states1)

  # Dont know if this is neccessary
  def do(self):
    x.cal_states()
    x.cal_mx()
    x.losses()
    x.e_def_loss()
    x.e_atk_loss()