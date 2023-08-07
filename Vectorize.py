#final segment of prototype code
#the purpose of this module is to take a list of contours and generate efficient GCODE
#AS OF TODAY, JULY 31 2023, THIS CODE DOES NOT WORK AT ALL!!!!!! :?
from matplotlib.image import imread
import matplotlib.pyplot as plot
import numpy as np
import cv2
import inspect


#function: find nearest contour index
#purpose: as part of an effort to order the contours logically for the laser printer, a function to find the nearest point on a contour that we havent seen is necessary
#arguments: a point and the list of contours
#returns: the index of the nearest point of another contour
def find_nearest_point(point, contours):
    return
    
#function: reorder contours
#purpose: orders the contours in such a way that minimized wasted movement of the laser printer
#arguments: contours tuple
#returns: reordered contours tuple
def reorder_contours(contours):
    return


#function: rescale_contours
#purpose: take the contour information and make the new bounds (-50,50) in X-axis and Y-axis
#argument: contours tuple
#returns: scaled contours tuple
def rescale_contours(contours):
    print(len(contours))
    print(contours[0].shape)
    #working width / height
    wwsh = 96
    #determine scaling factor
    minX, maxX, minY, maxY = float('inf'), float('-inf'),float('inf'), float('-inf')
    for contour in contours : 
        for point in contour :
            currX, currY = point
            minX = min(minX, currX)
            minY = min(minY, currY)
            maxX = max(maxX, currX)
            maxY = max(maxY, currY)
    #boolean: true for portrait, false for landscape
    portrait = (maxY - minY > maxX - minX)
    if portrait :
        scale = 96 / (maxY - minY)
        translateY = -48
        translateX = -1*(((maxX - minX) / 2)*scale)
    else :
        scale = 96 / (maxX - minX)
        translateX = -48
        translateY = -1*(((maxY - minY) /2)*scale)
    #now multiply the whole image by the scale and add translation
    scaledContours = []
    for contour in contours :
        scaledContour = [(point[0] * scale + translateX, point[1] * scale + translateY) for point in contour]
        scaledContours.append(scaledContour)
    return tuple(scaledContours)


#function: generate gcode
#purpose: efficiently create a set of gcode commands to draw the desired image
#arguments: orderedContour tuple
#return: array
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


#function: add_starting_GCODE
#purpose: to append the GCODE array with starting gcode commands and first contour
#arguments: array, tuple
#returns: modified array
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


#function: add_transition_GCODE
#purpose: the next step is to repeat a process of adding a transition set of commands that preceed a draw contour set of commands
#notes: this function adds a SINGLE set of transition code and contour code. Another implementation should call this function as the contours are enumerated
#arguments: array (command list), array (contour to be added)
#output: modified array
def add_transition_GCODE(commands, contour):
    firstX, firstY = contour[0]
    #transition code
    transitionCommands = ["G4 P0",
                    "M05 S0",                    
                    "G1 F1000",
                    f"G0 X{firstX} Y{firstY}",
                    "G4 P0",
                    "M03 255",
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


#function: add ending GCODE
#purpose: tail the gcode comman array with a set of ending commands
#arguments: commands array
#returns: augmented commands array
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


#function: print_gcode
#purpose: print out gcode commands so i can see what they are without writing to a text file
#argument: array
#return: nothing
def print_gcode(gcode_commands):
    for command in gcode_commands :
        print(command)


#function: file_write_gcode
#purpose: open a file and write G-code commands
#arguments: array of strings
#returns: nothing!
def write_GCODE(gcode):
    filePath = "/Users/samsonbienstock/Desktop/Foxconn/Image_Project/Code/gcode.txt"
    with open(filePath, 'w') as file:
        for command in gcode :
            file.write(command + '\n')

