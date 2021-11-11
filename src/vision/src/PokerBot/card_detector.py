from darknet import *
from matplotlib import pyplot as plt

def classify(im, thresh=0.75):
    net = load_net(b"/home/cc/ee106a/fl21/class/ee106a-afr/ros_workspaces/pokerbot/src/vision/src/PokerBot/tiny2-coco.cfg", b"/home/cc/ee106a/fl21/class/ee106a-afr/ros_workspaces/pokerbot/src/vision/src/PokerBot/tiny2_coco_100k_candidate.weights", 0)
    # print("loading meta")
    meta = load_meta(b"/home/cc/ee106a/fl21/class/ee106a-afr/ros_workspaces/pokerbot/src/vision/src/PokerBot/output.data")
    #r = detect(net, meta, b"SDC13156.JPG", 0.75)
    
    r = detect_np(net, meta, im, thresh)
    return r
im = plt.imread("test.png")
print(classify(im, 0.5))