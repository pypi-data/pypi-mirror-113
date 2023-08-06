# Contour


# my basic libraries 
import cv2
from LivestockCV.core import show_image

def contour(img):
   contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
   print("Number of Contours found = " + str(len(contours)))
   cv2.drawContours(img, contours, -1, (200, 100, 0), 2)
   show_image(img)