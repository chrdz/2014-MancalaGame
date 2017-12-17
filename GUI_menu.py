# ==============================================================================
"""Mancala : Mancala game"""
# ==============================================================================
__author__  = "Charlotte Rodriguez & Arthur Nguyen"
__version__ = "4.2"
__date__    = "2014-12-14"
__usage__   = """"""

# ==============================================================================
#main file: GUI_Mancala_main_program.py

import pygame, sys, time
from pygame.locals import *

# ==============================================================================
def ft_menu(fenetre, arene) :
    """ Main menu function """

    menu = True
    menu=pygame.image.load('img/walls/menu.png').convert_alpha()
    regle=pygame.image.load('img/walls/regles.png').convert_alpha()
    start=pygame.image.load('img/walls/start.png').convert_alpha()
    rect_regle = pygame.Rect(-600,0,600,451)
    rect_start = pygame.Rect(-600,0,600,451)
    fenetre.blit(arene,(0,0))
    fenetre.blit(regle,rect_regle)
    fenetre.blit(start, rect_start)
    abscisse_menu=0
    fenetre.blit(menu,(abscisse_menu,0))
    value_rule=""
    
    #ball (slider)
    abscisse_ball = 145
    abscisse_txt_seed = abscisse_ball+5
    img_ball = pygame.image.load('img/walls/ball.png').convert_alpha()
    pos_ball = pygame.Rect(abscisse_ball,224,36,36)
    pos_trail = pygame.Rect(144,233,20,18)
    trail = pygame.image.load('img/walls/trail.png').convert_alpha()
    fenetre.blit(img_ball,pos_ball)

    value_seed = 1
    myfont = pygame.font.SysFont("monospace", 42)
    txt_ball = myfont.render(str(value_seed), 1, (0,0,0))
    fenetre.blit(txt_ball, (abscisse_ball+5,255))
    
    #loading and blitting the size buttons, then rule buttons
    img_but_size = ['img/walls/5off.png','img/walls/30off.png',
                    'img/walls/42off.png']
    but_size=[0,0,0]
    pos_but_size = [0,0,0]
    abscisse_size = [160, 290, 440]

    img_but_rule = ['img/walls/aweleoff.png','img/walls/kalahoff.png',
                    'img/walls/owareoff.png']
    but_rule = [0,0,0]
    pos_but_rule = [0,0,0]
    abscisse_rule = [160, 310, 440]

    for i in range(3):
        but_size[i] = pygame.image.load(img_but_size[i]).convert_alpha()
        pos_but_size[i] = pygame.Rect(abscisse_size[i],110,101,71)
        fenetre.blit(but_size[i], pos_but_size[i])
        
        but_rule[i] = pygame.image.load(img_but_rule[i]).convert_alpha()
        pos_but_rule[i] = pygame.Rect(abscisse_rule[i],310,120,50)
        fenetre.blit(but_rule[i], pos_but_rule[i])

    mess_premium = pygame.image.load('img/walls/premium.png').convert_alpha()
    abscisse_prem = 600 
    pos_mess_premium = pygame.Rect(abscisse_prem,200,316,92)
    fenetre.blit(mess_premium, pos_mess_premium)

    
    endGame = False
    clic_size1, clic_size2, clic_size3 = False, False, False
    clic_rule1, clic_rule2, clic_rule3 = False, False, False
    clic_prem = False
    move_slider_seed = False
    show_rule = False

    while menu:
        for event in pygame.event.get():
            if event.type==QUIT or event.type==KEYDOWN and event.key==K_ESCAPE:
                endGame=True
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1: 
                if pos_but_size[0].collidepoint(pygame.mouse.get_pos()):
                    img_but_size[0] = 'img/walls/5on.png'
                    img_but_size[1] = 'img/walls/30off.png'
                    img_but_size[2] = 'img/walls/42off.png'
                    clic_size1,clic_size2,clic_size3=True,False,False 
                    abscisse_premium = 600 ###pk varaible en plus?
                    fenetre.blit(menu,(abscisse_menu,0))
                    pos_mess_premium = pygame.Rect(abscisse_premium,200,316,92)
                    fenetre.blit(mess_premium, pos_mess_premium)
                    
                elif pos_but_size[1].collidepoint(pygame.mouse.get_pos()) or \
                     pos_but_size[2].collidepoint(pygame.mouse.get_pos()) :
                    click_prem = True
                    abscisse_premium = 150 ###pk varaible en plus?
                    pos_mess_premium = pygame.Rect(abscisse_premium,200,316,92)
                    fenetre.blit(mess_premium, pos_mess_premium)

                elif pos_but_rule[0].collidepoint(pygame.mouse.get_pos()):
                    img_but_rule[0] = 'img/walls/aweleon.png'
                    img_but_rule[1] = 'img/walls/kalahoff.png'
                    img_but_rule[2] = 'img/walls/owareoff.png'
                    clic_rule1, clic_rule2, clic_rule3=True,False,False 
                elif pos_but_rule[1].collidepoint(pygame.mouse.get_pos()):
                    img_but_rule[0] = 'img/walls/aweleoff.png'
                    img_but_rule[1] = 'img/walls/kalahon.png'
                    img_but_rule[2] = 'img/walls/owareoff.png'
                    clic_rule1, clic_rule2, clic_rule3=False,True,False 
                elif pos_but_rule[2].collidepoint(pygame.mouse.get_pos()):
                    img_but_rule[0] = 'img/walls/aweleoff.png'
                    img_but_rule[1] = 'img/walls/kalahoff.png'
                    img_but_rule[2] = 'img/walls/owareon.png'
                    clic_rule1, clic_rule2, clic_rule3=False,False,True
                elif pos_ball.collidepoint(pygame.mouse.get_pos()):
                    move_slider_seed = True
                else: #si n a clique nulle part
                    abscisse_premium = 600 
                    pos_mess_premium = pygame.Rect(abscisse_premium,200,316,92)
                    fenetre.blit(menu,(abscisse_menu,0)) 
                for i in range(144, abscisse_ball):
                    pos_trail = pygame.Rect(i,233,20,18)
                    fenetre.blit(trail, pos_trail)
                fenetre.blit(txt_ball, (abscisse_txt_seed,255))
                        
            elif event.type == MOUSEBUTTONUP:
                move_slider_seed = False
            tempX, tempY = pygame.mouse.get_pos()
            if 140<tempX<507 and 225 < tempY < 270 and \
               event.type == MOUSEBUTTONDOWN and not show_rule:
                move_slider_seed = True
                
        if move_slider_seed:
            if 140<abscisse_ball<507:
                abscisse_ball = tempX-15 #modification of abscisse_ball
                value_seed = int((abscisse_ball-140)*42/(490-148))
            if abscisse_ball <= 148:
                abscisse_ball = 148
                value_seed = 1
            elif abscisse_ball >= 490:
                abscisse_ball = 490
                value_seed = 42

            i = 144
            pos_ball = pygame.Rect(abscisse_ball,224,36,36)
            
            fenetre.blit(menu,(abscisse_menu,0))
            fenetre.blit(trail, pos_trail)
            fenetre.blit(img_ball,pos_ball)
            txt_ball = myfont.render(str(value_seed), 1, (0,0,0))
            if value_seed < 10:
                abscisse_txt_seed = abscisse_ball+5
            else:
                abscisse_txt_seed = abscisse_ball-6
            fenetre.blit(txt_ball, (abscisse_txt_seed,255))
            for i in range(144, abscisse_ball):
                
                pos_trail = pygame.Rect(i,233,20,18)
                fenetre.blit(trail, pos_trail)
                           
        #hover size
        if pos_but_size[0].collidepoint(pygame.mouse.get_pos()):
            img_but_size[0] = 'img/walls/5on.png'
        elif pos_but_size[1].collidepoint(pygame.mouse.get_pos()):
            img_but_size[1] = 'img/walls/30on.png'
        elif pos_but_size[2].collidepoint(pygame.mouse.get_pos()):
            img_but_size[2] = 'img/walls/42on.png'
        else:
            if not clic_size1:
                img_but_size[0] = 'img/walls/5off.png'
            if not clic_size2:
                img_but_size[1] = 'img/walls/30off.png'
            if not clic_size3:
                img_but_size[2] = 'img/walls/42off.png'

        #hover rules
        if pos_but_rule[0].collidepoint(pygame.mouse.get_pos()):
            img_but_rule[0] = 'img/walls/aweleon.png'
        elif pos_but_rule[1].collidepoint(pygame.mouse.get_pos()):
            img_but_rule[1] = 'img/walls/kalahon.png'
        elif pos_but_rule[2].collidepoint(pygame.mouse.get_pos()):
            img_but_rule[2] = 'img/walls/owareon.png'
        else:
            if not clic_rule1:
                img_but_rule[0] = 'img/walls/aweleoff.png'
            if not clic_rule2:
                img_but_rule[1] = 'img/walls/kalahoff.png'
            if not clic_rule3:
                img_but_rule[2] = 'img/walls/owareoff.png'
            
        for i in range(3): 
            but_size[i] = pygame.image.load(img_but_size[i]).convert_alpha()
            but_rule[i] = pygame.image.load(img_but_rule[i]).convert_alpha()
            fenetre.blit(but_size[i], pos_but_size[i])
            fenetre.blit(but_rule[i], pos_but_rule[i])
    
        fenetre.blit(img_ball,pos_ball)
        fenetre.blit(mess_premium, pos_mess_premium) 
        pygame.display.flip()

        if clic_size1 and (clic_rule1 or clic_rule2 or clic_rule3):
            show_rule = True
            step = 0
            rect_regle = pygame.Rect(0,0,600,451)
            rect_start = pygame.Rect(135,370,100,42)
            if abscisse_menu > -630: 
                for i in range(3):
                    abscisse_size[i] -=15
                    abscisse_rule[i] -=15
                    abscisse_ball -= 15
                    pos_but_size[i] = pygame.Rect(abscisse_size[i],110,101,71)
                    pos_but_rule[i] = pygame.Rect(abscisse_rule[i],310,120,50)
                    pos_ball = pygame.Rect(abscisse_ball,224,36,36)
                    
                abscisse_menu -= 15
                fenetre.blit(arene,(0,0))
                fenetre.blit(regle,rect_regle)
                fenetre.blit(start, rect_start)
                fenetre.blit(menu,(abscisse_menu,0))
                fenetre.blit(img_ball,pos_ball)
                abscisse_txt_seed=-100
                fenetre.blit(txt_ball, (-100,255))
            else:
                if rect_start.collidepoint(pygame.mouse.get_pos()) and \
                   event.type == MOUSEBUTTONDOWN:
                    menu = False
            if clic_rule1:
                value_rule = "awele"
            elif clic_rule2:
                value_rule = "kalah"
            else:
                value_rule = "oware"
    return [value_seed, value_rule]
    #end


#<------ End of code ----->
