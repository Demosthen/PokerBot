#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Point, PoseStamped
from coord_client import Coord_Client
from vision.srv import fuck
from copy import deepcopy
import cv_bridge
from sensor_msgs.msg import Image
import cv2
import numpy as np
img_default = None
img_cheat = None
pub = None
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
        self.client.pickup()
        rospy.sleep(1)
        self.client.release()
        self.current_cards = None
        self.deck_of_cards = None # self.current_cards[1][0]
        self.game_state = "start"
        self.baxter_hand = [None] * 8
        self.free_spaces = np.ones(8)
        self.hand_start = Point(0.549, 0.616, -0.135)

        self.last_play = None
        
        self.bev = PoseStamped()
        self.setup_bev()
      
        rospy.wait_for_service('twod_to_3d')
        twod_to_3d = rospy.ServiceProxy('twod_to_3d', fuck)
        def wrapper():
            while not rospy.is_shutdown():
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
        self.locate_deck_and_init_hand()
        print("Game setup complete!")

    def setup_bev(self):
        # LEFT HAND BEV
        self.bev.header.frame_id = "base"
        self.bev.pose.position.x = 0.717
        self.bev.pose.position.y = 0.242 
        self.bev.pose.position.z = 0.035
        self.bev.pose.orientation.x = 0
        self.bev.pose.orientation.y = -1
        self.bev.pose.orientation.z = 0
        self.bev.pose.orientation.w = 0

    def go_to_bev(self, confirm=True):
        self.client.move(self.bev, "bev", hover=False)
        rospy.sleep(0.5)
        if (confirm):
            raw_input("Bird's eye view complete, press <Enter> to confirm: ")

    def locate_deck_and_init_hand(self):
        self.go_to_bev()
        deck_spotting = self.twod_to_3d()
        # print("deck location: ", deck_spotting)
        self.deck_of_cards = deck_spotting.cards.coords[0]
        self.play_center = deepcopy(self.deck_of_cards)
        self.play_center.y += 0.1 # Gameplay area is always to the right of the deck

        # Draw 3 cards as the starting hand
        self.draw_card(3, initial_bev=False)

    def move_card(self, source, dest):
        self.client.move(source, "card")
        self.client.pickup() 
        # print("GO_TO_BEV IS COMMENTED HERE, UNCOMMENT IF PATH PLANNING STARTS TO FAIL")
        self.go_to_bev(confirm=False)

        self.client.move(dest, "destination")
        self.client.release()
        
        up_more = deepcopy(dest)
        up_more.pose.position.z = dest.pose.position.z + 0.05
        self.client.move(up_more, "up", hover=False)

    def loop(self):
        global pub
        while not rospy.is_shutdown():
            # self.go_to_bev()
            fuckResponse = self.twod_to_3d()
            print("cArD lIsT: ", fuckResponse)

            # Identifies the center card in play
            center_card = fuckResponse.cards.cards[0]
            min_dist = self.compute_point_dist(fuckResponse.cards.coords[0], self.play_center)
            for c, coord in zip(fuckResponse.cards.cards, fuckResponse.cards.coords):
                dist = self.compute_point_dist(coord, self.play_center)
                if dist < min_dist:
                    min_dist = dist
                    center_card = c
            center_card = self.verify_card(center_card)
            if self.last_play:
                lnum = self.last_play[:-1]
                lsuit = self.last_play[-1]
                center_num = center_card[:-1]
                center_suit = center_card[-1]
                if not (lnum == center_num or lsuit == center_suit):
                    print("You cheating, illiterate fuck")
                    msg = cv_bridge.CvBridge().cv2_to_imgmsg(img_cheat)
                    pub.publish(msg)
            
            self.pick_play_card(center_card)
            raw_input("Baxter has finished its turn. Make your turn, then press <Enter>.")
            # self.move_card(target, self.make_pose(self.play_center))

    def pick_play_card(self, center): # TODO
        print("PICKING A CARD")
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
                print("FOUND CARD TO PLAY,", card)
                self.move_card(self.make_pose(coord), self.make_pose(self.play_center))
                self.free_spaces[i] = 1
                self.baxter_hand[i] = 0               
                self.turn = "player"
                self.last_play = card
                self.go_to_bev() # Return to neutral position
                return True # on success
        print("DID NOT FIND CARD, DRAWING")
        self.last_play = center
        self.draw_card(1)
        return False # on not finding a card to play :(

    def draw_card(self, num, initial_bev=True):
        def find_empty_position():
            target = None
            pos = 0
            for i in range(len(self.free_spaces)):
                if self.free_spaces[i]:
                    target = deepcopy(self.hand_start)
                    target.y += space * i
                    pos = i
                    break
            if not target:
                target = deepcopy(self.hand_start)
                target.y += space * len(self.free_spaces)
                self.free_spaces.append(1)
                self.baxter_hand.append(0)
            return target, pos

        space = -0.08 # Variable for card spacing during placement

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
    def verify_card(self, card):
        rinput = raw_input("Found %s, press <Enter> to confirm: " % card)
        while rinput:
            confirm = raw_input("Are you sure? New card will be %s" % rinput)
            if not confirm:
                return rinput
            else:
                rinput = raw_input("Retype the card, or press <Enter> to confirm %s" % card)
        return card


def main():
    global img_default, img_cheat, pub
    rospy.init_node('win_node')
    img_default = cv2.imread('./down.jpg')
    img_cheat = cv2.imread('./eyebrows_up.jpg')

    msg = cv_bridge.CvBridge().cv2_to_imgmsg(img_default)
    pub = rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=10)
    pub.publish(msg)
    gameplay = Gameplay()
    raw_input("Press <Enter> to begin.")
    gameplay.loop()
    
if __name__ == "__main__":
    main()