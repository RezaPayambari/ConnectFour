import sys
import random

__version__ = '1.0'
__author__ = 'Reza Payambari (reza.payambari@students.tbs1.de)'

class ConnectFour(object):
    def __init__(self):
        # self.opponent     1 || 2
        self.rows = 6  # 6 ≤ x
        self.cols = 7  # 7 ≤ x
        self.empty = '---'
        self.newline = 42
        self.pos = {}
        self.player = {
            1: {
                'name': 'Player 1',
                'marker': 'X'
            },
            2: {
                'name': 'Player 2',
                'marker': 'O'
            }
        }
        self.whois = random.randint(1, 2)

        self.game = []
        self.cols_filled = []
        self.latest = {}  # player, position

    # new round, if has winner, print winner else print no winner
    def newRound(self, has_winner=False):
        print('---')

        if has_winner:
            print('Congrats {0}, you won the match!'.format(self.player[self.latest['player']]['name']))
        else:
            print('Game over, no one won!')


    # set opponent
    def setOpponent(self, opponent):
        if opponent.isnumeric():
            if int(opponent) in [1, 2]:
                self.opponent = int(opponent)
                return True

    # set rows
    def setRows(self, rows):
        if rows.isnumeric():
            if int(rows) >= 6:
                self.rows = int(rows)
                return True

    # set cols
    def setCols(self, cols):
        if cols.isnumeric():
            if int(cols) >= 7:
                self.cols = int(cols)
                return True

    # calculate diagonal, horizontal and vertical
    def calculate(self):
        self.pos = {
            'n': - self.cols,
            'no': - (self.cols - 1),
            'o': + 1,
            'so': + (self.cols + 1),
            's': + self.cols,
            'sw': + (self.cols - 1),
            'w': - 1,
            'nw': - (self.cols + 1)
        }
        return True

    # start here, first call
    def start(self,player="1"):
        print('ConnectFour')
        self.setOpponent(player)
        # calculate nw, n, no, o, os, s, sw, w
        self.calculate()

        # build game
        self.buildGame()

        # start round
        self.round()

    # build game field
    def buildGame(self):
        for i in range(0, (self.rows * self.cols)):
            self.game.append(self.empty)

        return True

    # build game field ui
    def buildField(self):
        line = '|'
        for i in range(0, len(self.game)):
            line += '{0}|'.format(self.game[i].center(len(self.empty), ' '))
            if (i + 1) % self.cols == 0:
                print(line)
                line = '|'

        cols = '|';
        for i in range(1, self.cols + 1):
            cols += '{0}|'.format(str(i).center(len(self.empty), ' '))

        print(cols)

    # change who is next player
    def changeWhois(self):
        if self.whois == 2:
            self.whois = 1
        else:
            self.whois = 2

    # one round, one print of game field
    def round(self):
        # clear screen using prints
        for i in range(0, self.newline):
            print('\n')

        # build field
        self.buildField()

        # new round if game has winner
        if self.has_winner():
            self.newRound(True)

        # new round if cols_filled count = cols count => every col is filled
        if len(self.cols_filled) == self.cols:
            self.newRound(False)

        if self.opponent == 1 and self.whois == 2:
            # computer action
            step = self.brain()
        else:
            # user action
            step = input(
                '\n{0} in the row:\nplease give a number, to set your "{1}" into position:\n>>> '.format(
                    self.player[self.whois]['name'], self.player[self.whois]['marker']))

            while step.isnumeric() == False:
                print('please choose a number between 1 and {0}!'.format(self.cols))
                step = input(
                    '\n{0} in the row:\n>>> please give a number, to set your "{1}" into position: '.format(
                        self.player[self.whois]['name'], self.player[self.whois]['marker']))

            while step.isnumeric() and int(step) > self.cols:
                print('just a number between 1 and {0} is possible!'.format(self.cols))
                step = input(
                    '\n{0} in the row:\n>>> please choose a number, to set your "{1}" into position: '.format(
                        self.player[self.whois]['name'], self.player[self.whois]['marker']))

            while step.isnumeric() and int(step) in self.cols_filled:
                print('{0} already completely occupied'.format(self.cols_filled))
                step = input(
                    '\n{0} in the row:\n>>> please choose a number, to set your "{1}" into position: '.format(
                        self.player[self.whois]['name'], self.player[self.whois]['marker']))

        # position
        step = int(step)
        position = len(self.game) - (self.cols - (step - 1))

        while self.game[position] != self.empty:
            position -= self.cols
        else:
            # is in first line, so its the highest disc, so row is filled
            if position < self.cols:
                self.cols_filled.append(step)

            # set marker in field
            self.game[position] = self.player[self.whois]['marker']

        # set latest things
        self.latest['player'] = self.whois
        self.latest['position'] = position

        # change whois to other player 1 <=> 2
        self.changeWhois()

        # new round
        self.round()

    # check if there is a winner with latest marker
    def has_winner(self, latest={}):
        # if there is not latest player, latest position set, thats the beginning
        if len(latest) == 0:
            latest = self.latest

        if len(latest) != 2:
            return False

        # d1 = diagonal left top to right bottom
        # d2 = diagonal right top to left bottom
        # h = horizintal
        # d = diagonal
        possible = {
            'd1': {'is': 1, 'check': [self.pos['nw'], self.pos['so']]},
            'd2': {'is': 1, 'check': [self.pos['no'], self.pos['sw']]},
            'h': {'is': 1, 'check': [self.pos['o'], self.pos['w']]},
            'v': {'is': 1, 'check': [self.pos['n'], self.pos['s']]}
        }

        # marker
        marker = self.player[latest['player']]['marker']
        start = latest['position']

        for p in possible:
            for i in possible[p]['check']:
                pos = start + i

                while pos != False and pos >= 0 and pos <= len(self.game) - 1 and self.game[pos] == marker:
                    possible[p]['is'] += 1

                    if p in ['d1', 'd2']:
                        if (pos + 1) % self.cols == 0 or pos % self.cols == 0 or pos >= len(
                                self.game) - self.cols or pos <= self.cols:
                            pos = False
                        else:
                            pos += i
                    elif p == 'h':
                        if (pos + 1) % self.cols == 0 or pos % self.cols == 0:
                            pos = False
                        else:
                            pos += i
                    elif p == 'v':
                        if pos >= len(self.game) - self.cols or pos <= self.cols:
                            pos = False
                        else:
                            pos += i

                if possible[p]['is'] >= 4:
                    # print(p)
                    return True

        return False

    # the brain, the bot
    def brain(self):
        percentage_me = {}
        percentage_him = {}
        for i in range(1, self.cols + 1):
            percentage_me[i] = 0
            percentage_him[i] = 0

        if len(self.latest) != 2:
            # select middle:
            return (self.cols + 1) // 2

        win_me = False
        win_him = False

        for step in range(1, self.cols + 1):
            if step not in self.cols_filled:
                latest_me = {}
                latest_him = {}

                # position
                position = len(self.game) - (self.cols - (step - 1))

                while self.game[position] != self.empty:
                    if self.game[position] == self.player[1]['marker']:
                        percentage_him[step] += 1
                    elif self.game[position] == self.player[2]['marker']:
                        percentage_me[step] += 1

                    position -= self.cols

                latest_me['player'] = 2
                latest_me['position'] = position
                latest_him['player'] = 1
                latest_him['position'] = position

                if self.has_winner(latest_me):
                    win_me = step

                if self.has_winner(latest_him):
                    win_him = step

        if win_me != False:
            return win_me
        if win_him != False:
            return win_him

        sorted_me = sorted(percentage_me.items(), key=lambda item: item[1], reverse=True)
        sorted_him = sorted(percentage_him.items(), key=lambda item: item[1], reverse=True)

        if sorted_me[0][1] > sorted_him[0][1]:
            return sorted_me[0][0]
        elif sorted_me[0][1] < sorted_him[0][1]:
            return sorted_him[0][0]
        elif sorted_me[0][1] == sorted_him[0][1]:
            if sorted_me[0][1] == 0:
                rand = random.randint(1, self.cols)
                while rand in self.cols_filled:
                    rand = random.randint(1, self.cols)
                return rand
            else:
                return sorted_me[0][0]


# start new instance of Connect4
c4 = ConnectFour()
c4.start()
