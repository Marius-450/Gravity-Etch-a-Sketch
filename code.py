import board
import busio
import time
import math
from random import randint
from adafruit_gizmo import tft_gizmo
import adafruit_lis3dh

from adafruit_turtle import Color, turtle
import digitalio


# Create the TFT Gizmo display
display = tft_gizmo.TFT_Gizmo()



# shake sensitivity, lower=more sensitive
SHAKE_THRESHOLD = 25

# Accelerometer setup
accelo_i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
accelo = adafruit_lis3dh.LIS3DH_I2C(accelo_i2c, address=0x19)


# functions

def get_angle():
    x, y, z = accelo.acceleration
    angle = math.degrees(math.atan2(y,x)) + 90.0
    if angle < 0:
        angle = 360 + angle
    #print(angle, abs(z))
    return (angle, abs(z))


# init buttons :
button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.DOWN

button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.DOWN

# state variables

# color choice
# random override the color choice
# long press on button a toggle random_color to True / False
# when random_color is False, press button a to increment color_choice

random_color = False
color_choice = 6

# buttons
but_a = False
but_b = False

# pause

pause = False

# Warp

warp = False


turtle1 = turtle(display)

print("Turtle time! Lets follow the slippery slope...")

colors = (Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.BLUE, Color.PURPLE, Color.WHITE, Color.PINK)

turtle1.pendown()


while True:
    # Turtle gravity esk-a-sketch
    angle, z = get_angle()
    # wraparound to stay on the display
    t1x, t1y = turtle1.pos()
    #print(t1x, t1y)

    if abs(t1x) > 120:
        if warp:
            if t1x > 0:
                t1x = -120
            else:
                t1x = 120
        else:
            if t1x > 0:
                t1x = 119
            else:
                t1x = -120
        turtle1.penup()
        turtle1.goto(t1x, t1y)
        turtle1.pendown()

    if abs(t1y) > 120:
        if warp:
            if t1y > 0:
                t1y = -120
            else:
                t1y = 120
        else:
            if t1y > 0:
                t1y = 120
            else:
                t1y = -119
        turtle1.penup()
        turtle1.goto(t1x, t1y)
        turtle1.pendown()


    turtle1.setheading(angle)

    if pause == False and z < 9.65:
        z = 10-z
        if z < 3:
            z = 3
        if z > 8:
            z = 8
        # random color
        if random_color:
            turtle1.pencolor(colors[randint(0,5)])
        else:
            turtle1.pencolor(colors[color_choice])
        turtle1.forward(z)

    # actions for pressing or releasing buttons
    if button_a.value and but_a == False:
        print("button a pressed")
        a_presstime = time.monotonic()
        but_a = True

    if but_a and button_a.value == False:
        print("button a released")
        if time.monotonic() - a_presstime > 2.0:
            print("long press on button a released")
            random_color = not random_color
        else:
            color_choice += 1
            if color_choice == 8:
                color_choice = 0
        but_a = False

    if button_b.value and but_b == False:
        print("button b pressed")
        b_presstime = time.monotonic()
        but_b = True

    if but_b and button_b.value == False:
        # print("button b released")
        if pause:
            if time.monotonic() - b_presstime > 2.0:
                # long press released
                turtle1.home()
                turtle1.clear()
            else:
                # short press released
                pause = False
        else:
            pause = True
        but_b = False
    if accelo.shake(SHAKE_THRESHOLD, 6, 0.04):
        # TODO : neopixel reaction
        turtle1.home()
        turtle1.clear()
    time.sleep(0.01)