# flashing-lights

## Project aimed to be an electric scooter safety and aesthetic accessory

###
- Motivation:
  - Electric scooters and bikes are gaining popularity, especially amongst college students and teenagers. Though these mundane means of transportation offer immense convinience, students and teenagers often end up speeding on busy roads which can lead to dangerous accidents. Our product is aimed to tackle this problem and ensure the safety of students and teenagers.
  
- Working:
  - The product consists of an IMU (inertial measurement unit), WS2812B LED strip, and ESP32. 
  - The IMU measures the acceleration of the vehicle and is thus supposed to be placed flat on the vehicle. 
  - The LEDs have a default flashing pattern when the vehicle is in motion. In the case that the user travels faster than an arbitrary set value, 
  the LEDs start flashing a different color to indicate unsafe standard. 
  - Along with change in light color, an email (can also be over an app or a text message) is sent to the guardian/ parent to notify them.
  
- Technicalities:
  - Micropython is used on ESP32
  - The comunication protocol between the IMU and ESP32 is I2C.
  - The LEDs are controlled using a PWM signal outputted by the GPIO pins of the ESP32. 
  - MQTT is used to communicate over the

  
    
   
