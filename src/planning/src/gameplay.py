#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Point, PoseStamped
from coord_client import Coord_Client
from vision.srv import fuck
import time
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
        self.current_cards = None #self.client.twodto3d()
        self.deck_of_cards = None #self.current_cards[1][0]
        self.game_state = "start"   
        self.baxter_hand =[[None], [None]]
        self.free_spaces = []
        
        self.bev = PoseStamped()
        self.setup_bev()
        self.client.pickup()
      
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
        self.client.release()
        self.identify_deck()
        print("IniT COMpLeTE GaMEn ReAdy EtO LLoOPpPoP")

    def setup_bev(self):
        
        self.bev.header.frame_id = "base"
        # RIGHT HAND BEV
        # self.bev.pose.position.x = 0.738
        # self.bev.pose.position.y = 0.289
        # self.bev.pose.position.z = 0.035
        # LEFT HAND BEV
        self.bev.pose.position.x = 0.617
        self.bev.pose.position.y = 0.042 
        self.bev.pose.position.z = 0.035
        self.bev.pose.orientation.x = 0
        self.bev.pose.orientation.y = -1
        self.bev.pose.orientation.z = 0
        self.bev.pose.orientation.w = 0

    def go_to_bev(self):
        self.client.move(self.bev, "bev", hover=False)
        raw_input("Press <Enter> to confirm BIRD\'S EYE VIEW ACTIVATED!!!!!")

    def move_card(self, card_list, coord_list, card, dest):
        assert len(card_list) == len(coord_list)
        coords = None
        for c, cd in zip(card_list, coord_list):
            if c == card:
                coords = cd
                break
        assert coords != None
        card_pose = self.make_pose(coords)
        self.client.move(card_pose, "cArD")
        self.client.pickup() 
        self.client.move(dest, "cEntErRrr")
        self.client.release() 

    def make_pose(self, point):
        pose = PoseStamped()
        pose.header.frame_id = "base"
        pose.pose.position.x = point.x
        pose.pose.position.y = point.y
        pose.pose.position.z = max(point.z, -0.14)
        pose.pose.orientation = self.bev.pose.orientation
        return pose

    def identify_deck(self):
        self.go_to_bev()
        deck_spotting = self.twod_to_3d()
        print("deck location: ", deck_spotting)

        self.deck_of_cards = deck_spotting.cards.coords[0]
        print("deck location updated as: ", self.deck_of_cards)
        self.draw_card(4, initial_bev=False)
        # self.client.move(self.make_pose(self.deck_of_cards), "card")
        # self.client.pickup()
        # self.go_to_bev()
        # # self.client.release()

    def loop(self):
        # if self.game_state == "start":
        #     self.draw_card(4)
        while not rospy.is_shutdown():
            self.go_to_bev()
            rospy.sleep(2) # wait for images to go to 2d 2 3d
            fuckResponse = self.twod_to_3d()
            print("cArD lIsT: ", fuckResponse)
            cards = fuckResponse.cards.cards
            coords = fuckResponse.cards.coords
            
            center_card = cards[0]
            center_coord = coords[0]
            hand_cards = cards[1:]
            hand_coords = coords[1:]
            print("cEnTeR CaRD", center_card)
            print("hAnDS CaRdS", hand_cards)
            card_to_move = self.pick_card(hand_cards, hand_coords, center_card)
            self.move_card(cards, coords, card_to_move, self.make_pose(center_coord))

    def pick_card(self, hand, coords, center): #TODO
        for card, coord in zip(hand, coords):
            num = card[:-1]
            suit = card[-1]
            center_num = center[:-1]
            center_suit = center[-1]
            if num == center_num or suit == center_suit:
                
                # # baxter has a card that it can play, switch gamestate to player turn
                # self.pathplan(self.baxter_hand[1][c], "pick")
                # self.pathplan(self.center_card, "place")
                self.free_spaces.append(coord)       
                # self.baxter_hand[0].remove(c)
                # self.baxter_hand[1].remove(c)                    
                self.turn = "player"
                # break
                return card
        if self.game_state == "baxter":
            self.draw_card(1)
        return hand[0]


        

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
     
    def compute_point_dist(self, a, b):
        return (a.x - b.x) **2 + (a.y - b.y) **2

    def draw_card(self, num, initial_bev=True):
        # Variable for card spacing during placement
        print("I AM DRAW CARD FUNCTION, AND I AM RUNNING")
        space = -0.08
        
        if self.game_state == "start":
            target = Point(0.549, 0.181, -0.135) #TODO: CHANGE TO PLAYER DRAWS BAXTERS FIRST CARD
        else:
            if self.free_spaces != []:
                # Draw a card from deck and place in empty space or add to end of the hand
                target = self.free_spaces[0]
            else:
                # Add new card to the end of its hand
                target = self.baxter_hand[1][3]
                target.x = target.x + space

        # Draw 4 cards and play 1 card
        while len(self.baxter_hand) != num:
            if initial_bev:
                self.go_to_bev()
            fuckResponse = self.twod_to_3d()
            
            deck_card = fuckResponse.cards.cards[0]
            min_dist = self.compute_point_dist(fuckResponse.cards.coords[0], self.deck_of_cards)
            for c, coord in zip(fuckResponse.cards.cards, fuckResponse.cards.coords):
                dist = self.compute_point_dist(self.deck_of_cards, coord)
                if dist < min_dist:
                    min_dist = dist
                    deck_card = c
            print("PICKING UP CARD: ", deck_card)
            #goes to the deck and picks up card
            self.client.move(self.make_pose(self.deck_of_cards), "card")
            self.client.pickup()
            self.go_to_bev()

            #places card in own hand & look at it
            self.client.move(self.make_pose(target), "card")
            
            # self.baxter_hand[1].append(moved_card[1])
            self.client.release()
            self.baxter_hand[0].append(deck_card)
            self.baxter_hand[1].append(target)
            print("check check DID YOU ADD A CARD TO YOUR HAND", self.baxter_hand)
            # new_card = self.twodto3d()
            #apply offset for next start
            
            target.y += space
            print("target is n NOW THIS INSTEAD : ", target)
            initial_bev = True
            

    
    # # PATH PLAN AND EXECUTE
    # def pathplan(self, target, vac):
    #     # go to the location designated
    #     try:
    #         card_loc = PoseStamped()
    #         card_loc.header.frame_id = "base"

    #         #x, y, and z position
    #         card_loc.pose.position.x = target.x 
    #         card_loc.pose.position.y = target.y 
    #         card_loc.pose.position.z = target.z + 0.5

    #         #Orientation as a quaternion
    #         card_loc.pose.orientation.x = 0.0
    #         card_loc.pose.orientation.y = -1.0
    #         card_loc.pose.orientation.z = 0.0
    #         card_loc.pose.orientation.w = 0.0

    #         # run the pose stamped object through planner
    #         plan = self.planner.plan_to_pose(card_loc, [])

    #         raw_input("Press <Enter> to execute arm movement")
    #         if not planner.execute_plan(plan):
    #             raise Exception("Execution failed")
    #         if not controller.execute_path(plan):
    #             raise Exception("Execution failed")
            
    #         if vac == "place":
    #             # The gripper is placing down a card
    #             # tell vacuum cripper to let go
    #             card_loc.pose.position.z = target.z + 1
    #             plan = self.planner.plan_to_pose(card_loc, [])
    #             raw_input("Press <Enter> to lift up and look at card")

    #             # Baxter reads in the card it just put down
    #             moved_card = self.client.twodto3d()
    #             return moved_card
                
    #         else:
    #             # the gripper is picking up a card
    #             # tell vac to suck in
    #             return []



    #     except Exception as e:
    #         print(e)
    #         traceback.print_exc()

    #         # Print the contents of the message to the console
    #         # print("Message: %s" % message.msg + ", Sent at: %s" % message.timestamp  + ", Received at: %s" % rospy.get_time()  )



def main():
    rospy.init_node('win_node')
    gameplay = Gameplay()
    raw_input("Press <Enter> to begin.")
    gameplay.loop()
    
if __name__ == "__main__":
    main()