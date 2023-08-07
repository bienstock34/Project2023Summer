#middle of prototype code
#this module should start with a binarized image
#processes of this module include edge detection and contour determination
import cv2
import matplotlib.pyplot as plot
import numpy as np
import random


#function: Detect Edges
#purpose: Using the binarized image, transform into an edge represantation: 0s for no edge, 1s for yes edge
#arguments: uint8 array
#returns: uint8 array 
def detect_edges(binarizedImage) :
    kernel = np.ones((3,3), np.uint8)
    dilatedImage = cv2.dilate(binarizedImage, kernel, iterations=1)
    erodedImage = cv2.erode(binarizedImage, kernel, iterations=1)
    edges = dilatedImage - erodedImage
    return edges


#function: Find Contours
#purpose: Partition the discovered edges into contours
#arguments: uint8 array
#returns: tuple: ndarrays
def find_contours(edges) :
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #reshapes contour because I do not care about OpenCV convention
    contours = [contour.reshape((-1,2)) for contour in contours]
    return contours, hierarchy

