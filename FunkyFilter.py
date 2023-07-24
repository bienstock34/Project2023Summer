#!/usr/bin/env python
# coding: utf-8

# In[47]:


from matplotlib.image import imread
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

file_path = input("Enter Filepath: ")
input_image = imread(file_path)
#initialize new image
new_image = np.zeros((input_image.shape), dtype = np.uint8)

#print(input_image.shape)


# In[48]:


#separate into RGB channels
r,g,b = input_image[:,:,0], input_image[:,:,1], input_image[:,:,2]
#increase the red values
r_new = (r**4.55)
max_value = np.max(r_new)
r_new = (r_new/max_value)*255
max_value = np.max(r_new)


g_new = (g**0.83)

b_new = b/19

new_image[:, :, 0] = r_new
new_image[:, :, 1] = g_new
new_image[:, :, 2] = b
fig = plt.figure(1)
img1, img2 = fig.add_subplot(121), fig.add_subplot(122)
img1.imshow(input_image)
img2.imshow(new_image)
fig.show()
plt.show()



# In[ ]:





# In[ ]:





# In[ ]:




