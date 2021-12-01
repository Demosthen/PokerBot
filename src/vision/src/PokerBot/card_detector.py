from darknet.darknet_images import *
from darknet import darknet
from matplotlib import pyplot as plt

class ImageDetector():
    def __init__(self, config_file, data_file, weights):
        self.network, self.class_names, self.class_colors = darknet.load_network(
            config_file,
            data_file,
            weights,
            batch_size=1
        )

    def detect(self, img, thresh):
        # Darknet doesn't accept numpy images.
        # Create one with image we reuse for each detect
        width = darknet.network_width(self.network)
        height = darknet.network_height(self.network)
        darknet_image = darknet.make_image(width, height, 3)

        #image = cv2.imread(image_path)
        #image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # uncomment if ros gives us BGR
        image_resized = cv2.resize(img, (width, height),
                                interpolation=cv2.INTER_LINEAR)
        darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
        detections = darknet.detect_image(self.network, self.class_names, darknet_image, thresh=thresh)
        image = darknet.draw_boxes(detections, image_resized, self.class_colors)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections

def image_detection(image_path, network, class_names, class_colors, thresh):
    # Darknet doesn't accept numpy images.
    # Create one with image we reuse for each detect
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)

    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
    darknet.free_image(darknet_image)
    image = darknet.draw_boxes(detections, image_resized, class_colors)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections

#TODO: adapt image_classification function from darknet images to rework classify
def classify(im, thresh=0.75):
    net = load_net(b"tiny2-coco.cfg", b"tiny2_coco.weights", 0)
    # print("loading meta")
    meta = load_meta(b"output.data")
    #r = detect(net, meta, b"SDC13156.JPG", 0.75)
    
    r = detect_np(net, meta, im, thresh)
    return r
if __name__ == "__main__":
    detector = ImageDetector(
        config_file="~/ros_workspaces/pokerbot/src/vision/src/PokerBot/darknet/custom_yolo.config",
        data_file="~/ros_workspaces/pokerbot/src/vision/src/PokerBot/darknet/cards.data",
        weights="~/ros_workspaces/pokerbot/src/vision/src/PokerBot/darknet/weights/backup/yolov4-tiny-custom_20000.weights")
    im = plt.imread("kh.jpg")
    print(detector.detect(im, 0.1))
