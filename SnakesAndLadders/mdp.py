import numpy as np
import random as rd



class Game:

    board = None
    circle = False
    movement = None
    player = None

    def __init__(self):
        self.board = Board(10, 1)
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

    #fonction V qui retourne la valeur de Belleman,
    # state represent la case surlaquelle on se trouve
    # tour compte le nombre d'iteration
    #la fonction retourne dans l'ordre: la valeur calculé, le dé choisit, et le coût en nombre de tour
    def V(self, state, tour):

        #CHeck si la case actuelle est la case finale
        if state == 15 or tour > 10:
            return 0, 1, tour # La valeur V vaut 0 sur la case finale, le choix du dé n'a ici pas d'importance, et le nombre de tour.

        #Si on est sur une autre case
        else:
            tour += 1 #on itere d'abord le nombre de tour
            
            #Si il n y a qu'une case joignable
            if state != 3:

                #ici on calcule l'équation si on devait choisir le dé sécurité
                nextV , nextDice, tourTotal= self.V(self.movement.calculateNextPosition(state,1,False,True), tour)
                valueDice1 = 1 + nextV/2


                # cas particulier si on est sur la case 10 ou 14, donc une case avant la case finale
                #Si on modifie le graphe en rajoutant 15:[15] ou 15:[1] alors on peut virer les 2 conditions suivantes
                if state == 10 or state == 14:
                    valueDice2 = 1
                else :

                    #Puis on clacul l'équation so on devait choisir le dé normal
                    
                    nextV, nextDice, tourA = self.V(self.movement.calculateNextPosition(state,1,False,False),tour)
                    nextNextV, nextNextDice, tourB = self.V(self.movement.calculateNextPosition(state,2,False,False),tour)
                    #On calcul le nombre de tour minimum possible entre les 2 chemins.
                    tourTotal = self.minTour(tourA, tourB)
                    valueDice2 = 1 + nextV/3 + nextNextV/3

                #On selection le dé qui possède la plus petite valeure entre les 2 calculées juste avant
                valueDice, dice = self.min(valueDice1, valueDice2)


            #Si il y a 2 case joignabe ( par exemple sur la case 3 on peut joindre 4 et 11)
            else:

                #on calcul donc une première fois pour le premier chemin.

                #ici on calcule l'équation si on devait choisir le dé sécurité
                nextV , nextDice, tourTotal1= self.V(self.movement.calculateNextPosition(state,1,False,True), tour)
                valueDice1 = 1 + nextV/2

                # cas particulier si on est sur la case 10 ou 14, donc une case avant la case finale
                #Si on modifie le graphe en rajoutant 15:[15] ou 15:[1] alors on peut virer les 2 conditions suivantes
                
                nextV , nextDice, tourA= self.V(self.movement.calculateNextPosition(state,1,False,False), tour)
                nextNextV, nextNextDice, tourB = self.V(self.movement.calculateNextPosition(state,2,False,False), tour)
                #On calcul le nombre de tour minimum possible entre les 2 chemins.
                tourTotal1 = self.minTour(tourA,tourB)
                valueDice2 = 1 + nextV/3 + nextNextV/3

                #On selection le dé qui possède la plus petite valeure entre les 2 calculées juste avant
                a1, diceFirst = self.min(valueDice1, valueDice2)


                #on calcul ensuite pour le 2ieme chemin possible


                #ici on calcule l'équation si on devait choisir le dé sécurité
                nextV , nextDice, tourTotal2= self.V(self.movement.calculateNextPosition(state,1,True,True), tour)
                valuedice1 = 1 + nextV/2

                # cas particulier si on est sur la case 10 ou 14, donc une case avant la case finale
                #Si on modifie le graphe en rajoutant 15:[15] ou 15:[1] alors on peut virer les 2 conditions suivantes
                
                nextV , nextdice, tour2A= self.V(self.movement.calculateNextPosition(state,1,True,False), tour)
                nextNextV, nextNextdice, tour2B = self.V(self.movement.calculateNextPosition(state, 2 ,True,False), tour)
                #On calcul le nombre de tour minimum possible entre les 2 chemins.
                tourTotal2= self.minTour(tour2A,tour2B)
                valuedice2 = 1 + nextV/3 + nextNextV/3

                #On selection le dé qui possède la plus petite valeure entre les 2 calculées juste avant
                a2, diceSecond = self.min(valuedice1, valuedice2)



                #Ici on sélection le chemin qui possède la plus petite valeure
                valueDice, dice, tourTotal= self.minValue(a1, diceFirst,a2, diceSecond, tourTotal1, tourTotal2)

            return valueDice, dice, tourTotal




    def markovDecision(self, layout, circle):

        arrayExpected = [] #liste du cout
        arrayDice = [] #list du choix de dé
        arrayV=[] #list de la valeur V

        for i in range(1,15):
            value, dice, tour = self.V(i, 0)
            arrayExpected.append(tour)
            arrayDice.append(dice)
            arrayV.append(value)

        Expect = np.array(arrayExpected)
        Dice = np.array(arrayDice)
        markovDecisionsList = [Expect,Dice]
        print("layout")
        print(self.board.layout)
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
             14: [15],
             15: [15]}

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
        self.move(rd.randint(0,1))
        return

    #probability = 0.333..
    def throwNormalDice(self):
        self.move(rd.randint(0,2))
        self.checkForTraps()
        return

    def checkForTraps(self):

        trapType = self.board.layout[self.player.position-1]

        if trapType == 4:
            trapType = rd.randint(1,3)

        if trapType == 0:
            return
        elif trapType == 1:
            self.player.position = 1
            return
        elif trapType == 2:
            self.player.position-=3
            if self.player.position < 1:
                self.player.position = 1
            return
        elif trapType == 3:
            self.frozen
            return


        return

    def move(self, nbrMv):
        if self.frozen == True :
            self.frozen = False
            return
        if self.player.position == 3 and nbrMv > 0:
            self.player.position = self.board.graph[3][rd.randint(0,1)]
            nbrMv -= 1

        for i in range(0,nbrMv):
            if self.player.position == 3:
                self.player.position = self.board.graph[self.player.position][0]
            else:
                self.player.position = self.board.graph[self.player.position]
        return

    def calculateNextPosition(self, state, nbrMv, takeShorcut, isSecurityDice):
        self.player.position = state
        if self.frozen == True :
            self.frozen = False
            return
        if self.player.position == 3 and nbrMv > 0:
            if takeShorcut:
                self.player.position = self.board.graph[3][1]
            else:
                self.player.position = self.board.graph[3][0]
            nbrMv -= 1
            
        for i in range(0,nbrMv):
            if self.player.position == 3:
                self.player.position = self.board.graph[self.player.position][0]
            else:
                self.player.position = self.board.graph[self.player.position][0]
            
        if isSecurityDice == False:
            self.checkForTraps()
        
        return self.player.position

if __name__ == "__main__":
    a = Game()
