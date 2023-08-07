#middle of prototype code
#this module should start with a binarized image
#processes of this module include edge detection and contour determination
import cv2
import matplotlib.pyplot as plot
import numpy as np
import random


#function: edge detection
#purpose: determine the location of edges in the image
#arguments: binarized image as uint8 [][] 
#returns: edges as a uint8 [][] 
def detect_edges(binarizedImage) :
    kernel = np.ones((3,3), np.uint8)
    dilatedImage = cv2.dilate(binarizedImage, kernel, iterations=1)
    erodedImage = cv2.erode(binarizedImage, kernel, iterations=1)
    edges = dilatedImage - erodedImage
    return edges


#function: find contours
#purpose: partitions the discovered edges into contour regions
#arguments: edges
#returns: tuple of ndarrays of shape (#pointsInContour, 2), numpy array of shape (#contours, [Next, Previous, First Child, Parent])
def find_contours(edges) :
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #reshapes contour because I do not care about OpenCV convention
    contours = [contour.reshape((-1,2)) for contour in contours]
    return contours, hierarchy

