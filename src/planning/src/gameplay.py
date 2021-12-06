"""
Gameplay Class: is this the one that controls the entire game??
"""

from geometry_msgs.msg import Point
from coord_client import twodto3d
from planning.src.coord_client import Coord_Client

class gameplay(object):
    """
    Gameplay class that keeps track of the game state,
    baxter's cards and returns a next move.
    """
    def __init__(self):
        """
        Constructor. 
        
        Inputs:
        current_cards: the list of Point objects and strings of all
        the cards currently on the table. The most recently
        played card index 0.
        [["4D","10H",...], [Point1, Point2, ...]]
        "h" "s" "c" "d"
        
        """
        #Initiates coord_client and looks for cards
        self.client = Coord_Client()
        self.current_cards = []
        current_cards = self.client.twodto3d()
        # Scan for cards, if there's nothing, center card, baxter_hand = []
        self.center_card = current_cards[0][0]
        print("the center card is: " + self.center_card)
        self.deck_of_cards = current_cards[1][1]
        print("the deck of cards is located at: " + self.deck_of_cards)
        self.baxter_hand = current_cards[0][:]
        self.game_state = "start"
        # User Confirmation request
        raw_input("Press <Enter> to start the game! ")
        self.compare_cards()
    

    # Compares the most recently played card to its own, and 
    def compare_cards(self):
        target_card = []
        for card in self.baxter_hand:
            # Card[0] contains the card type, Card[1] accesses the coords
            # if either the card number or the suite is the same
            
            if card[-1] == self.center_card[-1] or card[0] == self.center_card[0] or card[1] == self.center_card[1]:
                target_card = card
                # baxter has a card that it can play, switch gamestate to player turn
                self.turn = "player"
                #TO DO: KEEP TRACK OF THE EMPTIED SLOTS TO PLACE NEW CARD NEXT
           
        if target_card == []:
            #draw a new card from the deck
            target_card = self.deck_of_cards

        return target_card



    def draw_card(self):
        if self.game_state == "start":
            # Draw 4 cards and play 1 card
            coords = []
            for coord in coords:



    def birdseye_pose():
        # Translation: [0.871, -0.252, 0.048]
        target = Point(0.871, -0.252, 0.048)
        return [target, " "]





def main():
    print('testing')
    point1 = Point(1, 1, 1)
    point2 = Point(2, 1, 1)
    point3 = Point(3, 1, 1)
 
    cards = [["4D","10H","2C"], [point1, point2, point3]]
    gameplay(cards)
main()