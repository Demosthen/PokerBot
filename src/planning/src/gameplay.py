#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Point, PoseStamped
from coord_client import Coord_Client
from vision.srv import fuck
import numpy as np
"""
Gameplay class that keeps track of the game state,
baxter's cards and returns a next move.
"""
class Gameplay:
    
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
        #Initiates coord_client and looks for card deck
        self.client = Coord_Client()
        rospy.sleep(2)
        self.client.release()
        self.current_cards = None
        self.deck_of_cards = None # self.current_cards[1][0]
        self.game_state = "start"
        self.baxter_hand = np.zeros(8)
        self.free_spaces = np.ones(8)
        self.hand_start = Point(0.549, 0.181, -0.135)
        
        self.bev = PoseStamped()
        self.setup_bev()
      
        rospy.wait_for_service('twod_to_3d')
        twod_to_3d = rospy.ServiceProxy('twod_to_3d', fuck)
        def wrapper():
            while(True):
                try:
                    ret = twod_to_3d()
                    satisfactory = raw_input("IS %s SATISFACTORY? PRESS a and enter to confirm \n" % ret)
                    if len(ret.cards.cards) != 0 and satisfactory == 'a':
                        return ret
                    if not satisfactory:
                        raw_input("Couldn't detect any cards, press Enter to try again")
                except rospy.service.ServiceException:
                    i = raw_input("Couldn't detect AR markers, press Enter to try again")
                    if i:
                        break
        self.twod_to_3d = wrapper
        self.locate_deck()
        self.init_hand()
        print("Game setup complete!")

    def setup_bev(self):
        # LEFT HAND BEV
        self.bev.header.frame_id = "base"
        self.bev.pose.position.x = 0.617
        self.bev.pose.position.y = 0.042 
        self.bev.pose.position.z = 0.035
        self.bev.pose.orientation.x = 0
        self.bev.pose.orientation.y = -1
        self.bev.pose.orientation.z = 0
        self.bev.pose.orientation.w = 0

    def go_to_bev(self):
        self.client.move(self.bev, "bev", hover=False)
        rospy.sleep(0.5)
        raw_input("Bird's eye view complete, press <Enter> to confirm: ")

    def locate_deck_and_init_hand(self):
        self.go_to_bev()
        deck_spotting = self.twod_to_3d()
        print("deck location: ", deck_spotting)
        self.deck_of_cards = deck_spotting.cards.coords[0]
        self.play_center = self.deck_of_cards.y + 0.1 # Gameplay area is always to the right of the deck

        # Draw 4 cards as the starting hand
        self.draw_card(4, initial_bev=False)

    # Moves a card (specified by name) to a Point destination
    # def move_card(self, card_list, coord_list, card, dest):
    #     assert len(card_list) == len(coord_list)
    #     coords = None
    #     for c, cd in zip(card_list, coord_list):
    #         if c == card:
    #             coords = cd
    #             break
    #     assert coords != None
    #     card_pose = self.make_pose(coords)
    #     self.client.move(card_pose, "card")
    #     self.client.pickup() 
    #     self.client.move(dest, "destination")
    #     self.client.release() 
    def move_card(self, source, dest):
        self.client.move(source, "card")
        self.client.pickup() 
        print("GO_TO_BEV IS COMMENTED HERE, UNCOMMENT IF PATH PLANNING STARTS TO FAIL")
        # self.go_to_bev()

        self.client.move(dest, "destination")
        self.client.release() 

    def loop(self):
        while not rospy.is_shutdown():
            self.go_to_bev()
            fuckResponse = self.twod_to_3d()
            print("cArD lIsT: ", fuckResponse)
            cards = fuckResponse.cards.cards
            coords = fuckResponse.cards.coords

            # Identifies the center card in play
            center_card = fuckResponse.cards.cards[0]
            min_dist = self.compute_point_dist(fuckResponse.cards.coords[0], self.play_center)
            for c, coord in zip(fuckResponse.cards.cards, fuckResponse.cards.coords):
                dist = self.compute_point_dist(coord, self.play_center)
                if dist < min_dist:
                    min_dist = dist
                    center_card = c
            center_card = self.verify_card(center_card)
            
            self.pick_play_card(center_card)
            raw_input("Baxter has finished its turn. Make your turn, then press <Enter>.")
            # self.move_card(target, self.make_pose(self.play_center))

    def pick_play_card(self, center): # TODO
        for i in range(len(self.baxter_hand)):
            if not self.baxter_hand[i]:
                continue
            (card, coord) = self.baxter_hand[i]
            num = card[:-1]
            suit = card[-1]
            center_num = center[:-1]
            center_suit = center[-1]

            if num == center_num or suit == center_suit:
                # # baxter has a card that it can play, switch gamestate to player turn
                # self.pathplan(self.baxter_hand[1][c], "pick")
                # self.pathplan(self.center_card, "place")
                self.move_card(coord, self.play_center)
                self.free_spaces[i] = 1
                self.baxter_hand[i] = 0               
                self.turn = "player"
                return True # on success
        self.draw_card(1)
        return False # on not finding a card to play :(


        

    # # Compares the most recently played card to its own, and 
    # def compare_cards(self):
    #     while not rospy.is_shutdown():
            
    #         for c in len(self.baxter_hand[0]):
    #             # Card[0] contains the card type, Card[1] accesses the coords
    #             # if either the card number or the suite is the same
    #             card = self.baxter_hand[0][c]

    #             if card[-1] == self.center_card[-1] or card[0] == self.center_card[0] or card[1] == self.center_card[1]:
    #                 # baxter has a card that it can play, switch gamestate to player turn
    #                 self.pathplan(self.baxter_hand[1][c], "pick")
    #                 self.pathplan(self.center_card, "place")
    #                 self.free_spaces.append(self.baxter_hand[1][c])       
    #                 self.baxter_hand[0].remove(c)
    #                 self.baxter_hand[1].remove(c)                    
    #                 self.turn = "player"
    #                 break
    #         if self.turn == "baxter":
    #             #draw a new card from the deck
    #             self.draw_card()

    #         raw_input("Press <Enter> to once player has played! ")
    #         self.turn = "baxter"

    #         if len(self.baxter_hand) == 0:
    #             print("Baxter wins!")   
    #             break

    def draw_card(self, num, initial_bev=True):
        def find_empty_position():
            target = None
            pos = 0
            for i in range(len(self.free_spaces)):
                if self.free_spaces[i]:
                    target = self.hand_start
                    target.y += space * i
                    pos = i
                    break
            if not target:
                target = self.hand_start
                target.y += space * len(self.free_spaces)
                self.free_spaces.append(1)
                self.baxter_hand.append(0)
            return target, pos

        space = -0.07 # Variable for card spacing during placement

        # Draw 4 cards and play 1 card
        for _ in range(num):
            if initial_bev:
                self.go_to_bev()

            # Identifies the card at the top of the deck
            fuckResponse = self.twod_to_3d()
            deck_card = fuckResponse.cards.cards[0]
            min_dist = self.compute_point_dist(fuckResponse.cards.coords[0], self.deck_of_cards)
            for c, coord in zip(fuckResponse.cards.cards, fuckResponse.cards.coords):
                dist = self.compute_point_dist(self.deck_of_cards, coord)
                if dist < min_dist:
                    min_dist = dist
                    deck_card = c
            
            # Make sure the vision node isn't tripping up
            deck_card = self.verify_card(deck_card)

            # Determines where to place the card in hand
            target, pos = find_empty_position()
            print("Found empty position at index", pos)
            print("Target hand location:", target)

            # Adds card from the deck to its hand
            self.move_card(self.make_pose(self.deck_of_cards), self.make_pose(target))
            self.baxter_hand[pos] = (deck_card, target)
            self.free_spaces[pos] = 0

            initial_bev = True

        self.go_to_bev() # Return to a neutral position
    
    # ===== HELPER FUNCTIONS =====
    def make_pose(self, point):
        pose = PoseStamped()
        pose.header.frame_id = "base"
        pose.pose.position.x = point.x
        pose.pose.position.y = point.y
        pose.pose.position.z = max(point.z, -0.14)
        pose.pose.orientation = self.bev.pose.orientation
        return pose

    def compute_point_dist(self, a, b):
        return (a.x - b.x) **2 + (a.y - b.y) ** 2

    # Gives user a chance to correct for vision errors
    def verify_card(card):
        rinput = raw_input("Found %s, press <Enter> to confirm: " % card)
        while rinput:
            confirm = raw_input("Are you sure? New card will be", rinput)
            if confirm:
                return rinput
            else:
                rinput = raw_input("Retype the card, or press <Enter> to confirm", card)
        return card


def main():
    rospy.init_node('win_node')
    gameplay = Gameplay()
    #gameplay.loop()
    
if __name__ == "__main__":
    main()