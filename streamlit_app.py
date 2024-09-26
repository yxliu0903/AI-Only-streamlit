import streamlit as st
import os
from PIL import Image

# Define the paths to the image folders
folder1 = 'data/graph/v8_with-gold-solution'
folder2 = 'data/graph/v8_with-gold-solution_cleaned'

# Get a list of images from each folder
images_folder1 = sorted([f for f in os.listdir(folder1) if f.endswith(('.png', '.jpg', '.jpeg'))])
images_folder2 = sorted([f for f in os.listdir(folder2) if f.endswith(('.png', '.jpg', '.jpeg'))])

# Ensure both folders have the same number of images
assert len(images_folder1) == len(images_folder2), "Both folders must contain the same number of images."

# Sidebar for image selection
selected_image_index = st.sidebar.selectbox("Select Image Number", range(1, len(images_folder1) + 1)) - 1

# Load and display the selected images
image1 = Image.open(os.path.join(folder1, images_folder1[selected_image_index]))
image2 = Image.open(os.path.join(folder2, images_folder2[selected_image_index]))

# Display images side by side
col1, col2 = st.columns(2)

with col1:
    st.image(image1, caption=f"Image from Folder 1: {images_folder1[selected_image_index]}", use_column_width=True)

with col2:
    st.image(image2, caption=f"Image from Folder 2: {images_folder2[selected_image_index]}", use_column_width=True)
