import numpy as np
import random as rd

class Game:
    
    board = None
    circle = False
    
    def __init__(self): 
        self.board = Board(0,0)
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
            if typeOfTraps == 4 :
                layout[rdPos]= rd.randint(1,4)
            else :
                layout[rdPos]= typeOfTraps
        return
            
class Traps :
    typeOfTrap = 0;
    
class Player :
    position = 0
    
class Dices:
    
    player = None
    
    def __init__(self, player): 
        self.player = player
        
        
    def throwSecurityDice():
        diceRslt = rd.randint(0,1)
        Player.position += diceRslt
        return
    
    def throwNormalDice():
        diceRslt = rd.randint(0,2)
        Player.position += diceRslt
        self.checkForTraps()
        return
    
    def checkForTraps():
        return
 