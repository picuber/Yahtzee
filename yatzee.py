from random import randint as r
from functools import reduce

def userInput():
    return input('>>')

class Yahtzee:
    def __init__(self):
        self.running = False
        """Wether or not a game is running

        True: A game is currently running
        False: No game current running
        """

        self._score = [None for _ in range(13)]
        """A list of 13 entries for storing the throws which are used to score

        The score card consits of 13 boxes, seperated into upper section and lower section.
        Upper section: Ones, Twos, Threes, Fours, Fives, Sixes
        Lower section: Three of a Kind, Four of a Kind, Full House, Low Straight, High Straight, Yahtzee, Chance
        This List has stores them in this order.
        The values are the throws used to score for this box for a score or None for blank.
        """
        
        self._dice = [1, 1, 1, 1, 1]
        """A 5-tuple of the dice, displaying the latest thow"""

        self._throws_left = 3
        """Number of Throws left for this round.

        Each round can consit of up to thee throws.
        This variable stores the number of throws left for the current round.
        Possible values: 0, 1, 2, 3
        """

    @staticmethod
    def _diceToCount(dice): 
        """Converts the dice format to the count format.

        Arguments:
        dice    -- a list with 5 elements whose fields are the values of the individual dice (eg.: [3, 4, 2, 6, 4])

        Returns:
        a list with 6 elements whose fields denote the number of times each value occures (eg.: [0, 1, 1, 2, 0, 1])
        """
        if dice is None:
            return [0, 0, 0, 0, 0, 0]

        count = [0 for _ in range(6)]
        for die in dice:
            count[die-1] += 1
        return count

    @staticmethod
    def _isThreeOfAKind(dice):
        """Checks if the throw is a Three of a Kind

        Arguments:
        dice    -- a list of 5 dice 
        """
        count = Yahtzee._diceToCount(dice)
        return (count is not None) and ((3 in count) or (4 in count) or (5 in count))

    @staticmethod
    def _isFourOfAKind(dice):
        """Checks if the throw is a Four of a Kind

        Arguments:
        dice    -- a list of 5 dice 
        """
        count = Yahtzee._diceToCount(dice)
        return (count is not None) and ((4 in count) or (5 in count))

    @staticmethod
    def _isLowStraight(dice):
        """Checks if the throw is a low straight

        Arguments:
        dice    -- a list of 5 dice 
        """
        return (dice is not None) and (3 in dice) and (4 in dice) and (((1 in dice) and (2 in dice)) or ((2 in dice) and (5 in dice)) or ((5 in dice) and (6 in dice)))

    @staticmethod
    def _isHighStraight(dice):
        """
        True if the throw is a high straight, False otherwise

        Arguments:
        dice    -- a list of 5 dice 
        """
        return (dice is not None) and (2 in dice) and (3 in dice) and (4 in dice) and (5 in dice) and ((1 in dice) or (6 in dice))

    def _roll(self, reroll=[]):
        """Rolls the dice. If it is the first throw of the round reroll is ignored.

        Keyword Arguments:
        reroll    -- contanis the indices(0-4) of dice to reroll
        """
        self._throws_left -= 1
        for i in range(1, 6):
            if i in reroll:
                self._dice[i-1] = r(1, 6)

    def _getScore(self):
        """Calculates the current score.
        
        There are boni for getting more than 63 points in the upper section and multiple Yahtzees including the Yahtzee box

        Returns:
        A list with 16 integers.
        Index 0-12 are the same as in the score card.
        Index 13 and 14 are upper section bonus and Yahtzee bonus respectively.
        Index 15 is the total sum.
        """
        score = [0 for _ in range(16)]
        
        #upper section
        for i in range(6):
            score[i] = Yahtzee._diceToCount(self._score[i])[i] * (i+1)

        score[13] = 35 if sum(score[:6]) >= 63 else 0

        #lower section
        score[6] = sum(self._score[6]) if Yahtzee._isThreeOfAKind(self._score[6]) else 0
        score[7] = sum(self._score[7]) if Yahtzee._isFourOfAKind(self._score[7]) else 0
        score[8] = 25 if (2 in Yahtzee._diceToCount(self._score[8])) and (3 in Yahtzee._diceToCount(self._score[8])) else 0
        score[9] = 30 if Yahtzee._isLowStraight(self._score[9]) else 0
        score[10] = 40 if Yahtzee._isHighStraight(self._score[10]) else 0
        if 5 in Yahtzee._diceToCount(self._score[11]):
            score[11] = 50
            score[14] = 0
            for i in range(13): #boni for multiple Yahtzees
                if i == 11: #is the Yahtzee slot
                    continue
                if 5 in Yahtzee._diceToCount(self._score[i]):
                    score[14] += 100
        score[12] = sum(self._score[12]) if self._score[12] is not None else 0
        score[15] = sum(score)
        return score

    def _printScoreCard(self):
        """Prints the whole score card to stdout"""
        score = self._getScore()
        print('\n'
              '~~~~~Score Card~~~~~\n'
              '-----Upper Section-----\n'
              '[1]Ones \t\t{0[0]} = {1[0]}\n'
              '[2]Twos \t\t{0[1]} = {1[1]}\n'
              '[3]Threes \t\t{0[2]} = {1[2]}\n'
              '[4]Fours \t\t{0[3]} = {1[3]}\n'
              '[5]Fives \t\t{0[4]} = {1[4]}\n'
              '[6]Sixes \t\t{0[5]} = {1[5]}\n'
              'Sum Upper Section = {2}\n'
              '\n'
              '-----Lower Section-----\n'
              '[7]Three of a Kind \t{0[6]} = {1[6]}\n'
              '[8]Four of a Kind \t{0[7]} = {1[7]}\n'
              '[9]Full House \t\t{0[8]} = {1[8]}\n'
              '[10]Low Straight \t{0[9]} = {1[9]}\n'
              '[11]High Straight \t{0[10]} = {1[10]}\n'
              '[12]Yahtzee \t\t{0[11]} = {1[11]}\n'
              '[13]Chance \t\t{0[12]} = {1[12]}\n'
              'Sum Lower Section = {3}'
              '\n'
              '-----Boni-----\n'
              'Upper Section Bonus = {1[13]}\n'
              'Multi-Yahtzee Bonus = {1[14]}\n'
              '\n'
              'Total Score: {1[15]}'
              '~~~~~~~~~~'
              ''.format(self._score, score, sum(score[:6]), sum(score[6:13]))
              )

    def run(self):
        """Runs the game.
        
        The game is played inside this method.
        Score and dice will be reinitialized in the beginning.
        Will end gracefully if KeyboardInterrupt is caught
        """
        self._score = [None for _ in range(13)]
        self._dice = [1, 1, 1, 1, 1]

        if self.running == True:
            print('This game is already running. Wait until it\'s over or start a different game')
        try:
            print('Welcome to a game of Yahtzee!')
            for i in range(1, 14):# There are 13 rounds in a game of Yahtzee
                print('Round {0}'.format(i))
                self._throws_left = 3 #There are up to 3 throws per round
                reroll = [1, 2, 3, 4, 5] #which dice to reroll
                while self._throws_left > 0:
                    self._roll(reroll)
                    print('You rolled {0}'.format(self._dice))
                    if self._throws_left > 0: #Was not last throw
                        print('If you want to keep this throw just hit Enter.\n'
                              'If you want to reroll enter the which dice to reroll. [any numbers betweet 1 and 5]\n'
                              '(Throws left: {0})'.format(self._throws_left))
                        reroll = []
                        uin = userInput()
                        for k in range(1, 6):
                            if str(k) in uin:
                                reroll += [k]
                        if reroll == []:
                            break
                #thow decided, now put it onto the score card
                self._printScoreCard()
                print('Where do you want to score? [any number between 1 and 13]')
                while True: #get userInput
                    try:
                        uin = int(userInput())
                    except ValueError:
                        print('Please enter a number between 1 and 13 inclusive')
                        continue
                    if not 1 <= uin <= 13:
                        print('Please enter a number between 1 and 13 inclusive')
                        continue
                    elif self._score[uin-1] is not None:
                        print('This box is already filled! Please choose another!')
                        continue
                    else:
                        break
                self._score[uin-1] = self._dice[:] #put the current throw to the specified box in the score card
                print('Added to score card')
                self._printScoreCard()
            print('The game has ended.')
            print('The final score is {0[15]}'.format(self._getScore()))
            self.running = False
        except KeyboardInterrupt:
            self.running = False
            print()

if __name__ == '__main__':
    yahtzee = Yahtzee()
    yahtzee.run()
