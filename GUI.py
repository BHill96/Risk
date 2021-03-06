#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

"""
This file creates the UI for the game risk. Comments have been translated from french to english,
so they be slightly off.
"""

import functools
import pygame
from pygame.locals import *
import Risk
import glob
import pickle 

PATH_IMG='Pictures/'
PATH_MAP='Pictures/Maps/'
PATH_BCK='Pictures/Backgrounds/'
PATH_DCE='Pictures/Dices/'
MAP_IMG='Risk_game_map_fixed_greylevel.png'
MAP_LVL='Risk_game_map_fixed_greylevel.png'
BCK_IMG='background5.jpg'
BAR_IMG='bar.png'
# Skull/Deadhead
DHE_IMG='tete-de-mort.png'
POLICE_NAME='freesansbold.ttf'
POLICE_SIZE=16
DICE_SIZE=25
f_w=1280
f_h=800

# For debugging
SEC = 2

class ColorMap():
    def __init__(self):
        self.green=(0,255,0)
        self.red=(255,0,0)
        self.blue=(0,0,255)
        self.white=(255,255,255)
        self.black=(0,0,0)
        self.grey=(100,100,100)
        self.yellow=(255,255,0)
        self.purple=(255,0,255)
        self.cian=(0,255,255)
        self.dark_purple=(127,0,255)
        self.dark_green=(0,170,0)
        self.dark_red=(170,0,0)
        self.dark_blue=(0,0,170)

# To put in a class
def text_objects(text, font, color=(0,0,0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x,y,w,h))
        if click[0] == 1 and action != None:
            Win.functions.append(action)
    else:
        pygame.draw.rect(window, ic,(x,y,w,h))

    smallText = pygame.font.Font(POLICE_NAME, POLICE_SIZE)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    window.blit(textSurf, textRect)

def color_surface(surface,color):
    for x in range(0,surface.get_width()):
        for y in range(0,surface.get_height()):
            if surface.get_at((x,y))!=(0,0,0):
                surface.set_at((x,y),color)

# not used right now
def color_surface_map(surface,color,map_color):
    for x in range(0,surface.get_width()):
        for y in range(0,surface.get_height()):
            if surface.get_at((x,y))==map_color:
                surface.set_at((x,y),color)
# useless?
def colorize(image, newColor):
    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

def color_surface(sprite,color,alpha):
    for x in range(0,sprite.bounds.width):
        for y in range(0,sprite.bounds.height):
            if sprite.map_country.get_at((sprite.bounds.x+x,sprite.bounds.y+y))!=(0,0,0):
                sprite.map_country.set_at((sprite.bounds.x+x,sprite.bounds.y+y),color)
                sprite.map_country.set_alpha(alpha)

def add_text(layer,message,pos,font,color=(0,0,0)):
    textSurf, textRect = text_objects(message, font,color)
    textRect.topleft = pos
    layer.append([textSurf, textRect])

def display_troops(textes,sprites,Map):
    smallText = pygame.font.Font(POLICE_NAME,POLICE_SIZE)
    for sprite in sprites:
        country=Map.country[sprite.id-1]
        textSurf, textRect = text_objects(str(country.nb_troops), smallText)
        textRect.center = sprite.bounds.center
        textes.append([textSurf, textRect])

def display_win(final_layer,players):
    bigText = pygame.font.Font(POLICE_NAME,42)
    marge=50
    pos=(200,200)
    for p in players:
        if p.obj.get_state()==True:
            p_win=p
            # player win
            textSurf, textRect = text_objects(p_win.name+' win', bigText,p_win.color)
            textRect.topleft = pos
            pos=(pos[0],pos[1]+marge)
            final_layer.append([textSurf, textRect])
            # objective
            textSurf, textRect = text_objects('Objective '+p_win.obj.description, bigText,p_win.color)
            textRect.topleft = pos
            pos=(pos[0],pos[1]+marge)
            final_layer.append([textSurf, textRect])

def display_help(final_layer,colormap):
    bigText = pygame.font.Font(POLICE_NAME,42)
    marge=50
    pos=(200,200)
    add_text(final_layer,'ESC : exit game',pos,bigText,colormap.white)
    pos=(pos[0],pos[1]+marge)
    add_text(final_layer,'n : next phase',pos,bigText,colormap.white)
    pos=(pos[0],pos[1]+marge)
    add_text(final_layer,'p : next player turn',pos,bigText,colormap.white)
    pos=(pos[0],pos[1]+marge)
    add_text(final_layer,'h : show/hide help menu',pos,bigText,colormap.white)
    pos=(pos[0],pos[1]+marge)
    add_text(final_layer,'d : show/hide quest',pos,bigText,colormap.white)
    pos=(pos[0],pos[1]+marge)
    add_text(final_layer,'u : use your cards',pos,bigText,colormap.white)

def display_hud(nb_units,t_hud,turns,pos,hide):
    smallText = pygame.font.Font(POLICE_NAME,POLICE_SIZE)
    marge=20
    col=[100,400,700,1000]
    row=pos[1]
    # Player part
    textSurf, textRect = text_objects('Turn : '+str(turns.num), smallText)
    textRect.topleft = pos
    t_hud.append([textSurf, textRect])
    textSurf, textRect = text_objects('Player: ',smallText)
    pos=(pos[0],pos[1]+marge)
    textRect.topleft = pos
    t_hud.append([textSurf, textRect])
    textSurf, textRect = text_objects(turns.players[turns.player_turn-1].name, smallText,turns.players[turns.player_turn-1].color)
    textRect.topleft = (pos[0]+70,pos[1]) # Not clean?
    t_hud.append([textSurf, textRect])
    textSurf, textRect = text_objects('Phase : '+turns.list_phase[turns.phase], smallText)
    pos=(pos[0],pos[1]+marge)
    textRect.topleft = pos
    t_hud.append([textSurf, textRect])
    textSurf, textRect = text_objects('Soldiers per Turn: '+str(turns.players[turns.player_turn-1].sbyturn), smallText)
    pos=(pos[0],pos[1]+marge)
    textRect.topleft = pos
    t_hud.append([textSurf, textRect])
    textSurf, textRect = text_objects('Soldiers to Deploy: '+str(turns.players[turns.player_turn-1].nb_troops), smallText)
    pos=(pos[0],pos[1]+marge)
    textRect.topleft = pos
    t_hud.append([textSurf, textRect])
    textSurf, textRect = text_objects('Selected Soldiers: '+str(nb_units), smallText)
    pos=(pos[0],pos[1]+marge)
    textRect.topleft = pos
    t_hud.append([textSurf, textRect])

    # Objectives part
    textSurf, textRect = text_objects('Objective(s) ', smallText)
    pos=(col[1],row)
    textRect.topleft = pos
    t_hud.append([textSurf, textRect])
    if hide==False:
        try:
            textSurf, textRect = text_objects(str(turns.players[turns.player_turn-1].obj.description), smallText)
        except AttributeError as e:
            print (e.args)
        pos=(col[1],row+marge)
        textRect.topleft = pos
        t_hud.append([textSurf, textRect])
        try:
            textSurf, textRect = text_objects('Status : '+str(turns.players[turns.player_turn-1].obj.get_state()), smallText)
        except AttributeError as e:
            print (e.args)
        pos=(col[1],row+2*marge)
        textRect.topleft = pos
        t_hud.append([textSurf, textRect])

    # Cards part
    textSurf, textRect = text_objects('Cards', smallText)
    pos=(col[1],row+3*marge)
    textRect.topleft = pos
    t_hud.append([textSurf, textRect])
    if hide==False:
        textSurf, textRect = text_objects(str(turns.players[turns.player_turn-1].cards), smallText)
        pos=(col[1],row+4*marge)
        textRect.topleft = pos
        t_hud.append([textSurf, textRect])

    # Continents bonus part
    pos=(col[3],row)
    textSurf, textRect = text_objects('Bonus Continents', smallText)
    textRect.topleft = pos
    t_hud.append([textSurf, textRect])
    for idx,c in enumerate(turns.map.continents):
        pos=(col[3],row+(idx+1)*marge)
        textSurf, textRect = text_objects(c.name+' '+str(c.bonus), smallText)
        textRect.topleft = pos
        t_hud.append([textSurf, textRect])

def display_continent(cont,temp_layer):
    for p in cont.country:
        temp_layer.append(next((x.map_country for x in self.sprites_country_masque if x.id == p.id), None))

def save_game(obj_lst):
    # Saving the objects:
    with open('saved_game', 'wb') as f:
        pickle.dump(obj_lst, f)
        print('Game saved')

def restore_game(obj_lst):
    # Getting back the objects:
    with open('saved_game','rb') as f:
        obj_lst=pickle.load(f)
        print('Game restored')

class GamePara():
    def __init__(self):
        self.nb_players=0
        self.tour=0
        self.players=[]

class SpritePays():
    def __init__(self,surface,name_id):
        self.map_country=surface
        self.name_country=''
        self.id=int(name_id[-6:-4]) # Not very clean
        self.bounds=surface.get_bounding_rect()

class CurrentWindow():
    def __init__(self,window,turns):
        self.window=window
        self.functions=[] # List all functions to be performed
        self.surfaces=[] # List all surfaces to be displayed
        self.dices=[] # List all die surfaces
        self.game=GamePara()
        self.turns=turns
        self.players=turns.players
        self.map=turns.map
        self.textes=[] # List of troop text to be merged after surfaces
        self.tmp=[] # List of temporary sprites
        self.t_hud=[] # List of HUD text
        self.final_layer=[] # Last display layer, used for winning screen and help menu
        self._nb_units=25 # Number of units 
        self.country_select=None # Selected country

    @property
    def nb_units(self):
        if self.turns.phase==0: # Get rules during deployment phase
            return min(self._nb_units,self.players[self.turns.player_turn-1].nb_troops) # Player cannot select more troops than they have
        else:
            return self._nb_units

    @nb_units.setter # Attention is incompatable with
    def nb_units(self, value):
        if self.turns.phase==0: # Setter rules during deployment
            if value<1:
                self._nb_units = 1
                raise ValueError('Too few troops',value)
            elif value>self.players[self.turns.player_turn-1].nb_troops:
                self._nb_units = self.players[self.turns.player_turn-1].nb_troops
                raise ValueError('Too much troops',value)
        else: # Setter rules during other phases
            if value<0:
                self._nb_units = 0
                raise ValueError('Too few troops',value)
            elif value>self.country_select.nb_troops-1:
                self._nb_units = self.country_select.nb_troops-1 # You can only attack/move with n-1 troops
                raise ValueError('Too much troops',value)
        self._nb_units = value

    def color_players(self,sprites):
        for pl in self.players:
            for country in pl.country:
                #print(pl.id,country,sprites[country-1].name_country)
                sprite=next((s for s in sprites if s.id == country), None)
                color_surface(sprite,pl.color,255)
                #print(sprite.id,country)

    # This function inits the game
    def start_game(self):
        self.surfaces=[]
        # Font blue
        # background = pygame.Surface(window.get_size())
        # background = background.convert()
        # background.fill(blue)
        # Personalize font
        background=pygame.image.load(PATH_BCK+BCK_IMG).convert()
        coeff=f_w/background.get_width() # Fit image to width
        w=int(coeff*background.get_width())
        h=int(coeff*background.get_height())
        background=pygame.transform.scale(background,(w,h))

        # Map
        map_world=pygame.image.load(PATH_IMG+MAP_IMG).convert_alpha()
        coeff=f_w/map_world.get_width() # Fit image to width
        w=int(coeff*map_world.get_width())
        h=int(coeff*map_world.get_height())
        map_world=pygame.transform.scale(map_world,(w,h))

        # HUD
        bar=pygame.image.load(PATH_IMG+BAR_IMG).convert_alpha()
        bar=pygame.transform.scale(bar,(f_w,f_h-h))

        self.functions=[]
        self.surfaces.extend([[background,(0,0)],[bar,(0,h)],[map_world,(0,0)]])

    def key_presses(self):
       for event in pygame.event.get():
           if event.type == QUIT:
               self.display=0
           elif event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                   self.display=0
               elif event.key == K_n:
                   try:
                       self.turns.next()
                   except ValueError as e:
                       print(e.args)
                   self.tmp=[]
                   self.select=False
                   self.sprite_select=0
               elif event.key == K_p:
                   try:
                       self.turns.next_player()
                   except ValueError as e:
                       print(e.args)
                   self.tmp=[]
                   self.select=False
                   self.sprite_select=0
               elif event.key == K_w: # Remove, debug func
                   self.turns.game_finish=True
               elif event.key == K_h:
                   self.help_menu = not self.help_menu
               elif event.key == K_c:
                   self.tmp=[]
                   display_continent(self.turns.map.continents[id_c],self.tmp)
                   id_c=(id_c+1)%len(self.turns.map.continents)
               elif event.key == K_u: # Card usage
                   self.turns.players[self.turns.player_turn-1].use_best_cards()
               elif event.key == K_d: # Display/Hide player goals
                   hide = not hide
               elif event.key == K_s: # Save backup
                   save_game(self)
               elif event.key == K_r: # Restore
                   restore_game(self.turns)
           elif event.type == MOUSEBUTTONDOWN:
               try:
                   if event.button==3: # Right click to unselect
                       self.tmp=[]
                       self.select=False
                       self.sprite_select=0
                   elif event.button==4: # Scroll wheel up
                       self.nb_units+=1
                   elif event.button==5: # Scroll wheel down
                       if self.nb_units>0:
                           self.nb_units-=1
               except AttributeError as e:
                   print('You should select a country first')
               except ValueError as e:
                   print(e.args)

    # This function manages the placement phase
    def placement(self, _click, _id_country_tmp):
        if _click[0]==1:
            country=next((p for p in self.map.country if p.id == _id_country_tmp), None)
            if country.id_player==self.turns.player_turn:
                # Update number of troops
                self.turns.placer(country, self.nb_units)
                # pygame.time.wait(100) # Not clean
            else:
                # Raise error
                print('Country does not belong to player')
   
    # This function manages the attack phase
    def attack(self, _click, _id_country_tmp, _sp_msq):
        if _click[0]==1 and not self.select: # Selection of attacking country
          self.country_select=next((p for p in self.map.country if p.id == _id_country_tmp), None)
          if self.country_select.id_player==self.turns.player_turn and self.country_select.nb_troops>1:
              self.nb_units=self.country_select.nb_troops-1
              self.tmp.append(_sp_msq.map_country)
              self.select=True 
              self.sprite_select=_id_country_tmp
        elif _click[0]==1: # Selection of defending country
            country2=next((p for p in self.map.country if p.id == _id_country_tmp), None)
            if self.atck_winmove and country2 == self.country_atck and self.country_select.nb_troops>1: # Move troops after successful attack
                self.turns.deplacer(self.country_select, country2, self.nb_units)
                self.select=False
                self.tmp=[]
                self.atck_winmove=False
            elif self.atck_winmove:
                self.select=False
                self.tmp=[]
                self.atck_winmove=False
            elif country2.id_player!=self.turns.player_turn and country2.id in self.country_select.neighbor:
                try:
                    self.dices=[] # Delete old dice sprites
                    atck,res_l=self.turns.attack(self.country_select, country2, self.nb_units)
                    for idx,res in enumerate(res_l):
                        roll_dices(self, res[0], res[2], 600, self.sprites_country[0].map_country.get_height()+10+idx*DICE_SIZE*1.1) # Not clean
                        roll_dices(self, res[1], res[3], 800, self.sprites_country[0].map_country.get_height()+10+idx*DICE_SIZE*1.1)
                    pygame.time.wait(100) # Not clean
                    #print(res)
                except ValueError as e:
                    print(e.args)
                    atck=False
                    self.select=False
                    self.tmp=[]
                if atck:
                    sprite=next((s for s in self.sprites_country if s.id == _id_country_tmp), None)
                    color_surface(sprite, self.turns.players[self.turns.player_turn-1].color, 255)
                    self.merged_country.blit(sprite.map_country,(0,0))
                    self.atck_winmove=True
                    self.country_atck=country2
                    self.nb_units=self.country_select.nb_troops-1
                else:
                    self.select=False
                    self.tmp=[]

    # This function manages the deplacement phase
    def deplacement(self, _click, _sp_msq, _id_country_tmp):
        print("in deplacement")
        if _click[0]==1 and not self.select:
            self.country_select=next((p for p in self.map.country if p.id == _id_country_tmp), None)
            if self.country_select.id_player==self.turns.player_turn and self.country_select.nb_troops>1:
                self.nb_units=self.country_select.nb_troops-1
                self.tmp.append(_sp_msq.map_country)
                self.select=True 
                self.sprite_select=_id_country_tmp
        elif _click[0]==1:
            country2=next((p for p in self.map.country if p.id == _id_country_tmp), None)
            chemin=self.map.chemin_exist(self.turns.players[self.turns.player_turn-1].country, self.country_select, country2)
            self.select=False
            self.sprite_select=0
            self.tmp=[]
            if chemin and country2.id != self.country_select.id:
                self.turns.deplacer(self.country_select, country2, self.nb_units)
                self.nb_units = 0
                self.turns.next()
        if self.country_select.id != _id_country_tmp:
        print("ERROR::SELECTED WRONG COUNTRY")

    # draws window
    def draw(self):
        for surface in self.surfaces:
            self.window.blit(surface[0],surface[1])
        for dice in self.dices:
            self.window.blit(dice[0],dice[1])
        #for sprite in self.sprites_country:
        #   self.window.blit(sprite.map_country,(0,0))
        self.window.blit(self.merged_country,(0,0))
        for tmp in self.tmp:
            self.window.blit(tmp,(0,0))
        for texte in self.textes:
            self.window.blit(texte[0],texte[1])
        for t in self.t_hud:
            self.window.blit(t[0],t[1])
        for final in self.final_layer:
            self.window.blit(final[0],final[1])
        if self.functions != []:
            for f in self.functions:
                f()             # Display functions

    # Draws help menu
    def draw_help(self):
        self.final_layer=[]
        win_screen = pygame.Surface(self.window.get_size())
        win_screen = win_screen.convert()
        win_screen.fill(colormap.black)
        win_screen.set_alpha(180)
        self.final_layer.append([win_screen,(0,0)])
        display_help(self.final_layer,colormap)

    # Checks for victory and ends the game if so
    def check_victory(self):
        if self.turns.players[self.turns.player_turn-1].obj.get_state()==True: # Not clean
            self.final_layer=[]
            win_screen = pygame.Surface(self.window.get_size())
            win_screen = win_screen.convert()
            win_screen.fill(colormap.black)
            win_screen.set_alpha(180)
            self.final_layer.append([win_screen,(0,0)])
            display_win(self.final_layer,self.players)

    # Loads map images
    def load_sprites(self, glob_country):
        for idx,fl in enumerate(glob_country):
            s=pygame.image.load(fl).convert()
            coeff=f_w/s.get_width()
            s=pygame.transform.scale(s,(int(coeff*s.get_width()),int(coeff*s.get_height())))
            sp=SpritePays(s,fl)
            sp_masque=SpritePays(s.copy(),fl)
            color_surface(sp_masque,(1,1,1),150)
            self.sprites_country.append(sp)
            self.sprites_country_masque.append(sp_masque)

    # This function manages the game.
    def display(self,fonction=None):
        colormap=ColorMap()
        self.display=1
        self.select=False
        self.atck_winmove=False
        self.sprite_select=-1
        self.sprites_country=[]
        self.help_menu=False
        id_c=0
        hide=True
        # Passing sprites
        self.sprites_country_masque=[]
        # Changing country sprites
        glob_country=glob.glob(PATH_MAP+"*.png")
        self.load_sprites(glob_country)

        # Color countries by player color
        self.color_players(self.sprites_country)
        for idx, spr in enumerate(self.sprites_country):#pas super propre
            if idx==0:
                self.merged_country = spr.map_country.copy()
            else:
                self.merged_country.blit(spr.map_country, (0, 0))

        # Display troops
        display_troops(self.textes,self.sprites_country,self.map)

        # This is where the game logic is
        mouse_color = (0,0,0,0)
        print("Entering 'while self.display:'")
        while self.display:
            #print('turn number:', self.turns.num, 'order', self.turns.order,'player turn', self.turns.order[self.turns.id_order])
            #print(self.turns.list_phase[self.turns.phase])
            #HUD
            #print('Turn Number:', self.num,'Order',self.order,'Player Turn', self.ordre[self.id_ordre])
            #print(self.list_phase[self.phase])
            self.t_hud=[]
            display_hud(self.nb_units,self.t_hud,self.turns,(75,self.sprites_country[0].map_country.get_height()+10),hide)
            pygame.display.flip()
            
            self.key_presses()
            self.draw()
            # for debugging
            pygame.time.wait(1000*SEC)
            # Victory screen for winning player
            self.check_victory()
            # Help screen
            if self.help_menu:
                self.draw_help()
            else:
                self.final_layer=[]

            mouse = pygame.mouse.get_pos()
            try:
                mouse_color=self.surfaces[2][0].get_at((mouse[0],mouse[1]))
            except IndexError as e:
                pass # Not clean
                #print(e.args)

            try:
                # AI
                phase = self.turns.list_phase[self.turns.phase]
                if self.turns.players[self.turns.player_turn-1].is_ai:
                  print(self.turns.players[self.turns.player_turn-1].name,"phase",phase)
                  if phase == 'placement':
                    placements = self.turns.players[self.turns.player_turn-1].placement()
                    for country in placements.keys():
                      self.nb_units = placements[country]
                      self.placement([1], country)
                    print("Done placing for {0}".format(self.turns.players[self.turns.player_turn-1].name))
                  elif phase == 'attack':
                    attack = self.turns.players[self.turns.player_turn-1].attack()
                    print("Final Attack Path:")
                    for a in attack:
                      print("  {0}::{1}::{2}".format(a[0].name, a[1].name, a[2]))
                      attkr = next((c for c in self.map.country if c.id == a[0].id), None)
                      sp_msq = next((sp for sp in self.sprites_country_masque if sp.id == attkr.id), None)
                      self.attack([1], attkr.id, sp_msq)
                      defnd = next((c for c in self.map.country if c.id == a[1].id), None)
                      sp_msq = next((sp for sp in self.sprites_country_masque if sp.id == defnd.id), None)
                      self.attack([1], defnd.id, sp_msq)
                      if attkr.nb_troops < 2:
                        print("  NUMBER OF TROOPS IS {0}".format(attkr.nb_troops))
                        break
                      if self.atck_winmove:
                        self.nb_units = attkr.nb_troops-1
                        self.attack([1], defnd.id, sp_msq)
                      else:
                        break
                    self.turns.next()
                  elif phase == 'deplacement':
                    deplacement = self.turns.players[self.turns.player_turn-1].deplacement()
                    if deplacement[2] <= 0:
                      print("Deplacement == {0}".format(deplacement[2]))
                      self.turns.next()
                    else:
                      print("{0}::{1}::{2}".format(deplacement[0], deplacement[1], deplacement[2]))
                      sp_msq=next((sp for sp in self.sprites_country_masque if sp.id == deplacement[0]), None)
                      self.deplacement([1], sp_msq, deplacement[0])
                      if deplacement[0] != self.country_select.id:
                        print("ERROR::GAME SELECTED {0} INSTEAD OF {1}".format(self.country_select.id, deplacement[0]))
                      sp_msq=next((sp for sp in self.sprites_country_masque if sp.id == deplacement[1]), None)
                      self.nb_units = deplacement[2]
                      self.deplacement([1], sp_msq, deplacement[1])
                    print("done deplacement")
                  # Display troops
                  self.textes=[]
                  display_troops(self.textes,self.sprites_country,self.map)
                # User interaction
                if mouse_color != (0,0,0,0) and mouse_color != (0,0,0,255):
                    id_country_tmp=mouse_color[0]-100
                    sp_msq=next((sp for sp in self.sprites_country_masque if sp.id == id_country_tmp), None)
                    if id_country_tmp != self.sprite_select:
                        self.window.blit(sp_msq.map_country,(0,0))
                        pygame.display.update(sp_msq.map_country.get_rect())
                    click = pygame.mouse.get_pressed()
                    # print("self.turns._player_turn",self.turns._player_turn)
                    if phase == 'placement':
                        self.placement(click, id_country_tmp)
                    elif phase == 'attack':
                        self.attack(click, id_country_tmp, sp_msq)
                    elif phase == 'deplacement':
                        self.deplacement(click, sp_msq, id_country_tmp)
                    # Display troops
                    self.textes=[]
                    display_troops(self.textes,self.sprites_country,self.map)
                    #break
            except ValueError as e:
              print("ERROR::{0}".format(e))
              pass # Not clean

def menu(Win):
    #useless?
    bar=pygame.image.load(PATH_IMG+BAR_IMG).convert()
    r1=Win.window.blit(bar,(0,0))
    Win.surfaces.extend([[bar,r1]])

# Die results and skulls (deaths)
def roll_dices(Win,pertes,number,x,y):
    L=[]
    for idx,d in enumerate(number):
        de=pygame.image.load(PATH_DCE+str(d)+".png").convert_alpha()
        resize_de=pygame.transform.scale(de,(DICE_SIZE,DICE_SIZE)) # Resize die
        L.append([resize_de,Win.window.blit(resize_de,(idx*DICE_SIZE*1.1+x,y))])

    for idx_p in range(0,pertes):
        deadhead=pygame.image.load(PATH_DCE+DHE_IMG).convert_alpha()
        resize_dh=pygame.transform.scale(deadhead,(DICE_SIZE,DICE_SIZE)) # Resize skulls
        L.append([resize_dh,Win.window.blit(resize_dh,(x-(idx_p+1)*DICE_SIZE*1.1,y))])
    Win.dices.extend(L) 

def menu_but(Win):
    #useless
    colors=ColorMap()
    #button('Start',150,150,100,50,colors.grey,colors.black,start_game)
    func=functools.partial(roll_dices,Win,[5,4,4],0,0)      # Generate new function
    button('Roll1',f_w/2,f_h/2,100,50,colors.grey,colors.black,func)
    func=functools.partial(roll_dices,Win,[1,6],0,0)        
    button('Roll2',300,300,100,50,colors.black,colors.black,func)

if __name__ == '__main__':
    import Risk
    from Risk import *
    print("== Unit Tests ==")
    M=Map('Terre')
    Continents=M.continents
    T=Turns(0,M,3)
    T.start_deploy()
    print(T.distrib_country(M.country))
    T.print_players()
    #M.print_country()
    Colors=ColorMap()
    T.players[0].name='Player A'
    T.players[0].color=Colors.dark_purple
    T.players[1].name='Player B'
    T.players[1].color=Colors.dark_green
    T.players[2].name='Player C'
    T.players[2].color=Colors.dark_red

    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((f_w, f_h))
    Win=CurrentWindow(window,T)
    Win.game.nb_players=0
    Win.game.nb_ai=3
    Win.game.players=[T.players[0].name, T.players[1].name, T.players[2].name]
    Win.functions.append(Win.start_game)        # Init functions
    clock.tick(60)

    Win.display()   # Display while loop
