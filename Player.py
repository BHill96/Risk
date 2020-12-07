#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

"""
This file manages the player's portion of the game
"""

import random
import copy

class Player():
    def __init__(self,id,Map,turns):
        self.id=id
        self.nb_troops=0
        self.name=""
        self.country=[]
        self._bonus=0
        self._sbyturn=0
        self._isalive=True
        self.color=(0,0,0)
        self.map=Map
        self.turns=turns
        self.obj=None
        self.cards=[]
        self.win_land=False
        self.is_ai=False

    def use_best_cards(self):
        # TODO Prevent use if not in deployment phase
        if self.turns.list_phase[self.turns.phase]=='placement':
            nb_s=[x for x in self.cards if x.type==x.types[0]]
            nb_h=[x for x in self.cards if x.type==x.types[1]]
            nb_c=[x for x in self.cards if x.type==x.types[2]]
            if len(nb_s)>0 and len(nb_h)>0 and len(nb_c)>0: # If triple unpaired
                self.use_cards([nb_s[0],nb_h[0],nb_c[0]])
            elif len(nb_c)>2: # Artillery?
                self.use_cards([nb_c[0],nb_c[1],nb_c[2]])
            elif len(nb_h)>2: # Horsemen
                self.use_cards([nb_h[0],nb_h[1],nb_h[2]])
            elif len(nb_s)>2: # Soldiers
                self.use_cards([nb_s[0],nb_s[1],nb_s[2]])
            else: # Otherwise no combo possible
                #TODO raise
                print('No combinations possible')
        else:#TODO raise
            print('We can only position during the placement phase')

    # Take only 3 cards in input
    def use_cards(self,cards):
        # Triple
        if cards[0].type==cards[1].type and cards[1].type==cards[2].type and cards[0].type==cards[2].type:
            self.nb_troops+=cards[0].bonus
            self.cards.remove(cards[0])
            self.cards.remove(cards[1])
            self.cards.remove(cards[2])
        # Unpaired
        elif cards[0].type!=cards[1].type and cards[1].type!=cards[2].type and cards[0].type!=cards[2].type:
            self.nb_troops+=cards[0].max_bonus
            self.cards.remove(cards[0])
            self.cards.remove(cards[1])
            self.cards.remove(cards[2])

    def del_card(self,card_index):
        self.cards.pop(card_index)

    def print_carac(self):
        print(self.id,self.name,self.nb_troops,self.sbyturn,self.country)

    @property
    def sbyturn(self): # Update when called
        return max(3,len(self.country)//3+self.bonus)

    @property
    def bonus(self): # Update when called
        b=0
        for c in self.map.continents:
            player_have_cont=True
            for country in c.country:
                if country.id not in self.country:
                    player_have_cont=False
                    break
            if player_have_cont:
                b+=c.bonus
        return b

    @property
    def isalive(self):
        if len(self.country)>0:
            return True
        else:
            #TODO
            #print(self.name+" is dead")
            #self.turns.order.remove(self.id_player)
            return False
