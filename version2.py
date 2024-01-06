import cv2
import numpy as np
import pyautogui
import keyboard
import os

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
"""
def get_dimensions():
    # Obtain the dimensions of the screen.
    screen_width, screen_height = pyautogui.size()

    # Eliminates the HUD of the game.
    screen_width = screen_width // 2
    screen_height = screen_height // 2

    # Calculate the minimun dimensions of the ball to parry.
    w_threshold = screen_width * 0.13
    h_threshold = screen_height * 0.23

    return w_threshold, h_threshold

def auto_parry(w_threshold, h_threshold):
    screen = read_screen()
    frame = np.array(screen)
    ball = find_ball(frame)
    x, y, w, h = (0, 0, 0, 0)
    if ball:
        x, y, w, h = ball

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Dibuja un cuadrado verde alrededor de la pelota

        # Agregar texto con los valores de ancho y altura dentro del rectángulo
        texto = f'Ancho: {w}, Altura: {h}'
        cv2.putText(frame, texto, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imshow('Red Ball Detection', frame)

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