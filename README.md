# Integration Project

Nicholas Hallman 150357790  
Yicheng Fan 146801620

CP320

Professor Terry Sturtevant  

## Circuit Overview

In this project, four devices were connected to a raspberry pi to demonstrate inter-device communication. We selected a stepper motor, distance sensor, capacitive keypad, and 8x8 led matrix. All devices run on 3.v volts of power supplied by the pi and none of the devices required resisting. The output of the sensor, however, is analog and required an analog-to-digital converter for recognition by the raspberry pi. The devices used a variety of different communication protocols. The sensor and motor were both driven by standard GPIO. However, the 8x8 led matrix used SPI and the keypad used a two-wire interface over SDA and SCL. While this interface sounds a lot like I2C it is not. 

## Block Diagram

![Block Diagram](https://raw.githubusercontent.com/NicholasHallman/Integration-Project/master/Block%20Diagram.png)

## Breakdown  
### Distance Sensor  
The distance sensor outputs an analog signal and is powered by 3.3 volts
### Analog-to-Digital  
The analog-to-digital converter relies on the SPI interface to communicate with the pi. It is powered by a 3.3v source on the pi. This device is connected to channel 0 on the pi along side the LED Matrix which is daisy chained with this device. 
### Stepper Motor  
The stepper motor has a four-wire controller that controls the four electromagnets in the motor. By interfacing with the controller over the GPIO pins on the pi in sequence the motor spins. 
### Capacitive Keyboard  
The keypad connects over a two-wire interface like I2 C. The connection interfaces with the pi over SDA / SCL and can be controller by timing the exchange of data. 
### 8x8 LED Matrix  
The 8x8 led matrix is the second SPI device on the project. The device is daisy chained with the analog-to-digital converter. Both devices interface across device channel 0.