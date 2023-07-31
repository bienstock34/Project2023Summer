#!/usr/bin/env python
# coding: utf-8

# In[8]:


#final segment of prototype code
#the purpose of this module is to take a list of contours and generate efficient GCODE
#AS OF TODAY, JULY 31 2023, THIS CODE DOES NOT WORK AT ALL!!!!!! :?
from Raster import import_file, grayscale, binarize
from Meaning import edge_detection, find_contours
from matplotlib.image import imread
import matplotlib.pyplot as plot
import numpy as np
import cv2


def find_nearest_contour_index(point, contours):
    distances = [cv2.pointPolygonTest(contour, point, True) for contour in contours]
    return np.argmin(distances)
    
def reorder_contours(contours):
    orderedContours = []
    #return empty if empty
    if not contours: 
        return orderedContours
    #starting point: the first point of the first contour
    startingPoint = tuple(contours[0][0][0])
    #keep track of the contours we have added to the ordered list
    visited = [0] #since we started with the first contour
    #add contour zero to the first contour
    orderedContours.append(contours[0])
    #while loop 
    while len(visited) < len(contours) : #while there are still contours left to go to
        #get the last point of the contour we just drew
        currentContour = orderedContours[-1]
        lastPoint = tuple(currentContour[-1][0])
        #find nearest neighbor to last point
        nearestContourIndex = find_nearest_contour_index(lastPoint, contours)
        #check if visited
        if nearestContourIndex not in visited :
            visited.append(nearestContourIndex)
            orderedContours.append(contours[nearestContourIndex])
    return orderedContours
            

#test code
contours = find_contours(edge_detection(binarize(grayscale(import_file()))))
reorderedContours = reorder_contours(contours)



# In[ ]:




