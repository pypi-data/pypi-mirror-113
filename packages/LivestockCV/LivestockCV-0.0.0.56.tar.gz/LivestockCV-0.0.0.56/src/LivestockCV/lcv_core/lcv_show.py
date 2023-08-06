# Importing our very important packages especially the one from google.colab.patches
import cv2
import numpy
import matplotlib
from matplotlib import pyplot as plt
from google.colab.patches import cv2_imshow

def lcv_show(img):
	cv2_imshow(img)
