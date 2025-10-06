import cv2
import numpy as np
import mss
import subprocess
import time

# --- First-time setup: Install the 'pywin32' library ---
# This is needed to find the scrcpy window by its title.
try:
    import win32gui
except ImportError:
    print("First-time setup: Installing the 'pywin32' library...")
    # We use subprocess to run pip from within the script
    subprocess.run(['pip', 'install', 'pywin32'], check=True)
    print("Installation complete. Please run the script again.")
    # Exit so the user can re-run with the library installed
    exit()

# --- CONFIGURATION ---
# UPDATE THIS to the EXACT title of your scrcpy window
SCRCPY_WINDOW_TITLE = "Pixel 7" 

# ADB path - Update this if you placed platform-tools elsewhere
ADB_PATH = "C:\\platform-tools\\adb.exe"

# --- HSV Color Range for Circle Detection ---
# This is crucial and will need to be tuned. This is set for a generic red.
LOWER_COLOR_BOUND = np.array([0, 150, 150])
UPPER_COLOR_BOUND = np.array([10, 255, 255])

def execute_adb_swipe(start_x, start_y, end_x, end_y, duration_ms):
    """Executes a swipe command on the connected Android device via ADB."""
    command = [
        ADB_PATH, "shell", "input", "swipe",
        str(int(start_x)), str(int(start_y)), str(int(end_x)), str(int(end_y)), str(duration_ms)
    ]
    print(f"Executing ADB Swipe: {command}")
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except Exception as e:
        print(f"Error executing ADB command: {e}")

def find_target_circle(screen_image):
    """Analyzes an image to find the colored target circle."""
    hsv_image = cv2.cvtColor(screen_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, LOWER_COLOR_BOUND, UPPER_COLOR_BOUND)
    
    # Use HoughCircles to find circles in the masked image
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100, param1=50, param2=30, minRadius=10, maxRadius=200)
    
    if circles is not None:
        # Return the first circle found
        return np.round(circles[0, :]).astype("int")[0]
    return None

def main():
    print("--- Pokémon Go Real-Time Assistant ---")
    print(f"Searching for window with title: '{SCRCPY_WINDOW_TITLE}'...")
    
    hwnd = win32gui.FindWindow(None, SCRCPY_WINDOW_TITLE)
    if hwnd == 0:
        print(f"ERROR: Could not find the '{SCRCPY_WINDOW_TITLE}' window.")
        print("Please make sure scrcpy is running and visible.")
        return

    print("scrcpy window found! Starting screen capture.")
    
    with mss.mss() as sct:
        while True:
            try:
                rect = win32gui.GetWindowRect(hwnd)
                x1, y1, x2, y2 = rect
                monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}

                # Grab the screen capture
                img = np.array(sct.grab(monitor))
                # Convert from BGRA to BGR for processing
                img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                # Find the circle
                circle_data = find_target_circle(img_bgr)
                
                if circle_data is not None:
                    (x, y, r) = circle_data
                    print(f"Circle Detected! Center: ({x}, {y}), Radius: {r}px")
                    # Draw a green circle on our feed to show what we've found
                    cv2.circle(img_bgr, (x, y), r, (0, 255, 0), 4)
                    
                    # If the circle is small enough, throw the ball
                    if r < 30: 
                        print("EXCELLENT THROW CONDITION MET! Firing ADB command...")
                        start_x_win, start_y_win = monitor['width'] // 2, monitor['height'] - 50
                        end_x_win, end_y_win = x, y 
                        execute_adb_swipe(start_x_win, start_y_win, end_x_win, end_y_win, 300)
                        print("Throw command sent. Waiting 5 seconds before next attempt...")
                        time.sleep(5)

                # Show the live feed
                cv2.imshow('Computer Vision Feed', img_bgr)

                # Press 'q' to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            except Exception as e:
                if "ScreenShotError" in str(e):
                    print("scrcpy window has been closed. Exiting.")
                    break
                else:
                    print(f"An unexpected error occurred: {e}")
                    break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()




