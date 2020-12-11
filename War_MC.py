#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

"""
This file manages the probabilistic nature of the wars fought in Risk.
"""

import numpy as np
import pandas as pd
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
    # Configure MC
    self.__cal_states()
    self.__cal_mx()
    self.__cal_p()

  def get_data(self):
    print('Test("%s","%s","%s")' % (self.q, self.r, self.F ))

  # create list of transition states and absorbing states.
  def __cal_states(self):
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

  # Create matrix Q, R, I, and F
  def __cal_mx(self): 
    self.q = self.__cal_prob(self.t_states, self.t_states)
    self.r = self.__cal_prob(self.t_states, self.ab_states)
    self.i = np.eye(len(self.t_states))
    self.F = pd.DataFrame(np.matmul(np.linalg.inv(self.i-self.q.values), self.r),
                          columns = self.ab_states, index=self.t_states)

  # Calculate proability that the attacker wins
  def __cal_p(self):
    if self.attacker == 0:
      self.p = 0.0
    else:
      self.p = sum(self.F.iloc[self.attacker*self.defender-1]
                   [len(self.F.iloc[self.attacker*self.defender-1])-self.attacker:])
    
  # number of lossing attacker and defender from each states to absorbing states
  def __losses(self):
    l = [] 
    for (x,y) in self.ab_states:
      l.append((self.attacker-x, self.defender-y))
    return l

  # Calculate the expected of lossing defender.
  def expected_loss_def(self):
    if self.attacker>0:
      d_l = []
      for (x,y) in self.__losses():
        d_l.append(y)
      pb = list(self.F.iloc[self.attacker*self.defender-1])
      return np.dot(d_l,pb)
    else:
      return 0

  # Calculate the expected of lossing attacker
  def expected_loss_atk(self):
    if self.attacker>0:
      d_l = []
      for (x,y) in self.__losses():
        d_l.append(x)
      pb = list(self.F.iloc[self.attacker*self.defender-1])
      return np.dot(d_l,pb)
    else:
      return 0

  # Creates transition matrix
  def __cal_prob(self, states1, states2):
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
