#!/usr/bin/env python3

#import subprocess
import RPi.GPIO as GPIO

import local_commands.text_to_speech_commands as gtts

    #local commands - power
def destroy_GPIO():
    GPIO.output(26, GPIO.LOW)
    GPIO.cleanup()
    
def shutdown():
    print('shut down')
    gtts.speak('Turning Off')
    destroy_GPIO()
    #subprocess.call(['sudo', 'shutdown', '-h', 'now'])

def reboot():
    print('reboot')
    gtts.speak('Restarting')
    destroy_GPIO()
    #subprocess.call(['sudo', 'reboot', '-h', 'now'])


