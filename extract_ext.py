import cv2
import numpy as np

def detect_biggest_rectangle(image):
  # Convert the image to grayscale.
  grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Apply a blur to the image to reduce noise.
  blurred_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)

  # Find the edges in the blurred image.
  edges = cv2.Canny(blurred_image, 100, 200)

  # Find the contours in the edges image.
  contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  # Find the largest contour.
  largest_contour = max(contours, key=cv2.contourArea)

  # Get the bounding rectangle of the largest contour.
  (x, y, w, h) = cv2.boundingRect(largest_contour)

  # Draw the bounding rectangle on the image.
  cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

  # Return the bounding rectangle of the largest rectangle.
  return (x, y, w, h)

# Load the image.
image = cv2.imread("templatec.jpg")

# Detect the biggest rectangle in the image.
(x, y, w, h) = detect_biggest_rectangle(image)

# Display the image with the bounding rectangle drawn on it.
cv2.imwrite('en_buyuk_dikdortgen.jpg', image)