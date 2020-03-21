import numpy as np
import random as rd



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

    def min(self,a, b):
        if a < b:
            return a, 1
        else:
            return b, 2

    def minTour(self,a, b):
        if a < b:
            return a
        else:
            return b

    def minValue(self, a, valueA, b, valueB, tour1, tour2):
        if a < b:
            return a, valueA, tour1
        else:
            return b, valueB, tour2

    def V(self, state, tour):
        if state == 15:
            return 0, 1, tour

        else:
            tour = tour +1
            nextState = self.board.graph[state]
            if len(nextState) == 1:
                nextV , nextdice, tourTotal= self.V(nextState[0], tour)
                valuedice1 = 1 + nextV/2

                if state == 10:
                    valuedice2 = 1
                else:
                    if state == 14:
                        valuedice2 = 1
                    else:
                        nextV , nextdice, tourA= self.V(nextState[0],tour)
                        nextnextV, nextnextdice, tourB = self.V(self.board.graph[nextState[0]][0],tour)
                        tourTotal = self.minTour(tourA, tourB)
                        valuedice2 = 1 + nextV/3 + nextnextV/3

                a, dice = self.min(valuedice1, valuedice2)

            if len(nextState) == 2:
                nextV , nextdice, tourTotal1= self.V(nextState[0], tour)
                valuedice1 = 1 + nextV/2
                if state == 14:
                    valuedice2 = 1
                else:
                    nextV , nextdice, tourA= self.V(nextState[0], tour)
                    nextnextV, nextnextdice, tourB = self.V(self.board.graph[nextState[0]][0], tour)
                    tourTotal1 = self.minTour(tourA,tourB)
                    valuedice2 = 1 + nextV/3 + nextnextV/3

                a1, diceFirst = self.min(valuedice1, valuedice2)

                nextV , nextdice, tourTotal2= self.V(nextState[0], tour)
                valuedice1 = 1 + nextV/2
                if state == 14:
                    valuedice2 = 1
                else:
                    nextV , nextdice, tour2A= self.V(nextState[0], tour)
                    nextnextV, nextnextdice, tour2B = self.V(self.board.graph[nextState[0]][0], tour)
                    tourTotal2= self.minTour(tour2A,tour2B)
                    valuedice2 = 1 + nextV/3 + nextnextV/3

                a2, diceSecond = self.min(valuedice1, valuedice2)

                a, dice, tourTotal= self.minValue(a1, diceFirst,a2, diceSecond, tourTotal1, tourTotal2)

            return a, dice, tourTotal




    def markovDecision(self, layout, circle):

        arrayExpected = []
        arrayDice = []
        arrayV=[]

        for i in range(1,15):
            value, dice, tour = self.V(i, 0)
            arrayExpected.append(tour)
            arrayDice.append(dice)
            arrayV.append(value)

        print("dice")
        print(arrayDice)
        print("number of expected tour")
        print(arrayExpected)
        print("value of Markov equation")
        print(arrayV)
        Expect = np.array(arrayExpected)
        Dice = np.array(arrayDice)
        markovDecisionsList = [Expect,Dice]

        print("dice")
        print(Dice)
        print("number of expected tour")
        print(Expect)
        print("value of Markov equation")
        print(arrayV)

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

    def __init__(self, nbrTraps, typeOfTraps):
        self.layout = np.zeros(15)
        self.generateLayout(nbrTraps, typeOfTraps)

    def generateLayout(self, nbrTraps,typeOfTraps):
        for i in range(0, nbrTraps):
            rdPos = rd.randint(1,13)
            while self.layout[rdPos] != 0 :
                rdPos+=1

            self.layout[rdPos]= typeOfTraps
        return

class Traps :
    typeOfTrap = 0

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
            self.player.position = self.board.graph[3][rd.randint(0,1)]
            nbrMv -= 1

        for i in range(0,nbrMv):
            self.player.position = self.board.graph[self.player.position]
        return

    def calculateNextPosition(self, nbrMv, takeShorcut):
        if self.player.position == 3 and nbrMv > 0:
            if takeShorcut:
                self.player.position = self.board.graph[3][1]
            else:
                self.player.position = self.board.graph[3][0]
            nbrMv -= 1
            
        for i in range(0,nbrMv):
            self.player.position = self.board.graph[self.player.position]
        return

if __name__ == "__main__":
    a = Game()
