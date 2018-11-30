from sys import stdout

__version__ = '1.0'
__author__ = 'Reza Payambari (reza.payambari@students.tbs1.de)'


# Spieler
NONE=0
SPIELER_1=1
SPIELER_2=2



# Game Board
class Gameboard:

    COL=7
    ROW=6
    WIN=4

    DEFAULT=". "
    PLAYER1="x "
    PLAYER2="o "

    aktueller_spieler=0
    gewinner=""
    fields = 42

    def __init__(self):
        beendet=False

    def einwurf(self, spalte=0):
        if self.fields>0:
            self.fields=self.fields-1
        else:
            pass
            # Game ends

    def draw(self):
        col=0
        for col in range(0,self.ROW):
            for col in range(0,self.COL):
                stdout.write(self.DEFAULT)
            print()

    def gewinnpruefung(self):
        pass

    def spieler_wechseln(self):
        pass

    def column_Full(self,spalte=0):
        pass


class Player:
    name="Player"
    color=""
    turn=False


class Game:
    def __init__(self):
        pass

    def start(self):
        pasambieri = Gameboard()
        pasambieri.draw()

philipp=Game()

philipp.start()