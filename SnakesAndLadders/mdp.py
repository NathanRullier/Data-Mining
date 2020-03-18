import numpy as np
import random as rd

from matplotlib._text_layout import layout


class Game:

    board = None
    circle = False
    movement = None
    player = None

    def __init__(self):
        self.board = Board(0, 0)
        self.player = Player()
        self.movement = Movement(self.player, self.board)
        self.markovDecision(self.board.layout, self.circle)

    def min(self, a, b):
        if a < b:
            return a
        else:
            return b

    def V(self, state):
        print(state)
        if state == 15:
            return 0

        else:
            nextState = self.board.graph[state]
            if len(nextState) == 1:
                dice1 = 1 + self.V(nextState[0])/2
                if state == 14:
                    dice2 = 1
                if state == 10:
                    dice2 = 1
                else:
                    dice2 = 1 + self.V(nextState[0])/3 + self.V(self.board.graph[nextState[0]][0])/3
                a = min(dice1, dice2)

            if len(nextState) == 2:
                dice1 = 1 + self.V(nextState[0])/2
                if state == 14:
                    dice2 = 1
                else:
                    dice2 = 1 + self.V(nextState[0])/3 + self.V(self.board.graph[nextState[0]][0])/3
                a1 = min(dice1, dice2)
                dice1 = 1 + self.V(nextState[1])/2
                if state == 14:
                    dice2 = 1
                else:
                    dice2 = 1 + self.V(nextState[1])/3 + self.V(self.board.graph[nextState[1]][0])/3
                a2 = min(dice1, dice2)

                a = min(a1, a2)
            return a




    def markovDecision(layout, lay , circle):

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

    def generateLayout(self, nbrTraps,typeOfTraps):
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

    #probabilité = 0.5
    def throwSecurityDice(self):
        if self.frozen == True :
            self.frozen = False
            return
        self.move(rd.randint(0,1))
        return

    #probability = 0.333..
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


if __name__ == "__main__":
    a = Game()
    b = a.V(1)
