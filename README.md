# Gravity-Etch-a-Sketch
Mini Etch-a-sketch using accelerometer and turtle library, for CircuitPlayground boards with TFT Gizmo

## Requirements 

### Material

* Circuit Playground Express or Bluefruit
* TFT Gizmo

### Libs 
* adafruit_gizmo
* adafruit_lis3dh
* adafruit_turtle (included in this repo for CP v5.0.0 Beta 3)

## Controls

* Gravity set the angle of heading of the turtle
* Tilt set the velocity
* Button A control the color.
  * Default color is White. next are : Pink, Red, Orange, Yellow, Green, Blue, Purple then White etc.
  * Brief press set the color to the next on the list.
  * Long press set the color to random (from the rainbow colors)
* Button B 
  * Brief press pauses the turtle 
  * Long press reset the display (intented to screenshot, but not possible ATM)
* Shake reset the display too






