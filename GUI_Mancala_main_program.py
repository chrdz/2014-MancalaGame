# ==============================================================================
"""Mancala : Mancala game"""
# ==============================================================================
__author__  = "Charlotte Rodriguez & Arthur Nguyen"
__version__ = "7.4.2"
__date__    = "2014-12-14"
__usage__   = """"""

# ==============================================================================
#other files needed: img dir, GUI_menu.py, GUI_move_functions.py

import pygame, sys, time, copy, os
from pygame.locals import *
from GUI_move_functions import *
from GUI_menu import *
 
# ==============================================================================
os.system('color 2')

class board(object):
    def __init__(self):
        self.j0=0 #list
        self.j1=0 #list
    def ft_crealist(self, size, seed) :
        """ Create lists of j0 and j1 according to the number of blocs and
        seeds """
        
        list_p=[int(seed) for i in range(size)]
        list_p.append(0)
        list_op=[int(seed) for i in range(size)]
        list_op.append(0)
        self.j0, self.j1=list_p, list_op
    def __str__(self):
        """print the awele, with data from the parameter"""

        length = len(self.j0) #int
        strain = "" #str
        i = 0; #int
        j = 0; #int
        num_bottom = [" %3d " % i for i in range(1, length)]
        num_up=[elem for elem in reversed(num_bottom)]
        
        line_up = "| p_2 |%s|     |" % '|'.join(num_up)
        line_bottom = "|     |%s| p_1 |" % '|'.join(num_bottom)
        bord = "*%s" % ("-----*" * (length + 1))
        empty = "%s|" % ("|     " * (length + 1))
        in_nb_1 = ''.join(["| %3s " % (self.j1[length - j]) \
                           for j in range(2, length + 1)])
        nb_1 = "|     %s|     |" % (in_nb_1)
        silo = "| %3s *%s %3s |" % (self.j1[length - 1],"-----*" * (length - 1),
                                    self.j0[length - 1])
        in_nb_0 = ''.join(["| %3s " % (self.j0[j]) for j in range(length - 1)])
        nb_0 = "|     %s|     |" % (in_nb_0)
        return('\n'.join([line_up,bord, empty, nb_1, empty, silo, empty, nb_0,
                          empty, bord,line_bottom]))
    
# ==============================================================================
def ft_ask(ask, err):
    "do the try except thing"

    while True:
        try:
            result=input(ask)
            break
        except ValueError:
            pass
    return (result)

# ==============================================================================            
def ft_ask_pos(ask, err, cell_nb):
    """ask for pos in [1..cell_nb]"""

    strain = [str(i) for i in range(1, cell_nb + 1)]
    pos=0
    while (not (pos in strain)):
        pos=ft_ask(ask, err)
        
    return(pos)

# ==============================================================================
def ft_check_end(metalist, cell_nb, nb_seed):
    """ If one player has more than half of the amount of total seed, or if all
    boxes are empty, returns 1 if j0 wins, 2 if j1 wins """

    score = 0
    score2 = 0
    half_total = (cell_nb*nb_seed)
    last = len(metalist.j0)-1

    for i in range(len(metalist.j0)-1):
        score = score + metalist.j0[i]
    for j in range(len(metalist.j1)-1):
        score2 = score2 + metalist.j1[j]

    if score == 0 or score2 == 0:
        if metalist.j0[last] > metalist.j1[last]:
            return(1)
        else:
            return(2)
    
    if metalist.j0[cell_nb] > half_total:
        return(1)
    elif metalist.j1[cell_nb] > half_total:
        return(2)
    return(0)

# ==============================================================================
def ft_check_can_eat(list_adv, pos):
    """return True if can eat"""
    
    i = 0 #int

    for i in range(len(list_adv)-1):
        if i != pos:
            if list_adv[i] != 0:
                return True
    return False

# ==============================================================================
def ft_test_oware(metalist, pos, player,len_list):
    """ tests oware on a fake list"""
    test=board()
    test = copy.deepcopy(metalist)
    boolen=eval("test.j"+str((player+1)%2))[pos-1] == 2 or \
            eval("test.j"+str((player+1)%2))[pos-1] == 3
    while boolen and pos >= 0:
        eval("test.j"+str(player))[len_list-1] += eval("test.j"+str((player+1)%2))[pos-1]
        eval("test.j"+str((player+1)%2))[pos-1]=0
        pos-=1
        boolen=eval("test.j"+str((player+1)%2))[pos-1] == 2 or \
                eval("test.j"+str((player+1)%2))[pos-1] == 3
    answer=ft_check_can_eat(eval("test.j"+str((player+1)%2)), pos)
    return(answer)

# ==============================================================================
def ft_take_opposite(metalist, pos, player, list_p, list_op, rule, stop, plus):
    """ take seeds from the other player, doesn't if starves the other player"""

    len_list = len(list_p)

    take_oppo  = False #bool

    if (rule =="kalah" or rule == "awele") and list_p[pos-1] == 1 :
        if list_p == eval("metalist.j"+str(player)): #if player on his own list
            take_oppo = ft_check_can_eat(eval("metalist.j"+str((player+1)%2)),
                                         len_list-1-pos)
        elif rule=="awele" : # rule awele and player not on his own list
            take_oppo = ft_check_can_eat(list_op,len_list-1-pos)
        if take_oppo:
            eval("metalist.j"+str(player))[len_list-1] += list_op[len_list-1-pos]+1
            list_op[len_list-1-pos], list_p[pos-1] = 0, 0

    elif rule == "oware" and list_p == eval("metalist.j"+str((player+1)%2)):
        take_oppo = ft_test_oware(metalist, pos, player, len_list)
        if take_oppo :
            while (list_p[pos-1] == 2 or list_p[pos-1] == 3) and pos >= 0:
                eval("metalist.j"+str(player))[len_list-1] += list_p[pos-1]
                list_p[pos-1]=0
                pos-=1
    return()
# ==============================================================================
def ft_blit_box(fenetre,meta_list):
    """change window print taking acount of meta_list"""

    index_silo = len(meta_list.j0) - 1
    #Box number-of-pokeball indicator
    box_dim = (28,18)
    abscisse_box = []

    coord_box_up = []
    coord_box_down = []
    value_box_up = []
    value_box_down = []
    value_box_up = [elem for elem in reversed(meta_list.j1[:5])]
    value_box_down = [elem for elem in meta_list.j0[:5]]
    
    rect_box = []
    
    myfont = pygame.font.SysFont("monospace", 12)

    for i in range(5):
        abscisse_box.append(78*(i+1))
        coord_box_up.append((50+abscisse_box[i%5], 105))
        coord_box_down.append((50+abscisse_box[i%5], 342))
        pygame.draw.rect(fenetre,(255,255,255),Rect(coord_box_up[i], box_dim))
        pygame.draw.rect(fenetre,(255,255,255),Rect(coord_box_down[i], box_dim))

        txt_value_up = myfont.render(str(value_box_up[i]), 1, (0,0,0))
        txt_value_down = myfont.render(str(value_box_down[i]), 1, (0,0,0))
        fenetre.blit(txt_value_up, (abscisse_box[i%5]+56, 105+3))
        fenetre.blit(txt_value_down, (abscisse_box[i%5]+56, 342+3))

    pygame.draw.rect(fenetre,(255,255,255),Rect((22,255), box_dim))
    txt_freq = myfont.render(str(meta_list.j1[index_silo]), 1, (0,0,0))
    fenetre.blit(txt_freq, (27, 258))

    pygame.draw.rect(fenetre,(255,255,255),Rect((546,255), box_dim))
    txt_freq = myfont.render(str(meta_list.j0[index_silo]), 1, (0,0,0))
    fenetre.blit(txt_freq, (551, 258))
    return()

# ==============================================================================
def ft_print_box(metalist,fenetre, t):
    """do the print thing for the little boxes containing numbers"""
    
    ft_blit_box(fenetre,metalist)
    pygame.display.flip()
    time.sleep(t)
    return()
# ==============================================================================

def ft_pos_perso_begin(metalist, pos_dep, player):
    """return the x and y positions of the next house"""
    
    x=[131,211,291,371,451]
    met=[[],[]]
    met[0]=[[elem,297] for elem in x]
    met[1]=[[elem,185] for elem in reversed(x)]

    met[0].append([491,241])
    met[1].append([91,241])

    return([met[player][pos_dep][0], met[player][pos_dep][1]])

#-------------------------------------------------------------------------------
def ft_distrib(metalist, pos, player, rule, fenetre, arene, perso, coor, mode):
    """Distribute the seeds. Return -1 if the box is empty, return 1 if valid,
    2 if the player can play again """
    
    if player%2 == 0:
        perso_idle = pygame.image.load('img/perso2_walk/2.png').convert_alpha()
        position_idle = pygame.Rect(60, 242,32,32)
    else:
        perso_idle = pygame.image.load('img/perso_walk/2.png').convert_alpha()
        position_idle = pygame.Rect(530, 242,32,32)
    
    result = 1
    if eval("metalist.j"+str(player))[pos-1] == 0:
        return(-1)
    list_p = eval("metalist.j"+str(player))
    list_op = eval("metalist.j"+str((player+1)%2))
    len_list = len(list_p)
    last_p = len_list-1 #index of the silo

    #perso goes in front of the right house
    pos_dep=ft_pos_perso_begin(metalist, pos-1, player)
    coor[0] = pos_dep[0]
    coor[1] = pos_dep[1]
    position_perso = pygame.Rect(coor[0],coor[1],32,32)
    fenetre.blit(arene,(0,0))
    fenetre.blit(perso, position_perso)
    fenetre.blit(perso_idle, position_idle)
    pygame.display.flip()
    ft_print_box(metalist,fenetre, 1.5)

    hand = list_p[pos-1] #taking the seeds from the selected box
    list_p[pos-1] = 0 #emptying the selected box
    ft_print_box(metalist,fenetre, 0.1)
    meta_save = board()
    where = player
    
    while hand>0:
        meta_save = copy.deepcopy(metalist)
        list_p[pos] += 1
        ft_move(meta_save,fenetre, arene, perso, coor ,pos, where, mode, player)
        ft_print_box(metalist,fenetre, 0.75)
        hand -= 1
        if pos == last_p:
            if hand == 0:
                result = 2
            list_p, list_op = list_op, list_p
            where = (where+1)%2
            pos = 0
        else:
            pos +=1
    if result != 2: #if last seed not in silo
        ft_take_opposite(metalist, pos, player, list_p, list_op, rule, False, 0)
    return(result)

# ==============================================================================
def main() :
    """ Main function """

    #var
    meta_list = board() #player's lists
    i = 0 #to determine which player is playing, J0 or J1
    pos = 0 #position of the cell entered by the player
    line = ""
    player = 0 #0 for player_1, 1 for player_2
    mode=0

    answer = 0
    #-1 if the houses doesn't hold any seed
    # 2 if the player ca play again
    # 1 if ft_distrib worked and it's the next player's turn

    #491, 185
    posx, posy = 530, 242 #perso's position at the beginning of the game. idle
    coor1= [posx, posy]

    posx2, posy2 = 60, 242 #2perso's position at the beginning of the game. idle
    coor2= [posx2, posy2]

    print("Follow the white rabbit...")
    pygame.init()
    fenetre=pygame.display.set_mode((600,450))
    arene=pygame.image.load('img/walls/arene.png').convert_alpha()
    
    #Chargement et collage du personnage
    perso1 = pygame.image.load("img/perso_walk/2.png").convert_alpha()
    perso2 = pygame.image.load("img/perso2_walk/2.png").convert_alpha()
    perso42 = pygame.image.load("img/42.png").convert_alpha()
    #perso
    perso_mode=ft_perso_mode(player)

    #begin
    options=[]
    options = ft_menu(fenetre, arene)
    nb_seed, cell_nb, rule = options[0], 5, options[1]
    meta_list.ft_crealist(cell_nb,nb_seed)

    #konami
    first, second, third, fourth,fifth = False, False, False, False, False
    sixth, seventh, eighth, ninth, konami = False, False, False, False, False
        
    fenetre.blit(arene,(0,0))
    position_perso1 = pygame.Rect(coor1[0],coor1[1],32,32)
    position_perso2 = pygame.Rect(coor2[0],coor2[1],32,32)
    abscisse42, ordonnee42 = 600,0
    position_perso42 = pygame.Rect(abscisse42,ordonnee42,348,234)
    fenetre.blit(perso42,position_perso42)
    fenetre.blit(perso1, position_perso1)
    fenetre.blit(perso2, position_perso2)
    ft_print_box(meta_list,fenetre, 0.1)

    message =  ""
    myfont = pygame.font.SysFont("Arial", 30)
    txt = myfont.render("Prof. Oak: "+message, 1, (0,0,0))
    pos_text = (20,380)
    fenetre.blit(txt, pos_text)

####### 
    while True:
        if konami:
            message = "Now is not the time to use that."
            abscisse42 -= 42
            ordonnee42 += 4.2
            position_perso42 = pygame.Rect(abscisse42,ordonnee42,348,234)
            fenetre.blit(perso42, position_perso42)
            if 100 < abscisse42 < 150:
                time.sleep(0.42)
            if abscisse42 < -350:
                abscisse42, ordonnee42 = 600,0
                konami = False
                          
        if ft_check_end(meta_list, cell_nb, nb_seed) == 2:
            message = "Leaf wins"
        elif ft_check_end(meta_list, cell_nb, nb_seed) == 1:
            message = "Red wins"
        txt = myfont.render("Prof. Oak: "+message, 1, (0,0,0))
        fenetre.blit(txt, pos_text)
        pygame.display.flip
        
        if player%2 == 0:
            perso = perso1
            coor = coor1
        else:
            perso = perso2
            coor = coor2
        for event in pygame.event.get():
            if event.type==QUIT or event.type==KEYDOWN and event.key==K_ESCAPE:                
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONUP and event.button == 1:       
                a=0
                for s in range(5):
                    if ((107+s*74)<event.pos[0]<(178+s*74)) and \
                       ((238-player*108)<event.pos[1]<(300-player*108)):
                        if player == 0:
                            answer=ft_distrib(meta_list, s+1, player, rule,
                                              fenetre, arene, perso, coor, mode)
                        elif player == 1:
                            answer=ft_distrib(meta_list, 6-s-1, player, rule,
                                              fenetre, arene, perso, coor, mode)
                        if answer == 1 :
                            player = (player+1)%2
                            answer = 0
                        break
                    
            if event.type == KEYDOWN:   #activation of the Konami code
                if event.key == K_F1:
                    mode = (mode+1)%2
                if event.key == K_UP:    
                    first=True
                if event.key == K_UP    and first:
                    second, first = True, False
                if event.key == K_DOWN  and second:
                    third, second = True, False
                if event.key == K_DOWN  and third:
                    fourth, third = True, False
                if event.key == K_LEFT  and fourth:
                    fifth, fourth = True, False
                if event.key == K_RIGHT and fifth:
                    sixth, fifth = True, False
                if event.key == K_LEFT  and sixth:
                    seventh, sixth = True, False
                if event.key == K_RIGHT and seventh:
                    eighth, seventh = True, False
                if event.key == K_b     and eighth:
                    ninth, eighth = True, False
                if event.key == K_q     and ninth:
                    ninth, konami = False, True
            
        fenetre.blit(arene,(0,0))
        position_perso1 = pygame.Rect(coor1[0],coor1[1],32,32)
        position_perso2 = pygame.Rect(coor2[0],coor2[1],32,32)
        fenetre.blit(perso42,position_perso42)
        message = "Error 418, I'm a teapot"   
        if player%2 == 1:
            fenetre.blit(perso2, (496,192))
            fenetre.blit(perso1, (posx, posy))#idle
            message = "Leaf's turn"
        else:
            fenetre.blit(perso1, (90,305))
            fenetre.blit(perso2, (posx2,posy2))#idle
            message = "Red's turn"

                     
        fenetre.blit(txt, pos_text)

        ft_print_box(meta_list,fenetre, 0.1)        
    #end
#-----------------------------------------------------------------------------------
if __name__ == "__main__" :
    main()
