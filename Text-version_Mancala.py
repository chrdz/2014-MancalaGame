# ==============================================================================
""" MANCALA : text version """
# ==============================================================================
__author__  = "Nguyen Arthur & Rodriguez Charlotte"
__version__ = "4.2"
__date__    = "2014-12-13"
__usage__   = """Play Mancala game"""
# ==============================================================================
import copy, time, os

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
def setoptions(command):
  """return dictionary containing union of default and user-defined options"""

  options = {'size':'6', 'seed':'5', 'rule':'kalah'}
  for i in range(len(command)):
    case = command[i].split('=')
    if (case[0] in options) and (len(case) == 2):
      options[case[0]] = case[1]
    else:
      print("be carefull, you wrote :",case,
            ", so it has not been taken into account.")      
  return options

# ==============================================================================
def ft_ask(ask, err):
    "do the try except thing"

    while True:
        try:
            result=input(ask)
            break
        except ValueError:
            print(err)
    return(result)

# ==============================================================================            
def ft_ask_pos(ask, err, cell_nb):
    """ask for pos in [1..cell_nb]"""

    strain = [str(i) for i in range(1, cell_nb + 1)]
    pos=0
    while (not (pos in strain)):
        pos=ft_ask(ask, err)
        if not (pos in strain):
            print("pos should be chosen in [1..",cell_nb,"]")
    return(pos)

# ==============================================================================
def ft_check_end(metalist, cell_nb, nb_seed):
    """ If one player has more than the half amount of total seed
        or if one player has no seeds, return True """
    
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
    """return true if oware can be executed (oware tried on a fake metalist)"""
    
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
    """take the other player's seeds if can do"""
    
    len_list = len(list_p)
    take_oppo  = False #bool #prevents from starving the other player
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
def ft_distrib(metalist, pos, player, rule):
    """Distribute the seeds. Return -1 if the box is empty, return 1 if valid,
    2 if the player can play again """

    result = 1
    if eval("metalist.j"+str(player))[pos-1] == 0:
        return(-1)
    list_p = eval("metalist.j"+str(player))
    list_op = eval("metalist.j"+str((player+1)%2))
    len_list = len(list_p)
    last_p = len_list-1 #index of the silo

    hand = list_p[pos-1] #taking the seeds from the selected box
    list_p[pos-1] = 0 #emptying the selected box

    while hand>0:

        list_p[pos] += 1
        hand -= 1
        if pos == last_p:
            if hand == 0:
                result = 2
            list_p, list_op = list_op, list_p      
            pos = 0
        else:
            pos +=1
    if result != 2: #if last seed not in silo
        ft_take_opposite(metalist, pos, player, list_p, list_op, rule, False, 0)
    return(result)

# ==============================================================================
def ft_greetings():
    """ Greets the user """

    #begin
    print("Follow the white rabbit...\n\n\n\n")
    time.sleep(1)
    print("Let's play Mancala!")
    time.sleep(1)
    print("You are free to change the setting if needed.\n")
    time.sleep(1)
    print("rule: awele, kalah, oware\n\n")
    #end
    return()

# ==============================================================================
def main() :
    """ Main function """

    #var
    meta_list = board()
    i = 0 #to determine which player is playing, J0 or J1
    pos = 0 #position of the cell entered by the player
    answer = -1
    line = ""
    
    #begin
    ft_greetings()
    line = ft_ask("enter this line with the desired options \n \"seed= size= rule=\": ",
                  "value error too bad")
    options = setoptions(line.split())
    nb_seed, cell_nb, rule = int(options['seed']), int(options['size']), options['rule']
    
    meta_list.ft_crealist(cell_nb,nb_seed)

    #TESTS:
##    meta_list.j1, meta_list.j0 = [1,0,2,0,0,3,0], [0,1,1,1,1,9,0]  #can take seed from adv
##    meta_list.j1, meta_list.j0 = [1,0,2,0,0,3,0], [0,0,0,0,1,3,0]  #can starve himself
##    meta_list.j1, meta_list.j0 = [1,0,0,0,0,3,0], [0,0,1,0,1,2,0]  #can not starve advers
##    meta_list.j1, meta_list.j0 = [1,2,2,0,0,1,0], [0,3,0,1,5,1,0]  #test oware
##    meta_list.j1, meta_list.j0 = [1,2,2,0,0,1,0], [0,3,0,1,5,1,74] #test check end

    print(meta_list) #First print of the board
    #boucle de jeu 
    while not ft_check_end(meta_list, cell_nb, nb_seed):
        print("player ",i%2," it's your turn")
        while answer!=1:
            if answer == 2 :
                print("player ", i%2, " can play again")
                print(meta_list)
            pos = int(ft_ask_pos("\nenter pos:","value error.try again",cell_nb))
            answer = ft_distrib(meta_list, pos, i%2, rule)
            if answer == -1:
                print("Rien dans la case")
            pos = 1
        print(meta_list)  
        answer = 0
        pos=0
        i+=1
    print("Player ",ft_check_end(meta_list, cell_nb, nb_seed),
          " you win the game. Congratulations.")
    input("Press any button to quit the game\n")
    return()
    #end

#-----------------------------------------------------------------------------------
if __name__ == "__main__" :
    main()
