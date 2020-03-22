import numpy as np
import random as rd



class Game:

    board = None
    circle = True
    movement = None
    player = None
    arrayExpected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #list of cost
    arrayDice = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #list of dice choice

    def __init__(self):
        self.board = Board(0, 0)
        self.player = Player()
        self.movement = Movement(self.player, self.board)

    def minDice(self, value1, value2):
        if value1 < value2:
            return value1, 1
        return value2, 2

    #function V returns Bellman's value
    #state represent on which case of the board we are
    #turn counts the number of iteration
    #the function returns in order:
    #   The chosen dice and the estimated cost in number of turn in the form of V
    def V(self, state):
        #CHeck si la case actuelle est la case finale
        if state == 15:
            return 0, 1 #The value of V is zero on the last case and the rest doesn't matter

        #For any other case
        else:

            if state != 3: #If there is only one accessible way
                valueDice1 = self.calculateValue(state, False, True)

                valueDice2 = self.calculateValue(state, False, False)

                minV, dice = self.minDice(valueDice1, valueDice2)

            else:#If there is more than one accessible way
                valueDice1 = self.calculateValue(state, False, True)/2\
                + self.calculateValue(state,True,True)/2

                valueDice2 = self.calculateValue(state, False, False)/2\
                + self.calculateValue(state, True, False)/2

                minV, dice = self.minDice(valueDice1, valueDice2)

            return minV, dice

    #returns the value at a certain state
    def calculateValue(self, state, takeShorcut, isSecurityDice):
        value = 1
        if isSecurityDice:
            diceRange = 2
        else:
            diceRange = 3
        for i in range(0, diceRange):
            tempFrozen = False
            tempFrozen, tempPosition = self.movement.calculateNextPosition(state, i, takeShorcut, isSecurityDice)
            value += self.arrayExpected[tempPosition]/diceRange
            if tempFrozen:
                value += 1/diceRange
        
        return value
        

    #returns the optimal decisions and their theoretical cost
    #needs a layout and if the board is circular or not
    def markovDecision(self, layout, circle):
        #sets the graph to be circular or not
        if circle:
            self.board.graph[15] = [1]
        else:
            self.board.graph[15] = [15]

        self.board.layout = layout

        
        #iterates trough the values to arrive to a converging function
        for _ in range(1, 1000):
            for i in range(1, 15):
                value, dice = self.V(i)
                self.arrayDice[i] = dice
                self.arrayExpected[i] = value

        #modifies the array to be the demanded form
        self.arrayExpected.pop(0)
        self.arrayExpected.pop(len(self.arrayExpected)-1)
        Expect = np.array(self.arrayExpected)

        #modifies the array to be the demanded form
        self.arrayDice.pop(0)
        self.arrayDice.pop(len(self.arrayDice)-1)
        Dice = np.array(self.arrayDice)

        #shows information
        markovDecisionsList = [Expect, Dice]
        print("layout")
        print(self.board.layout)
        print("dice")
        print(Dice)
        print("number of expected turn")
        print(Expect)

        return markovDecisionsList

class Board:

    #value of all the cases
    layout = np.ndarray([])
    #graph shows how to move on the board
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

    #generates traps randomly
    def generateLayout(self, nbrTraps, typeOfTraps):
        for _ in range(0, nbrTraps):
            rdPos = rd.randint(1, 13)
            while self.layout[rdPos] != 0:
                rdPos += 1

            self.layout[rdPos] = typeOfTraps
        return

#only has position for better clarity
class Player:
    position = 0

#in charge of the movement of the player
class Movement:

    player = None
    board = None
    frozen = False

    def __init__(self, player, board):
        self.player = player
        self.board = board

    #probability = 0.5
    def throwSecurityDice(self):
        self.move(rd.randint(0, 1))
        return

    #probability = 0.333..
    def throwNormalDice(self):
        self.move(rd.randint(0, 2))
        self.checkForTraps()
        return

    #applies the traps on the player
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
            for _ in range(0, 3):
                if self.player.position == 11:
                    self.player.position = 3
                else:
                    self.player.position -= 1
            if self.player.position < 1:
                self.player.position = 1
            return
        elif trapType == 3:
            self.frozen = True
            return


        return

    #makes the player move in a real game
    def move(self, nbrMv):
        if self.frozen == True:
            self.frozen = False
            return
        if self.player.position == 3 and nbrMv  > 0:
            self.player.position = self.board.graph[3][rd.randint(0, 1)]
            nbrMv -= 1

        for _ in range(0, nbrMv):
            self.player.position = self.board.graph[self.player.position][0]
        return

    #calculates where the player will end up
    def calculateNextPosition(self, state, nbrMv, takeShorcut, isSecurityDice):
        self.frozen = False
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

        return self.frozen, self.player.position


def markovDecision(layout, circle):
    a = Game()
    return a.markovDecision(layout,circle)
