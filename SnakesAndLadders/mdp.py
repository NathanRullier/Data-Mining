import numpy as np
import random as rd

class Game:
    
    board = None
    circle = False
    movement = None
    player = None
    
    def __init__(self): 
        self.board = Board(0,0)
        self.player = Player()
        self.movement = Movement(self.player,self.board)
        self.markovDecision(self.board.layout, self.circle)

    def markovDecision(layout, circle): 
        Expect = np.array([]);
        Dice = np.array([]);
        markovDecisionsList = [Expect,Dice]
        return markovDecisionsList

class Board:
    
    layout = np.ndarray([])
    graph = {1: [2],
             2: [3],
             3: [4,11],
             4: [5],
             5: [6],
             6: [7],
             7: [8],
             8: [9],
             9: [10],
             10: [15],
             11: [12],
             12: [13],
             13: [14],
             14: [15]}
    
    def __init__(self, nbrTraps,typeOfTraps): 
        self.layout = np.zeros(15)
        self.generateLayout(nbrTraps,typeOfTraps)
    
    def generateLayout(nbrTraps,typeOfTraps):
        for i in range(0,nbrTraps):
            rdPos = rd.randint(1,13)
            while layout[rdPos] != 0 :
                ++rdPos
                
            layout[rdPos]= typeOfTraps
        return
            
class Traps :
    typeOfTrap = 0;
    
class Player :
    position = 0
    
class Movement:
    
    player = None
    board = None
    frozen = False
    
    def __init__(self, player, board): 
        self.player = player
        self.board = board
        
    def throwSecurityDice(self):
        if self.frozen == True :
            self.frozen = False
            return
        self.move(rd.randint(0,1))
        return
    
    def throwNormalDice(self):
        if self.frozen == True :
            self.frozen = False
            return
        self.move(rd.randint(0,2))
        self.checkForTraps()
        return
    
    def checkForTraps(self):
        
       trapType = self.board.layout[self.player.position]
       
       if trapType == 4:
           trapType = rd.randint(1,3)
       
       if trapType == 0:
           return
       elif trapType == 1:
           self.player.position = 0
           return
       elif trapType == 2:
           self.player.position-=3
           if self.player.position < 0:
               self.player.position = 0
           return
       elif trapType == 3:
           self.frozen
           return
           
                     
       return
   
    def move(self, nbrMv):
        if self.player.position == 3 and nbrMv > 0:
            self.board.graph[3[rd.randint(0,1)]]
            --nbrMv
            
        for i in range(0,nbrMv):
            self.player.position = self.board.graph[self.player.position]
        return
        
