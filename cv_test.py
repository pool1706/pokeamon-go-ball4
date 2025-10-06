import cv2
import numpy as np

print("--- Starting OpenCV Diagnostic Test ---")

    # Create a blank black image (500 pixels wide, 300 pixels tall)
blank_image = np.zeros((300, 500, 3), dtype="uint8")

print("Image created. Trying to open window...")

try:
        # Display the image in a window
        cv2.imshow("Test Window", blank_image)
        
        print("Window should be open. Press any key in the window to close it.")
        
        # Wait for a key press and keep the window open
        cv2.waitKey(0)

except Exception as e:
        print(f"AN ERROR OCCURRED: {e}")

finally:
        # Clean up and close all windows
        cv2.destroyAllWindows()
        print("--- Test Finished ---")

