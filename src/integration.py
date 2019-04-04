
import RPi.GPIO as GPIO
import spidev
import time

from luma.core import legacy
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from PIL import Image

HALF_BIT_TIME=.001
CHARACTER_DELAY=5*HALF_BIT_TIME

UM_BITS=16

runningAngle = 0

GPIO.setmode(GPIO.BCM)

stepper_pins=[13,16,26,21]
SCLPin = 17
SDOPin = 4

GPIO.setup(stepper_pins,GPIO.OUT)
GPIO.setup(SCLPin,GPIO.OUT)
GPIO.setup(SDOPin,GPIO.IN)
GPIO.output(SCLPin,GPIO.HIGH)

time.sleep(HALF_BIT_TIME)

stepper_sequence=[]
stepper_sequence.append([GPIO.HIGH, GPIO.LOW, GPIO.LOW,GPIO.LOW])
stepper_sequence.append([GPIO.HIGH, GPIO.HIGH, GPIO.LOW,GPIO.LOW])
stepper_sequence.append([GPIO.LOW, GPIO.HIGH, GPIO.LOW,GPIO.LOW])
stepper_sequence.append([GPIO.LOW, GPIO.HIGH, GPIO.HIGH,GPIO.LOW])
stepper_sequence.append([GPIO.LOW, GPIO.LOW, GPIO.HIGH,GPIO.LOW])
stepper_sequence.append([GPIO.LOW, GPIO.LOW, GPIO.HIGH,GPIO.HIGH])
stepper_sequence.append([GPIO.LOW, GPIO.LOW, GPIO.LOW,GPIO.HIGH])
stepper_sequence.append([GPIO.HIGH, GPIO.LOW, GPIO.LOW,GPIO.HIGH])

#spi init

channel=1
 
serialpi = spidev.SpiDev()
serialpi.open(0,0)
serialpi.max_speed_hz = 5000

# matrix init

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)

def main():

    userChoice = int(input("Pick a mode (1: sensor -> motor, 2: keypad -> matrix): "))
    if userChoice == 1:
        try:
            while(True):
                speed = get_sensor()
                if(speed > 2):
                    speed = 2
                if(speed < 0):
                    speed = 0
                set_motor(speed)
        except:
            cleanup()
    if userChoice == 2:
        get_keypad()


def set_motor(speed): 
    speed = speed / 2
    speed = abs(speed - 1)
    speed += 1
    speed -= .999

    for row in stepper_sequence:
        GPIO.output(stepper_pins,row)
        time.sleep(speed) # value between 1 -> 0.001

    return None


def get_sensor():
    adc=serialpi.xfer2([1,(8+channel)<<4,0])
    data=((adc[1]&3)<<8) +adc[2]
    data_scale=(data*3.3)/float(1023)
    data_scale=round(data_scale,2)
    
    return data_scale


def set_matrix(number):

    number = str(number)

    with canvas(device) as draw:
        legacy.text(draw, (0,0), "Your string here", fill="white", 
        font=proportional(CP437_FONT) )
    
    return None


def get_keypad():
    oldKey = 18
    try:
        while True:
            button=1
            time.sleep(CHARACTER_DELAY)

            while button < 17:
                print_button=button
                if (print_button==17):
                        print_button=1

                GPIO.output(SCLPin,GPIO.LOW)
                time.sleep(HALF_BIT_TIME)
                keyval=GPIO.input(SDOPin)
                if not keyval:
                    pressed=True
                    if(oldKey!=button) :
                        set_matrix(print_button) #number between 1 -> 16
                        oldKey=button
                GPIO.output(SCLPin,GPIO.HIGH)
                time.sleep(HALF_BIT_TIME)

                button+=1

            pressed=False

    except KeyboardInterrupt:
        cleanup()
        pass


def cleanup():
    GPIO.cleanup()
    serialpi.close()
