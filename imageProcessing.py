import numpy as np
import cv2
import argparse
from matplotlib import pyplot as plt
from scipy.spatial import distance
from imutils import perspective
from imutils import contours
import imutils


def sort_contours(contours, method="left-to-right"):
	#initialize the reverse flag and sort index
	reverse = False
	i = 0

	#handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	#handle if we are sorting against the y-coordinate rather than the x-coordinate
	# of the bounding box

	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	#construct the list of bounding boxes and sort them from top to bottom
	boundingBoxes = [cv2.boundingRect(c) for c in contours]
	(contours, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes), key=lambda b:b[1][i], reverse=reverse))

	return contours

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def findCenter(contour):
	M = cv2.moments(contour)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])

	return cY

def findHeight(contour):
	box = cv2.minAreaRect(contour)
	box = cv2.cv.BoxPoints(box)
	box = np.array(box, dtype="int")
	box = perspective.order_points(box)
	#for (x,y) in box:
		#cv2.circle(orig, (int(x), int(y)), 5, (0,0,255), -1)
	(tl, tr, br, bl) = box
	#Calculate midpoint between top left and top right points, and bottom left and bottom right points
	(tltrX, tltrY) = midpoint(tl, tr)
	(blbrX, blbrY) = midpoint(bl, br)

	dst = distance.euclidean( (tltrX, tltrY) , (blbrX,blbrY) )
	return dst

def getRects(rects, image, im_th):
	for rect in rects:
		cv2.rectangle(image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)
		# Make the rectangular region around the digit
		leng = int(rect[3] * 1.6)
		pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
		pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
		roi = im_th[pt1:pt1+leng, pt2:pt2+leng] 
		# Resize the image 
		roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
		roi = cv2.dilate(roi, (3, 3))
		


def main():
	img = cv2.imread('test3.png', cv2.IMREAD_GRAYSCALE)
	
	#GaussianBlur in order to get rid of Gaussian noise.
	blur = cv2.GaussianBlur(img,(3,3),0)

	#Adaptive threshold in order to isolate all black and white areas.
	#adapted = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
	            #cv2.THRESH_BINARY,75,10)

	#CONTOUR DETECTION
	_,thresh = cv2.threshold(blur,90,255,cv2.THRESH_BINARY_INV)
	
	#Detect contours using both methods on the same image
	contours, hierarchy= cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

	#rects = [cv2.boundingRect(contour) for contour in contours]

	contours = sort_contours(contours, "top-to-bottom")

	line_list = []
	contour_list = []
	
	for contour in contours:
		area = cv2.contourArea(contour)
		if area <= 10.0:
			continue

		inLineList = False
		height = findHeight(contour)
		center = findCenter(contour)

		for line in line_list:
			if (line < (center + (height/2)) and line > center) or (line > (center - (height/2)) and line < center) or (line is center):
				contour_list[line_list.index(line)].append(contour)
				inLineList = True
				break

		if (inLineList is True):
			continue
		else:
			print center
			#x,y,w,h = cv2.boundingRect(contour)
			#cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
			#cv2.imshow("Result", img)
			#cv2.waitKey(0)
			line_list.append(center)
			contour_list.append([contour])

	
	print len(line_list)
	print len(contour_list)
	i=0
	for contours in contour_list:
		contours = sort_contours(contours)
		for contour in contours:
			[x,y,w,h] = cv2.boundingRect(contour)
			cv2.imwrite(str(i) + ".png", img[y:y+h, x:x+w])
			i=i+1
main()