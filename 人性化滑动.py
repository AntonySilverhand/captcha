import pyautogui
import random

def move_slide(offset_x, offset_y, left):
    pyautogui.moveTo(offset_x, offset_y,
                     duration=0.1 + random.uniform(0, 0.1 + random.randint(1, 100) / 100))

    pyautogui.mouseDown()

    offset_y += random.randint(9, 19)

    pyautogui.moveTo(offset_x + int(left * random.randint(15, 25) / 20), offset_y,
                     duration=0.1 + random.uniform(0, 0.1 + random.randint(1, 100) / 100))
    offset_y += random.randint(-9, 0)
    pyautogui.moveTo(offset_x + int(left * random.randint(18, 22) / 20), offset_y,
                     duration=random.randint(19, 31) / 100)
    offset_y += random.randint(0, 8)
    pyautogui.moveTo(offset_x + int(left * random.randint(19, 21) / 20), offset_y,
                     duration=random.randint(20, 40) / 100)
    offset_y += random.randint(-3, 3)
    pyautogui.moveTo(left + offset_x + random.randint(-3, 3), offset_y,
                     duration=0.5 + random.randint(-10, 10) / 100)
    offset_y += random.randint(-2, 2)
    pyautogui.moveTo(left + offset_x + random.randint(-2, 2), offset_y,
                     duration=0.5 + random.randint(-3, 3) / 100)


    pyautogui.mouseUp()