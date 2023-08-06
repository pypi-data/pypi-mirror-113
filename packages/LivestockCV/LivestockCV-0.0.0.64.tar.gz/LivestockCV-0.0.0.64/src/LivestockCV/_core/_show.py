import cv2
import numpy
import matplotlib
from matplotlib import pyplot as plt
from google.colab.patches import cv2_imshow


def _show(img, cmap=None):
	cv2_imshow(img)
