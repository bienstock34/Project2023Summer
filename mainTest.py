#!/usr/bin/env python
# coding: utf-8

# In[3]:


#THIS CODE WORKS
#beginning of Prototype Code
#the job of this code is to take in the Raster File and prepare it as necessary
#FLOW:
#(1) JPEG
#(2) Grayscale uint8 array
#(3) Binary uint8 array
from matplotlib.image import imread
import matplotlib.pyplot as plot
import numpy as np
import cv2
import random
import inspect

#Date: 8/1/23

#function: Import File
#purpose: act as the first step of the software: asking the user for a file, and then reading the file as a grayscale image
#arguments: none
#returns: uint8 array
def import_file():
    #prompt user for filepath to pixel image
    fileName = input("Enter Filename: ") 
    #concatenate filename with path to Image folder
    filePath = "/Users/samsonbienstock/Desktop/Foxconn/Image_Project/Testing/" + fileName
    #load image from file into memory AS GRAYSCALE
    inputImage = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE) 
    return inputImage
    
    

#function: Binarize Image
#purpose: Transform the image into binary pixels instead of grayscale, employing blur and adaptive threshold
#inputs: uint8 array (values 0-255)
#outputs: uint8 array (0 or 1)
def binarize_image(image) :
    image = cv2.medianBlur(image, 5)
    #th = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)
    _, th = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th

#future work: apply low-frequency pass filter


#function: Detect Edges
#purpose: Using the binarized image, transform into an edge represantation: 0s for no edge, 1s for yes edge
#arguments: uint8 array
#returns: uint8 array 
def detect_edges(binarizedImage) :
    print(binarizedImage.shape)
    kernel = np.ones((3,3), np.uint8)
    #dilatedImage = cv2.dilate(binarizedImage, kernel, iterations=1)
    #erodedImage = cv2.erode(binarizedImage, kernel, iterations=1)
    #edges = dilatedImage - erodedImage
    edges = cv2.Canny(binarizedImage, 30, 70)
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


#function: Rescale Contours
#purpose: Change the coordinate data of the contours so that they match the engravement area in millimeters
#argument: tuple: ndarray
#returns: tuple: ndarray
def rescale_contours(contours):
    print('hi')
    #working width / height in mm
    wwsh = 80
    #TRANSLATE 1
    translateOneContours = translateOne(contours)
    midScaledContours, maxX, maxY = midScale(translateOneContours, wwsh)
    translateTwoContours = translateTwo(midScaledContours, wwsh, maxX, maxY)
    return translateTwoContours

def translateOne(contours) :
    #determine translate 1 distances
    print(3)
    minX = 55000
    minY = 55000
    for contour in contours : 
        for point in contour :
            currX, currY = point
            minX = min(minX, currX)
            minY = min(minY, currY)
    print("minX:", minX)
    print("minY:", minY)
    translateOneContoursArray = []
    for contour in contours :
        translateOneContour = [(point[0] - minX, point[1] - minY) for point in contour]
        translateOneContoursArray.append(translateOneContour)
    translateOneContours = tuple(translateOneContoursArray)
    return translateOneContours

def midScale(translateOneContours, wwsh) :
    maxY = -1
    maxX = -1
    for contour in contours : 
        for point in contour :
            currX, currY = point
            maxX = max(maxX, currX)
            maxY = max(maxY, currY)
    if maxX == 0:
        maxX = 1
    if maxY == 0:
        maxY = 1
    scale = wwsh / max(maxX, maxY)
    scaledContoursArray = []
    for contour in translateOneContours:
        scaledContour = []
        for point in contour:
            scaledX = point[0] * scale if scale != 0 else 0
            scaledY = point[1] * scale if scale != 0 else 0
            scaledContour.append((scaledX, scaledY))
        scaledContoursArray.append(scaledContour)
    scaledContours = tuple(scaledContoursArray)
    #subprocess
    maxX = maxX * scale
    maxY = maxY * scale
    return scaledContours, maxX, maxY

def translateTwo(midScaledContours, wwsh, maxX, maxY) :
    translateTwoContoursArray = []
    if (maxY>=maxX) :
        translateY = (-1*wwsh) / 2
        translateX = (-1*maxX) / 2
    else :
        translateX = (-1*wwsh) / 2
        translateY = (-1*maxY) / 2
    translateTwoContoursArray = []
    for contour in midScaledContours :
        translateTwoContour = [(point[0] + translateX, point[1] + translateY) for point in contour]
        translateTwoContoursArray.append(translateTwoContour)
    translateTwoContours = tuple(translateTwoContoursArray)
    return translateTwoContours



#function: Generate GCODE
#purpose: create a set of gcode commands to draw the desired image
#arguments: tuple: ndarray
#return: array: string lines
def generate_GCODE(commands, contours) :
    #step 1: append starting code and first contour code
    commands = add_starting_GCODE(commands, contours)
    #step 2: append transition code followed by contour code for contours 2...numContours
    #we start on contour 2 since contour 1 has already been appended with the starting code
    contourCounter = 2 
    t = 10
    while contourCounter <= len(contours) :
        if len(contours[contourCounter-1])>t :
            commands = add_transition_GCODE(commands, contours[contourCounter-1])
        contourCounter += 1
    #step 3: end code
    commands = add_ending_GCODE(commands)
    return commands


#function: Add Starting GCODE
#purpose: Initiate the GCODE array with starting gcode commands, first contour commands
#arguments: array, tuple: ndarray
#returns: array
#future work: fix inefficiency- function takes all contours but only needs contours[0]
def add_starting_GCODE(commands, contours):
    firstX, firstY = contours[0][0]
    #starting code
    initialCommands = ["M05 S0",
                     "G90",
                     "G21",
                     "G1 F1000",
                     f"G0 X{firstX} Y{firstY}",#SHOULD BE G1, BUT NCVIEWER WORKS BETTER WITH G0 REMEMBER TO CHANGE
                     "G4 P0",
                     "M03 S255",
                     "G4 P0",
                     "G1 F600.000000"]
    commands.append(" ")
    commands.append("; starting code")
    #append one-by-one
    for command in initialCommands :
        commands.append(command)
    commands.append(" ")
    commands.append("; first contour")
    #append first contour code
    for point in contours[0][1:] :
        currX = point[0]
        currY = point[1]
        currCommand = f"G1 X{currX} Y{currY}"
        commands.append(currCommand)
    #return the modified command list
    return commands


#function: Add Transition GCODE
#purpose: Repeat the process of appending transition set of commands, next contour, for all remaining contours
#arguments: array, tuple: ndarray
#returns: array
def add_transition_GCODE(commands, contour):
    firstX, firstY = contour[0]
    #transition code
    transitionCommands = ["G4 P0",
                    "M05 S0",                    
                    "G1 F1000",
                    f"G0 X{firstX} Y{firstY}",
                    "G4 P0",
                    "M03 S255",
                    "G4 P0",
                    "G1 F600.000000"]
    commands.append(" ")
    commands.append("; transition code")
    for command in transitionCommands : 
        commands.append(command)
    commands.append(" ")
    commands.append("; new contour")
    #contour code
    t=10
    for point in contour :
        currX = point[0]
        currY = point[1]
        commands.append(f"G1 X{currX} Y{currY}")
    #this line fixes a bug where the GCODE does not finish each contour
    commands.append(f"G1 X{firstX} Y{firstY}") #this actually finishes the contour
    return commands


#function: Add Ending GCODE
#purpose: Add GCODE command tail with a set of ending commands
#arguments: array
#returns: array
def add_ending_GCODE(commands) :
    endingCommands = ["G4 P0",
                     "M05 S0",
                     "G1 F1000",
                     "G1 X0 Y0",
                     "M18"]
    commands.append(" ")
    commands.append("; end code")
    for command in endingCommands :
        commands.append(command)
    return commands


#function: Print GCODE
#purpose: testing function: print out gcode commands
#argument: array
#return: -
def print_gcode(gcode_commands):
    for command in gcode_commands :
        print(command)


#function: Write GCODE
#purpose: Write G-code commands to file: gcode.txt on my desktop
#arguments: array
#returns: -
def write_GCODE(gcode):
    filePath = "/Users/samsonbienstock/Desktop/Foxconn/Image_Project/Code/gcode.txt"
    with open(filePath, 'w') as file:
        for command in gcode :
            file.write(command + '\n')






inputImage = import_file()
binarizedImage = binarize_image(inputImage)
edges = detect_edges(binarizedImage)
contours, hierarchy = find_contours(edges)
rescaledContours = rescale_contours(contours)
GCODE = []
GCODE = generate_GCODE(GCODE, rescaledContours)
write_GCODE(GCODE)





# In[ ]:




