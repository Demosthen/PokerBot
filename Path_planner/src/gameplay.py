"""
Gameplay Class
"""

import Point

class gameplay(object):
    """
    Gameplay class that keeps track of the game state,
    baxter's cards and returns a next move.
    """
    def __init__(self, current_cards):
        """
        Constructor. 
        
        Inputs:
        current_cards: the list of Point objects of all
        the cards currently on the table. The most recently
        played card index 0.
        
        """
        self.center_card = current_cards[0]
        self.rem_deck = current_cards[1]
        self.my_cards = current_cards[2:]
        print('this works!')


def main():
    print('testing')
    point1 = new Point
    points = [1, 2, 3]
main()