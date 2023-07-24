#!/usr/bin/env python
# coding: utf-8

# In[38]:


from matplotlib.image import imread
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

file_path = input("Enter Filepath: ")
input_image = imread(file_path)
print(input_image.dtype)
#separate into RGB channels
r,g,b = input_image[:,:,0], input_image[:,:,1], input_image[:,:,2]
gamma = 1.04
r_const, g_const, b_const = 0.2126, 0.7152, 0.0722
grayscale_image = r_const * r ** gamma + g_const * g ** gamma + b_const * b ** gamma
fig = plt.figure(1)
img1, img2 = fig.add_subplot(121), fig.add_subplot(122)
img1.imshow(input_image)
img2.imshow(grayscale_image, cmap=plt.get_cmap('gray'))
fig.show()
plt.show()
print("done")


# In[31]:





# In[32]:





# In[33]:





# In[ ]:




