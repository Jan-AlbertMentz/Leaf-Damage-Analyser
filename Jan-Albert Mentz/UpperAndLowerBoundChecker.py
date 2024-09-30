import cv2
import numpy as np

# Hex colors
hex_colors = [
    "#acba33",  # healthy leaf
    "#1d4900",  # healthy leaf
    "#347a00",  # healthy leaf
    "#4b8300",  # healthy leaf
    "#4b8000",  # healthy leaf
    "#6b8d02",  # less healthy
    "#005004",  # very healthy
    "#708c1d",  # healthy leaf
    "#acb331",  # healthy leaf
    "#81960b",  # healthy leaf
    "#86c103",  # healthy
    "#93c003",  # healthy
    "#095600",  # healthy
    "#5b9107"   # healthy
]
# Convert hex to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Convert RGB to HSV
def rgb_to_hsv(rgb_color):
    rgb_color = np.uint8([[rgb_color]])
    hsv_color = cv2.cvtColor(rgb_color, cv2.COLOR_RGB2HSV)
    return hsv_color[0][0]

# Convert hex to HSV
hsv_colors = [rgb_to_hsv(hex_to_rgb(color)) for color in hex_colors]

# Find the min and max HSV values across all colors
hsv_array = np.array(hsv_colors)
lower_bound = np.min(hsv_array, axis=0)
upper_bound = np.max(hsv_array, axis=0)

print(f'Lower: {lower_bound} Upper: {upper_bound}')
