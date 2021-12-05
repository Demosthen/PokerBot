"""
Gameplay Class
"""

from geometry_msgs.msg import Point

class gameplay(object):
    """
    Gameplay class that keeps track of the game state,
    baxter's cards and returns a next move.
    """
    def __init__(self, current_cards):
        """
        Constructor. 
        
        Inputs:
        current_cards: the list of Point objects and strings of all
        the cards currently on the table. The most recently
        played card index 0.
        [["4D", Point], ["10H", Point], ...]
        
        """
        self.center_card = current_cards[0]
        self.deck_of_cards = current_cards[1]
        self.baxter_hand = current_cards[2:]
        self.turn = "baxter"
    
    # Compares the most recently played card to its own, and 
    def compare_cards():
        target_card = []
        for card in self.baxter_hand:
            # Card[0] accesses the coords, Card[1] is the string that contains the type
            # if either the card number or the suite is the same
            ll = len(card[0])
            if card[0].charAt(ll-1) == center_card[0].charAt(ll-1) or card[1][0:ll-2] == center_card[1][0:ll-2]:
                target_card = card
           
        # if baxter has a card that it can play, switch gamestate to player turn
        if target_card != null:
            self.turn = "player"
        else:
            #draw a new card from the deck
            target_card = self.deck

        return target_card

    def birdseye_pose():
        # Translation: [0.871, -0.252, 0.048]
        target = Point(0.871, -0.252, 0.048)
        return [target, " "]





def main():
    print('testing')
    point1 = Point(1, 2, 3)
    points = [1, 2, 3]
main()