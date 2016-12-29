import numpy as np
import cv2


im = cv2.imread('test.jpg')
blur = cv2.GaussianBlur(im,(3,3),0)
im2 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
cv2.imshow('Output', im2)
cv2.waitKey(0)
cv2.destroyAllWindows()







#CONTOUR DETECTION
#imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
#ret,thresh = cv2.threshold(imgray,127,255,0)

# Detect contours using both methods on the same image
#im,contours1, _= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
#im,contours2, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# Copy over the original image to separate variables
#img1 = im.copy()
#img2 = im.copy()

# Draw both contours onto the separate images
#cv2.drawContours(img1, contours1, -1, (255,0,0), 3)
#cv2.drawContours(img2, contours2, -1, (255,0,0), 3)

#Stack images side by side and display
#out = np.hstack([img1, img2])

# Now show the image
#cv2.imshow('Output', out)
#cv2.waitKey(0)
#cv2.destroyAllWindows()