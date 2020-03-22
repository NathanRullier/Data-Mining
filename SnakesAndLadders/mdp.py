import numpy as np
import random as rd



class Game:

    board = None
    circle = False
    movement = None
    player = None
    arrayExpected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #liste du cout
    arrayDice = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #list du choix de dé

    def __init__(self):
        self.board = Board(4, 4)
        self.player = Player()
        self.movement = Movement(self.player, self.board)
        self.markovDecision(self.board.layout, self.circle)

    def minDice(self, value1, value2):
        if value1 < value2:
            return value1, 1

        return value2, 2

    #function V returns Bellman's value
    #state represent on which case of the board we are
    #turn counts the number of iteration
    #the function returns in order:
    #   The chosen dice and the estimated cost in number of turn in the form of V
    def V(self, state, turn):
        #CHeck si la case actuelle est la case finale
        isFreeze = self.board.layout[state] == 3
        moveCost = 1
        if isFreeze:
            moveCost = 2
        if state == 15:
            return 0, 1 #The value of V is zero on the last case and the rest doesn't matter

        #Si on est sur une autre case
        else:
            turn += 1 #on itere d'abord le nombre de turn

            #Si il n y a qu'une case joignable
            if state != 3:
                valueDice1 = moveCost\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 0, False, True)]/2\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 1, False, True)]/2

                valueDice2 = moveCost\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 0, False, False)]/3\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 1, False, False)]/3\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 2, False, False)]/3

                minV, dice = self.minDice(valueDice1, valueDice2)

            else:
                valueDice1 = moveCost\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 0, False, True)]/4\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 1, False, True)]/4\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 0, True, True)]/4\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 1, True, True)]/4

                valueDice2 = moveCost\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 0, True, False)]/6\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 1, True, False)]/6\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 2, True, False)]/6\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 0, False, False)]/6\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 1, False, False)]/6\
                + self.arrayExpected[self.movement.calculateNextPosition(state, 2, False, False)]/6

                minV, dice = self.minDice(valueDice1, valueDice2)

            return minV, dice




    def markovDecision(self, layout, circle):
        if circle:
            self.board.graph[15] = [1]
        else:
            self.board.graph[15] = [15]
        for _ in range(1, 1000):
            for i in range(1, 15):
                value, dice = self.V(i, 0)
                self.arrayDice[i] = dice
                self.arrayExpected[i] = value

        Expect = np.array(self.arrayExpected)
        Dice = np.array(self.arrayDice)
        markovDecisionsList = [Expect, Dice]
        print("layout")
        print(self.board.layout)
        print("dice")
        print(Dice)
        print("number of expected turn")
        print(Expect)

        return markovDecisionsList

class Board:

    layout = np.ndarray([])
    graph = {1: [2],
             2: [3],
             3: [4, 11],
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

    def generateLayout(self, nbrTraps, typeOfTraps):
        for _ in range(0, nbrTraps):
            rdPos = rd.randint(1, 13)
            while self.layout[rdPos] != 0:
                rdPos += 1

            self.layout[rdPos] = typeOfTraps
        return

class Player:
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
        self.move(rd.randint(0, 1))
        return

    #probability = 0.333..
    def throwNormalDice(self):
        self.move(rd.randint(0, 2))
        self.checkForTraps()
        return

    def checkForTraps(self):

        trapType = self.board.layout[self.player.position-1]

        if trapType == 4:
            trapType = rd.randint(1, 3)

        if trapType == 0:
            return
        elif trapType == 1:
            self.player.position = 1
            return
        elif trapType == 2:
            self.player.position -= 3
            if self.player.position < 1:
                self.player.position = 1
            return
        elif trapType == 3:
            self.frozen = True
            return


        return

    def move(self, nbrMv):
        if self.frozen == True:
            self.frozen = False
            return
        if self.player.position == 3 and nbrMv > 0:
            self.player.position = self.board.graph[3][rd.randint(0, 1)]
            nbrMv -= 1

        for _ in range(0, nbrMv):
            self.player.position = self.board.graph[self.player.position][0]
        return

    def calculateNextPosition(self, state, nbrMv, takeShorcut, isSecurityDice):
        self.player.position = state
        if self.player.position == 3 and nbrMv > 0:
            if takeShorcut:
                self.player.position = self.board.graph[3][1]
            else:
                self.player.position = self.board.graph[3][0]
            nbrMv -= 1

        for _ in range(0, nbrMv):
            self.player.position = self.board.graph[self.player.position][0]
        if isSecurityDice == False:
            self.checkForTraps()

        return self.player.position

if __name__ == "__main__":
    a = Game()
