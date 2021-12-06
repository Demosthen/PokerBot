"""
Gameplay Class: is this the one that controls the entire game??
"""

from geometry_msgs.msg import Point
from coord_client import twodto3d
from planning.src.coord_client import Coord_Client
from planning.src.path_planner import PathPlanner

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
        #Initiates coord_client and looks for card deck
        self.client = Coord_Client()
        self.planner = PathPlanner("right_arm")
        self.current_cards =  self.client.twodto3d()
        self.deck_of_cards = current_cards[1][1]
        print("the deck of cards is located at: " + self.deck_of_cards)

        # User Confirmation request
        raw_input("Press <Enter> to start the game! ")
        self.game_state = "start"   
        self.target_card = []
        self.baxter_hand = []
        # Baxter draws 4 cards for itself
        self.draw_card()
        
        # Player plays first, baxter reads in
        self.current_cards =  self.client.twodto3d()
        self.center_card = self.current_cards[0][0]
        print("the center card is: " + self.center_card)

      
        print("Baxter's hand includes: " + self.baxter_hand)
        self.game_state = "baxter"
        self.compare_cards()
    

    # Compares the most recently played card to its own, and 
    def compare_cards(self):
        while not rospy.is_shutdown():
            
            for card in self.baxter_hand:
                # Card[0] contains the card type, Card[1] accesses the coords
                # if either the card number or the suite is the same
                
                if card[-1] == self.center_card[-1] or card[0] == self.center_card[0] or card[1] == self.center_card[1]:
                    self.pathplan(card)
                    # baxter has a card that it can play, switch gamestate to player turn
                    self.turn = "player"
                    #TO DO: KEEP TRACK OF THE EMPTIED SLOTS TO PLACE NEW CARD NEXT

            if self.target_card == []:
                #draw a new card from the deck
                self.draw_card()

            raw_input("Press <Enter> to once player has played! ")
            self.turn = "baxter"

            if len(self.baxter_hand) == 0:
                print("Baxter wins!")   
                break
        

        
            



    def draw_card(self):
        # Variable for card spacing during placement
        start = Point(0, 0, 0)
        space = 0.5

        if self.game_state == "start":
            # Draw 4 cards and play 1 card
            while len(self.baxter_hand[0]) != 4:
                #goes to the deck
                self.pathplan(self.deck_of_cards, "pick")
                #TO DO: picks up card                

                #places card in own hand & look at it
                self.pathplan(start, "place")
                #apply offset for next start
                start[0] = start[0] + space
                
                
            self.target_card = []
        else:
            # Draw a card from deck and place in empty space or add to end of the hand
            self.pathplan()
            return 0

            

    
    # PATH PLAN AND EXECUTE
    def pathplan(self, target, vac):
        # go to the location designated
        try:
            card_loc = PoseStamped()
            card_loc.header.frame_id = "base"

            #x, y, and z position
            card_loc.pose.position.x = target.x 
            card_loc.pose.position.y = target.y 
            card_loc.pose.position.z = target.z + 0.5

            #Orientation as a quaternion
            card_loc.pose.orientation.x = 0.0
            card_loc.pose.orientation.y = -1.0
            card_loc.pose.orientation.z = 0.0
            card_loc.pose.orientation.w = 0.0

            # run the pose stamped object through planner
            plan = self.planner.plan_to_pose(card_loc, [])

            raw_input("Press <Enter> to execute arm movement")
            if not planner.execute_plan(plan):
                raise Exception("Execution failed")
            if not controller.execute_path(plan):
                raise Exception("Execution failed")
            
            if vac == "place":
                # The gripper is placing down a card
                # tell vacuum cripper to let go
                card_loc.pose.position.z = target.z + 1
                plan = self.planner.plan_to_pose(card_loc, [])
                raw_input("Press <Enter> to lift up and look at card")

                # Baxter reads in the card it just put down
                moved_card = self.client.twodto3d()
                return moved_card
                
            else:
                # the gripper is picking up a card
                # tell vac to suck in
                return 0



        except Exception as e:
            print(e)
            traceback.print_exc()

            # Print the contents of the message to the console
            # print("Message: %s" % message.msg + ", Sent at: %s" % message.timestamp  + ", Received at: %s" % rospy.get_time()  )



def main():
    print('testing')
    point1 = Point(1, 1, 1)
    point2 = Point(2, 1, 1)
    point3 = Point(3, 1, 1)
 
    cards = [["4D","10H","2C"], [point1, point2, point3]]
    gameplay(cards)
main()