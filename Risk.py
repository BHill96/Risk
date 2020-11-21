#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
import random
import copy

class Continent():
	def __init__(self,country,bonus,name,Map):
		self.bonus=bonus
		self.name=name
		self.country=[]
		for p in country:
			P=Pays(p,name,Map)
			self.country.append(P)
			Map.country.append(P)
		self.nb_country=len(self.country)

class Pays():
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
	def __init__(self,nb_players,M):
		self.game_finish=False
		self.num=0
		self.nb_players=nb_players
		self.order=list(range(1,nb_players+1))
		random.shuffle(self.order)
		self.nb_country=M.nb_country
		self.players=[]
		# Generation of players
		for k in range(0,nb_players):
			self.players.append(Player(k+1,M,self))
		# Assignment of objective after players are made
		self.goal=Goal(M,self)
		for k in range(0,nb_players):
			self.players[k].obj=Objective(self.goal,self.players[k])
		self.id_order=0
		self.map=M
		self.list_phase=['placement','attack','deplacement']
		self.phase=0
		self._player_turn=self.order[self.id_order]

	def next(self):
		if self.players[self.player_turn-1].nb_troops>0:
			raise ValueError('Need to deploy',self.players[self.player_turn-1].nb_troops)
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
		# 	raise ValueError('Need to deploy',self.players[self.player_turn-1].nb_troops)
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
				for country_restant in lst_id_country[i:i+n]:	# Randomly assign the remaining countries varient when neutral?
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
		# Decrease counter when player places a troop
		player=next((p for p in self.players if p.id == country.id_player), None)
		if(player.nb_troops-nb_troops<=0):
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

class Map():
	def __init__(self,name):
		self.name=name
		self.country=[]  
		self.continents=[]
		self.nb_country=0
		if name=='Terre':
			self.continents.append(Continent(['Congo','East Africa','Egypt','Madagascar','North Africe','South Africa']
											,3,'Africa',self))
			self.continents.append(Continent(['Alaska','Alberta','Central America','Eastern States','Greenland','North-West Territories','Ontario','Quebec','Western States']
											,5,'North America',self))
			self.continents.append(Continent(['Venezuela','Brazil','Peru','Argentina']
											,2,'South America',self))
			self.continents.append(Continent(['Afghanistan','China','India','Tchita','Japan','Kamchatka','Middle East','Mongolia','Siam','Siberia','Urals','Yakutia']
											,7,'Asia',self))
			self.continents.append(Continent(['Great Britian','Island','Northern Europe','Scandinavia','Southern Europe','Ukraine','Western Europe']
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
			self.continents[1].country[8].neighbor=[9,10,8,13]
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
				print('a path exists')
				return True
			else:
				print('no path')
				return False
		else:
			print('The countryn\' is not the player')
			return False

	def path_length(self,country,country_player,country_reachable):
		for p_id in country.neighbor:
			if p_id in country_player and p_id not in country_reachable:
				country_reachable.append(p_id)
				self.path_length(self.country[p_id-1],country_player,country_reachable)

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
