import pyautogui
import keyboard
import cv2
import numpy as np
import os
import time

"""
    This function calculates de percentaje of pixels that are red.
"""
def red_percentaje(pixels):
    width, height = pixels.size # Get the dimensions.
    red_counter = 0 # How many pixels are red.

    # Evaluate each pixel.
    for x in range(width):
        for y in range(height):
            r, g, b = pixels.getpixel((x, y)) # Get the RGB value of the pixel.
            if r >= 150 and g <= 100 and b <= 100: # R value needs to be higher to the other values for be the red color.
                red_counter += 1
    
    # Calculate the percentaje given the amount of pixels that are red.
    total_pixels = width * height
    percentaje = (red_counter / total_pixels) * 100

    return percentaje

"""
    Function that sets the zone that's going to be read.
"""
def read_screen(side):
    # Obtain the dimensions of the screen.
    screen_width, screen_height = pyautogui.size()

    # Calculate the coordinates of the center without decimals.
    x, y = screen_width //2, screen_height //2
    y += 100
    # Set the coordinates of the square.
    x1 = x - (side // 2)
    y1 = y - (side // 2)

    # Capture the area given.
    capture = pyautogui.screenshot(region=(x1, y1, side, side))

    # Convertir la captura a una imagen que OpenCV pueda procesar
    captura_np = np.array(capture)
    captura_cv2 = cv2.cvtColor(captura_np, cv2.COLOR_RGB2BGR)

    # Dibujar un rectángulo alrededor del área capturada
    cv2.rectangle(captura_cv2, (0, 0), (side - 1, side - 1), (0, 255, 0), 2)

    # Mostrar la captura con el rectángulo
    cv2.imshow("Captura con cuadro del área", captura_cv2)
    cv2.waitKey(1)
    # Cierra la ventana si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    return capture

"""
    Function that picks the average percentaje based on the user.
"""
def percentaje_picker():
    picked = []
    os.system("cls")
    print("LISTENING...")
    print("Press [f] to read the percentaje.")
    print("Press [9] to return to menu.")
    average = 0
    while not keyboard.is_pressed('9'):
        screen = read_screen(100)
        if (keyboard.is_pressed('f')):
            percentaje = red_percentaje(screen)
            picked.append(percentaje)
            average = sum(picked) / len(picked)
            os.system("cls")
            print("LISTENING...")
            print("Press [f] to read the percentaje.")
            print("Press [9] to return to menu.")
            print("PERCENTAJE: ", average, "%")
    return average

"""
    Function that parry the ball.
"""
def auto_parry(threshold):
    detector = read_screen(100)
    percentaje = red_percentaje(detector)
    if (percentaje >= threshold):
        keyboard.press('f')
        print("PARRY!")
    else:
        keyboard.release('f')

def menu():
    print("AUTO PARRY")
    print("[6] Set default percentaje (20%)")
    print("[7] Pick percentaje")
    print("[8] Start")
    print("[9] Stop")
    print("[0] Exit")

def main():
    threshold = 20
    menu()
    print("Auto-Parry DISABLED")
    while not keyboard.is_pressed('0'):
        if (keyboard.is_pressed('6')):
            threshold = 20
            os.system("cls")
            menu()
            print("RESTORED DEFAULT PERCENTAJE")
        if (keyboard.is_pressed('7')):
            threshold = percentaje_picker()
            os.system("cls")
            menu()
            print("New percentaje: ", threshold, "%")
        if (keyboard.is_pressed('8')):
            print("Auto-Parry ENABLED")
            while not keyboard.is_pressed('9'):
                auto_parry(threshold)
            os.system("cls")
            menu()
            print("Auto-Parry DISABLED")
    return 0

main()