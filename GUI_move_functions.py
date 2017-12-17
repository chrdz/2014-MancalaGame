# ==============================================================================
"""Mancala : Mancala game"""
# ==============================================================================
__author__  = "Charlotte Rodriguez & Arthur Nguyen"
__version__ = "1.0"
__date__    = "2014-12-10"
__usage__   = """"""

# ==============================================================================
#main file: GUI_Mancala_main_program.py

import pygame, sys, time
from pygame.locals import *
from GUI_Mancala_main_program import *


# ==============================================================================
def comptage(count):
    """chooses 1 images (one index)(3 per direction) for the walking effet"""
    count=count-1
    if count%4 == 1:
        return(2)
    elif count%4 == 3:
        return(0)
    elif count%4 == 2 or count%4 == 0: #millieu
        return(1)

# ==============================================================================
def mouvx(left, right , posx):
    """axis move(domain)"""
    if right:
        return(posx+10)
    else:
        return(posx-10)

# ==============================================================================
def mouvy(down, up, posy):
    """ordinate move(range)"""
    if up:
        return(posy-7)
    else:
        return(posy+7)

# ==============================================================================
def ft_perso_mode(player):
    """prepares a list containing all version of a sprite"""

    perso_mode=[[],[],[],[]]
    mode = 0
    for i in range(0,2):
        if player%2 == 0:
            if i == 0:
                img = 'img/perso_walk/'
            else:
                img = 'img/perso_bike/'
        else:
            if i == 0:
                img = 'img/perso2_walk/'
            else:
                img = 'img/perso2_bike/'

        for j in range(0,4):
            j1, j2, j3 = (3*j)+1, (3*j)+2, (3*j)+3
            perso_mode[i].append([img+'%d.png' %j1, img+'%d.png' %j2,
                                  img+'%d.png' %j3])
    return(perso_mode)

# ==============================================================================
def ft_see_the_next(pos_dep, where):
    """return the x and y positions of the next house"""
    
    x_stop=0 #coordinates of the next position
    y_stop=0
    
    x=[131,211,291,371,451] #x of the houses from left to right
    met=[[],[]] #[[player_0:[x,y of the houses]],[player_1:[x,y of the houses]]]

    #building of met:
    met[0]=[[elem,297] for elem in x] 
    met[1]=[[elem,185] for elem in reversed(x)] 
    met[0].append([491,241])
    met[1].append([91,241]) 
    index_final = pos_dep%6 #index of the next house
    list_final =  where #list (0 or 1) in whic is the next house

    x_stop=met[list_final][index_final][0] #A COMPACTER########
    y_stop=met[list_final][index_final][1]

    return([x_stop, y_stop])

#-------------------------------------------------------------------------------
def ft_move(meta_save,fenetre, arene, perso, coor, pos_dep, where, mode,player):
    """move the perso to the next house"""

    down,up,right,left=False,False,False,False

    perso_mode=ft_perso_mode(player)

    #pos_dep%6 ==> does he move to the other list or not
    next = ft_see_the_next(pos_dep, where)

    img_down,img_up = perso_mode[mode][0],perso_mode[mode][1]
    img_left,img_right = perso_mode[mode][2],perso_mode[mode][3]

    if player%2 == 0:
        perso_idle = pygame.image.load('img/perso2_walk/2.png').convert_alpha()
        position_idle = pygame.Rect(60, 242,32,32)
    else:
        perso_idle = pygame.image.load('img/perso_walk/2.png').convert_alpha()
        position_idle = pygame.Rect(530, 242,32,32)
        
    while coor[0] > 91 and coor[1] == 185:
        if coor[0] < next[0]:
            return 0
        
        perso = pygame.image.load(img_left[coor[0]%3]).convert_alpha()
        left, right = True, False
        coor[0] = mouvx(left,right,coor[0])
        
        time.sleep(0.1)
        position_perso = pygame.Rect(coor[0], coor[1],32,32)
        fenetre.blit(arene,(0,0))
        fenetre.blit(perso_idle, position_idle)
        ft_blit_box(fenetre,meta_save)
        fenetre.blit(perso, position_perso)
        pygame.display.flip()

    while coor[0] == 91 and coor[1] < 297:
        if coor[1] > next[1]:
            return 0
        
        perso = pygame.image.load(img_down[coor[1]%3]).convert_alpha()
        down, up = True, False                
        coor[1] = mouvy(down,up,coor[1])
        
        time.sleep(0.1)
        position_perso = pygame.Rect(coor[0], coor[1],32,32)
        fenetre.blit(arene,(0,0))
        fenetre.blit(perso_idle, position_idle)
        ft_blit_box(fenetre,meta_save)
        fenetre.blit(perso, position_perso)
        pygame.display.flip()

    while coor[0] < 491 and coor[1] == 297:
        if coor[0] > next[0]:
            return 0

        perso = pygame.image.load(img_right[coor[0]%3]).convert_alpha()
        left, right = False, True
        coor[0] = mouvx(left,right,coor[0])
        
        time.sleep(0.1)
        position_perso = pygame.Rect(coor[0], coor[1],32,32)
        fenetre.blit(arene,(0,0))
        fenetre.blit(perso_idle, position_idle)
        ft_blit_box(fenetre,meta_save)
        fenetre.blit(perso, position_perso)
        pygame.display.flip()

    while coor[0] == 491 and coor[1] > 185:
        if coor[1] < next[1]:
            return 0
            
        perso = pygame.image.load(img_up[coor[1]%3]).convert_alpha()
        down, up = False, True                
        coor[1] = mouvy(down,up,coor[1])
        
        time.sleep(0.1)
        position_perso = pygame.Rect(coor[0], coor[1],32,32)
        fenetre.blit(arene,(0,0))
        fenetre.blit(perso_idle, position_idle)
        ft_blit_box(fenetre,meta_save)
        fenetre.blit(perso, position_perso)
        pygame.display.flip()
