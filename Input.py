#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

"""
This file manages input from the UI to the game.
Most french has been translated to english, so they might be slightly off meaning.
"""

from tkinter import *
import Risk
from Risk import *
import GUI
from GUI import *

fields = []
PLAYERS_COLORS=['red','green','blue','yellow','purple','cian']
MAX_NB_PLAYERS=6
MIN_NB_PLAYERS=3
CLOCK_TICK=60 #refresh rate

def fetch(entries):
   for entry in entries:
      field = entry[0]
      text = entry[1].get()
      color=entry[2].get()
      print('%s: "%s" %s' % (field, text,color))

def correspondance_colors(nameofcolor,colormap):
   if nameofcolor =='red':
      return colormap.red
   elif nameofcolor=='green':
      return colormap.green
   elif nameofcolor=='blue':
      return colormap.blue
   elif nameofcolor=='yellow':
      return colormap.yellow
   elif nameofcolor=='purple':
      return colormap.purple
   elif nameofcolor=='cian':
      return colormap.cian

def launch_game(entries):
   # Ensure players each have different colors
   try:
      players_names=[]
      players_colors=[]
      for entry in entries:
         players_names.append(entry[1].get())
         if entry[1].get()=='':
            raise ValueError('You must choose a player name')
         players_colors.append(entry[2].get())
      seen = set()
      uniq = []
      for c in players_colors:
         if c not in seen:
           uniq.append(c)
           seen.add(c)
      if not len(uniq)==len(players_names):
         raise ValueError('You must choose a different color from other players:')
   except ValueError as e:
         print (e.args)
   else:
      root.destroy() #exiting the players choicd window

      print("== Game launched ==")
      M=Map('Terre')
      Continents=M.continents
      nb_players=len(players_names)
      T=Turns(nb_players,M)
      T.start_deploy()
      print(T.distrib_country(M.country))
      T.print_players()
      #M.print_country()
      colors=ColorMap()
      for idx,play_name in enumerate(players_names):
         T.players[idx].color=correspondance_colors(players_colors[idx],colors)
         T.players[idx].name=play_name

      pygame.init()
      clock = pygame.time.Clock()
      fenetre = pygame.display.set_mode((f_w, f_h))
      Win=CurrentWindow(fenetre,T)
      Win.game.nb_players=nb_players
      Win.game.players=players_names
      menu(Win) # Init poster?
      Win.fonctions.append(Win.start_game) # Init functions
      clock.tick(CLOCK_TICK)
      Win.window() # We enter the display loop

def save(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()

def check_colors(entries,lst1):
   for entry in entries:
      if entry[2].get() in lst1: lst1.remove(entry[2].get())   

def makeform(root, fields):
   entries = []
   for idx,field in enumerate(fields):
      lab = Label(root, width=15, text=field, anchor='w')
      ent = Entry(root)
      lab.grid(row=idx, column=0)
      ent.grid(row=idx, column=1)
      # Color list
      lst1 = PLAYERS_COLORS
      # Colors already used

      var1 = StringVar()
      Drop = OptionMenu(root,var1,*lst1)
      Drop.grid(row=idx, column=2,sticky="ew") # make option menu with uniform width for all the rows 
      entries.append((field, ent,var1))
   return entries

def next():
   nb_players = int(Entry1.get())
   if nb_players<MIN_NB_PLAYERS:
      print("Minimum players number is "+str(MIN_NB_PLAYERS))
      nb_players=MIN_NB_PLAYERS
   elif nb_players>MAX_NB_PLAYERS:
      print("Maximum players number is "+str(MAX_NB_PLAYERS))
      nb_players=MAX_NB_PLAYERS
   else:
      print(nb_players)
   for k in range(0,nb_players):
      fields.append("Joueur"+str(k+1))
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))  # He didn't know what he was doing here 
   b1.grid_forget()
   Entry1.grid_forget()
   Lbl1.grid_forget()
   b2 = Button(root, text='Jouer',command=lambda e=ents: launch_game(e)) 
   b2.grid(row=20, column=0) # Not clear
   b3.grid(row=20, column=1) # Not clear
   
if __name__ == '__main__':
   root = Tk()
   root.title("Risk")

   Lbl1 = Label(root, text="Number de players:")
   Lbl1.grid(row=0, column=0,columnspan=2)
   Entry1 = Entry(root, bd =1)
   Entry1.grid(row=1, column=0,columnspan=2)

   b1 = Button(root, text='Next',command=next)
   b1.grid(row=2, column=0)
    
   b3 = Button(root, text='Quit', command=root.quit)
   b3.grid(row=2, column=1)
   root.mainloop()
