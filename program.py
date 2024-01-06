import os
dependencies = []
os.system("cls")

try:
    import numpy as np
    print("NumPy: INSTALLED")
except ImportError:
    print("NumPy: NOT INSTALLED")
    dependencies.append('numpy')

try:
    import pyautogui
    print("PyAutoGUI: INSTALLED")
except ImportError:
    print("PyAutoGUI: NOT INSTALLED")
    dependencies.append('pyautogui')

try:
    import keyboard
    print("keyboard: INSTALLED")
except ImportError:
    print("keyboard: NOT INSTALLED")
    dependencies.append('keyboard')

try:
    import cv2
    print("opencv-python: INSTALLED")
except ImportError:
    print("opencv-python: NOT INSTALLED")
    dependencies.append('opencv-python')

if (len(dependencies) != 0):
    print("Please copy and paste the next lines of code individually on a terminal of your computer and restart the program:")
    for library in dependencies:
        print("pip install ", library)
    os.system("pause")
else:
    os.system("pause")
    os.system("cls")

import cv2
import numpy as np
import pyautogui
import keyboard

"""
    Function that finds the ball on the screen.
    
    Args:
        frame (Any): A numpy array that contains the frame to analyize.
    Returns:
        tuple: The coordinates and the width and height of the ball detected.

"""
def find_ball(frame):
    # Define the lower and upper limits for the color red in RGB
    lower_red = np.array([100, 0, 0])
    upper_red = np.array([255, 100, 100])

    # Create a mask for the color red in the RGB color space
    mask = cv2.inRange(frame, lower_red, upper_red)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
    for contour in contours:
        # Get the bounding rectangle for each contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # Add a condition to consider only contours with w and h greater than 30
        if w > 30 and h > 30:
            return (x, y, w, h)
    
    return None


"""
    Function that sets the zone that's going to be read.
    Returns:
        Any: The screen recording.
"""
def read_screen():
    # Obtain the dimensions of the screen.
    screen_width, screen_height = pyautogui.size()

    # Calculate the coordinates of the center without decimals.
    x, y = screen_width //2, screen_height //2

    # Eliminates the HUD of the game.
    screen_width = screen_width // 2
    screen_height = screen_height // 2

    # Set the coordinates of the square.
    x1 = x - (screen_width // 2)
    y1 = y - (screen_height // 2)

    # Capture the area given.
    capture = pyautogui.screenshot(region=(x1, y1, screen_width, screen_height))

    return capture

"""
    Function that automatically sets the size of the ball to parry based on the screen size.

    Returns:
        Tuple: The minimum width and height of the ball to parry.
"""
def get_dimensions():
    # Obtain the dimensions of the screen.
    screen_width, screen_height = pyautogui.size()

    # Eliminates the HUD of the game.
    screen_width = screen_width // 2
    screen_height = screen_height // 2

    # Calculate the minimum dimensions of the ball to parry.
    w_threshold = screen_width * 0.13
    h_threshold = screen_height * 0.23

    return w_threshold, h_threshold


"""
    Function that makes the Auto Parry.

    Args:
        w_threshold (float): The minimum width of the ball.
        h_threshold (float): The minimum height of the ball.
"""
def auto_parry(w_threshold, h_threshold):
    screen = read_screen() # Get the screen.
    frame = np.array(screen) # Convert the screen to a readable frame.
    ball = find_ball(frame)
    x, y, w, h = (0, 0, 0, 0)
    # If there's the ball.
    if ball:
        x, y, w, h = ball # Get the dimensions of the ball.

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw a green rectangle around the ball

        # Add text with the width and height values:
        texto = f'Width: {w}, Height: {h}'
        cv2.putText(frame, texto, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imshow('Red Ball Detection', frame) # Show the screen

    # If the size of the ball surprass the threshold.
    if (w >= w_threshold and h >= h_threshold):
        keyboard.press('f')
    else:
        keyboard.release('f')
    
"""
    Function that makes the main menu.
"""
def menu():
    print("AUTO PARRY")
    print("[8] Start")
    print("[0] Exit")

def main():
    menu()
    while not keyboard.is_pressed('0'):
        if (keyboard.is_pressed('8')):
            w_threshold, h_threshold = get_dimensions()
            os.system("cls")
            print("Auto-Parry: ENABLED")
            print("[9] Stop")
            while not keyboard.is_pressed('9'):
                auto_parry(w_threshold, h_threshold)

                # Exit loop if '9' key is pressed
                if cv2.waitKey(1) & 0xFF == ord('9'):
                    break
            cv2.destroyAllWindows()
            os.system("cls")
            menu()
            print("Auto-Parry: DISABLED")
    return 0

main()