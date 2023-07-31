#!/usr/bin/env python
# coding: utf-8

# In[28]:


#middle of prototype code
#this module should start with a binarized image
#processes of this module include edge detection and contour determination
import cv2
import matplotlib.pyplot as plot
from Raster import import_file, grayscale, binarize
import numpy as np
import random



def edge_detection(binarizedImage) :
    kernel = np.ones((3,3), np.uint8)
    dilatedImage = cv2.dilate(binarizedImage, kernel, iterations=1)
    erodedImage = cv2.erode(binarizedImage, kernel, iterations=1)
    edges = dilatedImage - erodedImage
    return edges

def find_contours(edges) :
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours




#if __name__ == "__main__":
    #test code
    #binarizedImage = binarize(grayscale(import_file()))  
    #plot.figure()
    #plot.imshow(binarizedImage, cmap="gray")
    #edges = edge_detection(binarizedImage)
    #plot.figure()
    #plot.imshow(edges, cmap="gray")
    #contours = find_contours(edges)
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




