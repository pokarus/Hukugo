#!/usr/bin/env python
#
# This is the code for Grove - Ultrasonic Ranger
# (https://www.seeedstudio.com/Grove-Ultrasonic-Ranger-p-960.html)
# which is a non-contact distance measurement module which works with 40KHz sound wave. 
#
# This is the library for Grove Base Hat which used to connect grove sensors for raspberry pi.
#

'''
## License

The MIT License (MIT)

Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
Copyright (C) 2018  Seeed Technology Co.,Ltd. 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
import sys
import time
from grove.gpio import GPIO
import RPi.GPIO as GPIORPi

usleep = lambda x: time.sleep(x / 1000000.0)

_TIMEOUT1 = 1000
_TIMEOUT2 = 10000

class GroveUltrasonicRanger(object):
    def __init__(self, pin):
        self.dio = GPIO(pin)

    def _get_distance(self):
        self.dio.dir(GPIO.OUT)
        self.dio.write(0)
        usleep(2)
        self.dio.write(1)
        usleep(10)
        self.dio.write(0)

        self.dio.dir(GPIO.IN)

        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT1:
            return None

        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT2:
            return None

        t2 = time.time()

        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            return None

        distance = ((t2 - t1) * 1000000 / 29 / 2)    # cm

        return distance

    def get_distance(self):
        while True:
            dist = self._get_distance()
            if dist:
                return dist


Grove = GroveUltrasonicRanger


def main():
    from grove.helper import SlotHelper
    LED = 13
    #GPIORPi.setup(LED, GPIORPi.OUT, initial=GPIORPi.LOW)
    GPIORPi.setup(LED, GPIORPi.OUT)
    
    PwmNumber1 = 5
    PwmNumber2 = 6
    Freq = 30
    Duty_Stop = 0
    Duty_Start = 1
    
    GPIORPi.setup(PwmNumber1, GPIORPi.OUT)
    GPIORPi.setup(PwmNumber2, GPIORPi.OUT)
    
    pwm1 = GPIORPi.PWM(PwmNumber1, Freq)
    pwm1.start(Duty_Stop)
    pwm2 = GPIORPi.PWM(PwmNumber2, Freq)
    pwm2.start(Duty_Stop)
    pwmLED = GPIORPi.PWM(LED, Freq)
    pwmLED.start(Duty_Stop)
    
    #led = GPIO(11, GPIO.OUT)
    
    
    sh = SlotHelper(SlotHelper.GPIO)
    pin = sh.argv2pin()

    sonar = GroveUltrasonicRanger(pin)

    print('Detecting distance...')
    while True:
        if sonar.get_distance() < 20:
            #pwm1.ChangeDutyCycle(100)
            #pwmLED.ChangeDutyCycle(90)
            pwm1.ChangeDutyCycle(Duty_Start)
            pwm2.ChangeDutyCycle(Duty_Stop)
            
            pwmLED.ChangeDutyCycle(0.01) #インジケーター

            time.sleep(0.01)
            #GPIORPi.output(LED, GPIORPi.HIGH)
            #print('{} cm'.format(sonar.get_distance()))
            
            #time.sleep(1)
        else:
            pwm1.ChangeDutyCycle(Duty_Stop)
            pwm2.ChangeDutyCycle(Duty_Stop)
            
            pwmLED.ChangeDutyCycle(80)
            #GPIORPi.output(LED, GPIORPi.LOW)
            #print('too far!')
            time.sleep(0.01)
            #time.sleep(1)

if __name__ == '__main__':
    main()

