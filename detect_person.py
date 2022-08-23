import os
from utils import Detector
import cv2

def detect_user(img):
    detector = Detector()
    img = cv2.resize(img,(460,460))
	# get predictions and draw them on image
    predictions = detector.get_people_names(img, speed_up=False, downscale_by=1)
    # annoted_image = detector.draw_results(img, predictions)
    # image = cv2.cvtColor(annoted_image, cv2.COLOR_RGB2BGR)
    return predictions