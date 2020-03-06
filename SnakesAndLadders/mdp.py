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
    
    def __init__(self, nbrTraps,typeOfTraps): 
        self.layout = np.zeros(15)
        self.generateLayout(nbrTraps,typeOfTraps)
    
    def generateLayout(nbrTraps,typeOfTraps):
        for x in range(0,nbrTraps):
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
        diceRslt = rd.randint(0,1)
        Player.position += diceRslt
        return
    
    def throwNormalDice(self):
        if self.frozen == True :
            self.frozen = False
            return
        diceRslt = rd.randint(0,2)
        Player.position += diceRslt
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
        
 