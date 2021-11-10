from darknet import *
net = load_net(b"tiny2-coco.cfg", b"tiny2_coco_100k_candidate.weights", 0)
print("loading meta")
meta = load_meta(b"./output.data")
r = detect(net, meta, b"SDC13156.JPG", 0.75)
print(r)