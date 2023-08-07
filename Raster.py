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

#Date: 8/1/23

#function: import_file
#arguments: none
#returns: loaded-in pixel image GRAYSCALE
def import_file():
    #prompt user for filepath to pixel image
    fileName = input("Enter Filename: ") 
    #concatenate filename with path to Image folder
    filePath = "/Users/samsonbienstock/Desktop/Foxconn/Image_Project/Testing/" + fileName
    #load image from file into memory AS GRAYSCALE
    inputImage = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE) 
    return inputImage
    
    
#Date: 8/2/23
#Refined binarization attempt with Otsu's Thresholding
#function: binarize
#purpose: binarize a color image
#inputs: uint8 array with 3 channels
#outputs: binary uint8 array with 1 channel
def binarize_image(image) :
    image = cv2.medianBlur(image, 5)
    th = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)
    return th

#apply low-frequency pass filter