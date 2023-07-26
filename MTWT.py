#!/usr/bin/env python
# coding: utf-8

# In[5]:


#MTWT stands for maybe the whole thing?
import cv2
import matplotlib.pyplot as plt

def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # Apply binarization (thresholding)
    _, binary_image = cv2.threshold(blurred_image, 200, 255, cv2.THRESH_BINARY)

    return binary_image

def generate_gcode(contours, scale_factor=8.5):
    gcode = ""
    for contour in contours:
        for point in contour:
            x, y = point[0]
            x_scaled, y_scaled = x / scale_factor, y / scale_factor
            gcode += f"G1 X{x_scaled:.2f} Y{y_scaled:.2f} F100\n"
    return gcode

if __name__ == "__main__":
    file_path = input("Enter Filepath: ")

    try:
        binary_image = preprocess_image(file_path)

        # Perform edge detection on the binarized image
        edges = cv2.Canny(binary_image, 50, 150)

        # Find contours in the binarized image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Generate G-code from the contours with scaling
        gcode = generate_gcode(contours)

        # Create a figure to display the images
        plt.figure(figsize=(12, 6))

        # Original Image
        plt.subplot(1, 3, 1)
        plt.imshow(cv2.imread(file_path, cv2.IMREAD_GRAYSCALE), cmap='gray')
        plt.title('Original Image')
        plt.axis('off')

        # Binarized Image
        plt.subplot(1, 3, 2)
        plt.imshow(binary_image, cmap='gray')
        plt.title('Binarized Image')
        plt.axis('off')

        # Edge-Detected Image
        plt.subplot(1, 3, 3)
        plt.imshow(edges, cmap='gray')
        plt.title('Edge-Detected Image')
        plt.axis('off')

        plt.show()

        # Print the generated G-code
        print("Generated G-code:")
        print(gcode)

    except Exception as e:
        print(f"Error: {e}")


# In[ ]:




