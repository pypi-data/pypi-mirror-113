# ContourMax


# my basic libraries 
import cv2

def ContourMax(img):
	(contours, hierarchy) = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
	biggest_contour = max(contours, key= cv2.contourArea)
	cv2.drawContours(img, biggest_contour, contourIdx=-1, color=(0, 0, 250), thickness=2) 