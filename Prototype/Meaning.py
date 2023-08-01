#!/usr/bin/env python
# coding: utf-8

# In[40]:


#middle of prototype code
#this module should start with a binarized image
#processes of this module include edge detection and contour determination
import cv2
import matplotlib.pyplot as plot
from Raster import import_file, grayscale, binarize
import numpy as np
import random


#function: edge detection
#purpose: determine the location of edges in the image
#arguments: binarized image as uint8 [][] 
#returns: edges as a uint8 [][] 
def edge_detection(binarizedImage) :
    kernel = np.ones((3,3), np.uint8)
    dilatedImage = cv2.dilate(binarizedImage, kernel, iterations=1)
    erodedImage = cv2.erode(binarizedImage, kernel, iterations=1)
    edges = dilatedImage - erodedImage
    return edges


#function: find contours
#purpose: partitions the discovered edges into contour regions
#arguments: edges
#returns: (1) contours: a tuple of ndarrays of shape (#pointsInContour, 2)
        #(2) hierarchy: numpy array of shape (#contours, [Next, Previous, First Child, Parent])
def find_contours(edges) :
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #reshapes contour because I do not care about OpenCV convention
    contours = [contour.reshape((-1,2)) for contour in contours]
    return contours, hierarchy


if __name__ == "__main__":
    #test code
    binarizedImage = binarize(grayscale(import_file()))  
    #plot.figure()
    #plot.imshow(binarizedImage, cmap="gray")
    edges = edge_detection(binarizedImage)
    #print(edges.shape)
    #print("dtype edges: ", edges.dtype)
    #plot.figure()
    #plot.imshow(edges, cmap="gray")
    contours, hierarchy = find_contours(edges)
    print(contours[0][0], contours[1][0], contours[2][0], contours[3][0], contours[4][0], contours[5][0], contours[6][0], contours[7][0])
    #print("type contours: ", type(contours))
    #sortedContours = sorted(contours, key=cv2.contourArea, reverse=True)
    #contourImage = np.zeros_like(edges)
    #numDraw = min(10, len(sortedContours))
    #for i in range (numDraw):
    #    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    #    cv2.drawContours(contourImage, [sortedContours[i]], -1, color, thickness=2)
    #resultImage = cv2.addWeighted(edges, 1, contourImage, 0.5, 0)
    #plot.figure()
    #plot.imshow(resultImage)


# In[ ]:




