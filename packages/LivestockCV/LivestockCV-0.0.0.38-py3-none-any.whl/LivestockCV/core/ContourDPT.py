# ContourDPT


# my basic libraries 
import cv2

def ContourDPT(contouredimg, epsilon):
   thresh_copy = cv2.cvtColor(binary2, cv2.COLOR_GRAY2RGB) 
   perimeter = cv2.arcLength(biggest_contour, True)
   e = epsilon * perimeter 
   transformed_contour = cv2.approxPolyDP(biggest_contour, epsilon = e, closed = True)
   cv2.drawContours(thresh_copy, [ transformed_contour ], contourIdx=-1, color=(0, 255, 0), thickness=10) 
   print('', transformed_contour.shape[0])

   print("DP Transformed Polygon: ")
   plt.imshow(thresh_copy)