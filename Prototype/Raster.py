#!/usr/bin/env python
# coding: utf-8

# In[2]:


#beginning of Prototype Code
#the job of this code is to take in the Raster File and prepare it as necessary
from matplotlib.image import imread
import matplotlib.pyplot as plot
import numpy as np


#function: import_file
#arguments: none
#returns: loaded-in pixel image
def import_file():
    #prompt user for filepath to pixel image
    fileName = input("Enter Filename: ") 
    #concatenate filename with path to Image folder
    filePath = "/Users/samsonbienstock/Desktop/Foxconn/Image_Project/Code/" + fileName
    #load image from file into memory
    inputImage = imread(filePath) 
    #debugging code:
    #print(inputImage.dtype)
    #print(np.min(inputImage))
    #print(np.max(inputImage))
    print(inputImage.shape)
    return inputImage


#function: grayscale
#arguments: pixel image array
#returns: grayscale image of the same size
def grayscale(inputImage):
    red = inputImage[:,:,0].astype(np.uint16)
    green = inputImage[:,:,1].astype(np.uint16)
    blue = inputImage[:,:,2].astype(np.uint16)
    #redC, greenC, blueC = 0.2126, 0.7152, 0.0722
    grayscaledArray = ((red + green + blue) // 3).astype(np.uint8)
    #debugging code:
    #print(grayscaledArray.dtype)
    #min_value = np.min(grayscaledArray)
    #max_value = np.max(grayscaledArray)
    #print(min_value, max_value)
    return grayscaledArray
    
    
#function: binarize
#arguments: pixel image array
#returns: binarized image of the same size
def binarize(grayImage):
    #should be a cutoff number between 1-254, larger numbers = more black, smaller numbers = more white 
    threshold = 128
    #create new array
    binarizedArray = grayImage.copy()
    binarizedArray[grayImage >= threshold] = 1
    binarizedArray[grayImage < threshold] = 0
    #debugging code:
    #print("Threshold:", threshold)
    return binarizedArray
    

if __name__ == "__main__":
    p=1
    #unit test code: import
    #inputImage = import_file()  


    #unit test code: grayscale
    #grayscaledImage = grayscale(inputImage)


    #unit test code: binarize
    #binarizedImage = binarize(grayscaledImage)
    #height, width = binarizedImage.shape
    #print("pixels: ", height*width)
    #print(np.sum(binarizedImage == 1))


    #system test code
    #inputImage = import_file()
    #grayscaledImage = grayscale(inputImage)
    #binarizedImage = binarize(grayscaledImage)


    #plot.figure(figsize=(100,50))
    #plot.subplot(1,3,1)
    #plot.imshow(inputImage)
    #plot.subplot(1,3,2)
    #plot.imshow(grayscaledImage, cmap="gray")
    #plot.subplot(1,3,3)
    #plot.imshow(binarizedImage, cmap="gray")



# In[ ]:





# In[ ]:




