from darknet.darknet_images import *
from darknet import darknet
from matplotlib import pyplot as plt

#TODO: adapt image_classification function from darknet images to rework classify
def classify(im, thresh=0.75):
    net = load_net(b"tiny2-coco.cfg", b"tiny2_coco.weights", 0)
    # print("loading meta")
    meta = load_meta(b"output.data")
    #r = detect(net, meta, b"SDC13156.JPG", 0.75)
    
    r = detect_np(net, meta, im, thresh)
    return r
im = plt.imread("e.jpg")
print(classify(im, 0.7))
