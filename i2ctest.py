#!/usr/bin/env python3

import smbus
import time
import math
from Sunfounder_PWM_Servo_Driver import PWM

def main():
    print("i2c test")
    pwm = PWM(address=0x40, debug=True)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()