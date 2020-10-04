#!/usr/bin/python
from Sunfounder_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
#pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
	pulseLength = 1000000                   # 1,000,000 us per second
	pulseLength /= 5                       # 50 Hz
	print ("%d us per period" % pulseLength)
	pulseLength /= 4096                     # 12 bits of resolution
	print ("%d us per bit" % pulseLength)
	pulse *= 1000
	pulse /= pulseLength
	pwm.setPWM(channel, 0, int(pulse))

def setServo(position):
    servoMin = 105
    servoMax = 525
    servoRange = servoMax-servoMin
    servoValue = ((position/180)*servoRange) + servoMin
    pwm.setPWM(0, 0, int(servoValue))

pwm.setPWMFreq(49)                        # Set frequency to 60 Hz
# pwm.setPWM(0,0,525)

while (True):
    setServo(0)
    time.sleep(1)
    setServo(180)
    time.sleep(1)
