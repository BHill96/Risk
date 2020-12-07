#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

"""
This file manages the various aspects of the game.
"""

import random
import copy
from AI import *
from Map import *

# Types of missions(?) players are able to perform
class Goal():
    def __init__(self,Map,turns):
        self.turns=turns
        self.types=['capture continents','capture country','destroy']
        self.map=Map
        self.randrange=[[0,1,2,3,4,5],[],[x for x in range(1,turns.nb_players+1)]]

# Define missions
class Objective():
    def __init__(self,goal,player):
        self.goal=goal
        self.type=self.goal.types[random.randint(0,len(self.goal.types)-1)]
        self.player=player
        self._description=''
        self.gen_obj()

    def gen_obj(self):
        if self.type=='capture continents':
            self.continents=[]
            self.other_cont=False
            self.nbtroops=1
            r_choice=random.choice(self.goal.randrange[0])
            self.goal.randrange[0].remove(r_choice) # Remove chosen combo to prevent duplicate missions
            if r_choice==0:
                self.continents.append(self.goal.map.continents[4])
                self.continents.append(self.goal.map.continents[5])
                self.other_cont=True
            elif r_choice==1:
                self.continents.append(self.goal.map.continents[4])
                self.continents.append(self.goal.map.continents[2])
                self.other_cont=True
            elif r_choice==2:
                self.continents.append(self.goal.map.continents[1])
                self.continents.append(self.goal.map.continents[0])
            elif r_choice==3:
                self.continents.append(self.goal.map.continents[1])
                self.continents.append(self.goal.map.continents[5])
            elif r_choice==4:
                self.continents.append(self.goal.map.continents[3])
                self.continents.append(self.goal.map.continents[2])
            elif r_choice==5:
                self.continents.append(self.goal.map.continents[3])
                self.continents.append(self.goal.map.continents[0])
        if self.type=='capture country':
            r_choice=random.randint(0,1)
            if r_choice==0:
                self.nbcountry=18
                self.nbtroops=2
            if r_choice==1:
                self.nbcountry=24
                self.nbtroops=1
        if self.type=='destroy':
            randrange_excl=copy.copy(self.goal.randrange[2])
            try:
                randrange_excl.remove(self.player.id) # Exclude himself
            except ValueError:
                pass # Player already removed from list
            if len(randrange_excl)==0:
                print('ERROR in gen_obj in Risk.py')
            try:
                randid=random.choice(randrange_excl)
                print(self.goal.randrange[2],randrange_excl,randid)
                self.goal.randrange[2].remove(randid) # Remove combination to prevent duplicate missions
                self.target=self.goal.turns.players[randid-1] 
            except IndexError: # The only attackable player is him?
                self.type=self.goal.types[random.randint(0,1)] # We choose another mission
                self.gen_obj()
            
    @property
    def description(self):
        if self.type=='capture continents':
            tmp_str='Capturer'
            for i in range(0,len(self.continents)):
                tmp_str+=' '+str(self.continents[i].name)
            if self.other_cont:
                tmp_str+=' and another cont'
            return tmp_str
        elif self.type=='capture country':
            tmp_str = 'Capturer '+str(self.nbcountry)+' country' 
            if self.nbtroops>1:
                tmp_str+=' with '+str(self.nbtroops)+' soldiers'
            return tmp_str
        elif self.type=='destroy':
            if self.target.name=='':
                return 'Destroy '+str(self.target.id)
            else:
                return 'Destroy'+str(self.target.name)

    def get_state(self):
        if self.type=='capture country':
            return self.capture_country(self.nbcountry,self.nbtroops)
        if self.type=='capture continents':
            return self.capture_continents(self.continents,self.nbtroops)
        if self.type=='destroy':
            return self.destroy_player(self.target)     

    def capture_country(self,nb_country,nb_troops):
        nb_occupied=0
        for p in self.goal.map.country:
            if p.nb_troops>nb_troops-1 and p.id_player==self.player.id:
                nb_occupied+=1
        if nb_occupied>nb_country-1:
            self.goal.turns.game_finish=True
            return True
        else:
            return False

    def capture_continents(self,continents,nb_troops):
        nb_occupied=0
        for c in continents:
            cont_occupied=True
            for p in c.country:
                if p.nb_troops<nb_troops or p.id_player!=self.player.id:
                    cont_occupied=False
            if cont_occupied==True:
                nb_occupied+=1
        if self.other_cont:
            # player must have another continent
            additionnal_cont=0
            other_conts=[x for x in self.goal.map.continents if x not in continents]
            for c in other_conts:
                cont_occupied=True
                for p in c.country:
                    if p.nb_troops<nb_troops or p.id_player!=self.player.id:
                        cont_occupied=False
                if cont_occupied==True:
                    additionnal_cont+=1
        if nb_occupied == len(continents):
            if self.other_cont and additionnal_cont>0:
                self.goal.turns.game_finish=True
                return True
            elif not self.other_cont:
                self.goal.turns.game_finish=True
                return True
            else:
                return False
        else:
            return False

    def destroy_player(self,player):
        if not player.isalive:
            self.goal.turns.game_finish=True
            return True
        else:
            return False

class Card():
    def __init__(self):
        self.types=['Soldier','Cavalier','Canon']
        bonus=[5,8,10,12]
        rand=random.randint(0,2)
        self.type=self.types[rand]
        self.bonus=bonus[rand]
        print(self.bonus)
        self.max_bonus=bonus[-1]
    def __repr__(self):
        return str(self.type)

class Turns():
    def __init__(self,nb_players,M,nb_ai):
        self.game_finish=False
        self.num=0
        self.nb_players=nb_players+nb_ai
        self.order=list(range(1,self.nb_players+1))
        random.shuffle(self.order)
        self.nb_country=M.nb_country
        self.players=[]
        # Generation of players
        for k in range(0,nb_players):
            self.players.append(Player(k+1,M,self))
        for k in range(nb_players, nb_ai+nb_players):
            self.players.append(AI(k+1,M,self))
        # Assignment of objective after players are made
        self.goal=Goal(M,self)
        for k in range(0,self.nb_players):
            self.players[k].obj=Objective(self.goal,self.players[k])
        self.id_order=0
        self.map=M
        self.list_phase=['placement','attack','deplacement']
        self.phase=0
        self._player_turn=self.order[self.id_order]

    def next(self):
        print("in next")
        if self.players[self.player_turn-1].nb_troops>0:
            raise ValueError('Need to deploy',self.players[self.player_turn-1].nb_troops)
        print("num",self.num,"id order",self.id_order)
        if self.num==0: # Initial placement phase
            self.id_order=(self.id_order+1)%len(self.order)
            if self.id_order==0:
                self.num+=1
                self.phase=(self.phase+1)%len(self.list_phase)
        elif self.num==1: # Skip placement phase
            self.phase=(self.phase+1)%len(self.list_phase)
            if self.phase == 0 :
                self.phase+=1
                self.id_order=(self.id_order+1)%len(self.order)
                # Update if country is captured
                self.players[self.player_turn-1].win_land=False
                if self.id_order==0:
                    self.num+=1
                    self.phase=0
                    # Update number of troops available (reinforcments at beginning of turn)
                    self.players[self.player_turn-1].nb_troops+=self.players[self.player_turn-1].sbyturn
        else:
            self.phase=(self.phase+1)%len(self.list_phase)
            if self.phase == 0 :
                self.id_order=(self.id_order+1)%len(self.order)
                # Update if country is captured
                self.players[self.player_turn-1].win_land=False
                # Update number of troops available (reinforcments at beginning of turn)
                self.players[self.player_turn-1].nb_troops+=self.players[self.player_turn-1].sbyturn
                if self.id_order==0:
                    self.num+=1
        print('turn number:', self.num,'order',self.order,'player turn', self.order[self.id_order])
        print(self.list_phase[self.phase])

    def next_player(self):
        # if self.players[self.player_turn-1].nb_troops>0:
        #   raise ValueError('Need to deploy',self.players[self.player_turn-1].nb_troops)
        if self.num==0: # Initial placement phase
            self.id_order=(self.id_order+1)%len(self.order)
            if self.id_order==0:
                self.num+=1
                self.phase=(self.phase+1)%len(self.list_phase)
        elif self.num==1: # Skip placement phase
            self.phase=1
            self.id_order=(self.id_order+1)%len(self.order)
            # Update if country is captured
            self.players[self.player_turn-1].win_land=False
            if self.id_order==0:
                self.num+=1
                self.phase=0
                # Update number of troops available (reinforcments at beginning of turn)
                self.players[self.player_turn-1].nb_troops+=self.players[self.player_turn-1].sbyturn
        else:
            # Next players turn
            self.id_order=(self.id_order+1)%len(self.order)
            self.phase=0
            # Update if country is captured
            self.players[self.player_turn-1].win_land=False
            # Update number of troops available (reinforcments at beginning of turn)
            self.players[self.player_turn-1].nb_troops+=self.players[self.player_turn-1].sbyturn
            if self.id_order==0:
                self.num+=1

    def start_deploy(self):
        if self.nb_players==3:
            nb_troops=35
        elif self.nb_players==4:
            nb_troops=30
        elif self.nb_players==5:
            nb_troops=25
        elif self.nb_players==6:
            nb_troops=20
        else:
            #throw execption
            print('Number of players invalid')
        print("start_deploy:",nb_troops)
        for p in self.players:
            p.nb_troops=nb_troops

    def distrib_country(self,country):
        lst_id_country=[]
        for k in country:
            lst_id_country.append(k.id)
        random.shuffle(lst_id_country)
        n=self.nb_country//self.nb_players
        for idx,i in enumerate(range(0, len(lst_id_country),n)):
            if idx<self.nb_players:
                self.players[idx].country=lst_id_country[i:i+n]
            else:
                for country_restant in lst_id_country[i:i+n]:   # Randomly assign the remaining countries varient when neutral?
                    self.players[random.randint(0,self.nb_players-1)].country.append(country_restant)
        for p in self.players:
            for country in p.country:
                self.map.country[country-1].id_player=p.id
                self.map.country[country-1].nb_troops=1 # Each territory required at least one soldier
                p.nb_troops-=1
        return lst_id_country     #debug

    def throw_dices(self,atck,defense):
        d_a=[]
        d_b=[]
        losses=[0,0,d_a,d_b] #[Attacker losses, Defender]
        for k in range(0,atck):
            d_a.append(random.randint(1,6))
        d_a.sort(reverse=True)
        for k in range(0,defense):
            d_b.append(random.randint(1,6))
        d_b.sort(reverse=True)
        for k in range(0,min(atck,defense)):
            if d_b[k]<d_a[k]: # Attacker won
                losses[1]=losses[1]+1
            else:
                losses[0]=losses[0]+1
        return losses

    def attack(self,country_a,country_d,nb_attackers):
        res_l=[]
        while(True):
            if nb_attackers>2:
                dice_atck=3
            elif nb_attackers>1:
                dice_atck=2
            elif nb_attackers>0:
                dice_atck=1
            else:
                #throw exception
                raise ValueError('not enough troops :',nb_attackers)
            if country_d.nb_troops>1:
                dice_def=2
            elif country_d.nb_troops>0:
                dice_def=1
            res=self.throw_dices(dice_atck,dice_def)
            print(res)
            res_l.append(res)
            country_a.nb_troops-=res[0]
            nb_attackers-=res[0]
            country_d.nb_troops-=res[1]

            if nb_attackers==0: # The attack failed
                return False,res_l
            elif country_d.nb_troops==0: # Country is captured
                # Update list of countries per player
                self.players[country_a.id_player-1].country.append(country_d.id)
                self.players[country_d.id_player-1].country.remove(country_d.id)
                # Change player id
                country_d.id_player=country_a.id_player
                # Automatically move the number of attacking troops based on number of die used
                self.deplacer(country_a,country_d,dice_atck)
                # Give player card after first successful capture of turn

                if self.players[country_a.id_player-1].win_land==False:
                    self.players[country_a.id_player-1].win_land=True
                    # If player has more than 5 they discard
                    if len(self.players[country_a.id_player-1].cards)>4:
                        self.players[country_a.id_player-1].del_card(0)
                        #TODO raise ValueError('Too much cards',len(self.players[country_a.id_player-1].cards))
                    self.players[country_a.id_player-1].cards.append(Card())
                    #print(self.players[country_a.id_player-1].cards)
                return True,res_l  #success

    def deplacer(self,country_ori,country_dest,nb_troops):
        country_ori.nb_troops-=nb_troops
        country_dest.nb_troops+=nb_troops

    def placer(self,country,nb_troops):
        print("in placer")
        # Decrease counter when player places a troop
        player=next((p for p in self.players if p.id == country.id_player), None)
        print("Troops:",player.nb_troops, nb_troops)
        if (player.nb_troops-nb_troops<=0):
            print("time to change players")
            country.nb_troops+=player.nb_troops
            player.nb_troops-=player.nb_troops
            self.next()
        else:
            player.nb_troops-=nb_troops
            country.nb_troops+=nb_troops

    def print_players(self):
        for p in self.players:
            p.print_carac()

    @property
    def player_turn(self): # Update when called
        return self.order[self.id_order]

class Check():
    def __init__(self):
        self.totalcheck=0

        # either unique or open
    def country_unicite(self,country):
        self.a=a

if __name__ == '__main__':
    print("== Unit Tests ==")
    M=Map('Terre')
    Continents=M.continents
    Europe=Continents[4]
    print(Europe.bonus)
    print(Europe.nb_country)
    for P in T.players:
        print(P.country,P.id)

    print("== Attack Tests ==")
    T=Turns(4,M)
    r=T.throw_dices(1,2)
    print(r[0:2])
    print("== Order Tests ==")
    print(T.order)

    print("== Tests round 0 ==")
    T.start_deploy()
    print(T.distrib_country(M.country))
    T.print_players()
    M.print_country()
