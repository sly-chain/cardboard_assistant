#local commands - led

import RPi.GPIO as GPIO

import aiy.assistant.auth_helpers
import aiy.cloudspeech
import aiy.voicehat
import aiy.audio
import aiy.assistant.grpc


def led_control():
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('turn on the light')
    recognizer.expect_phrase('turn off the light')
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(26, GPIO.OUT)
    GPIO.output(26, GPIO.HIGH)
    
    with aiy.audio.get_recorder():
        while True:
            text = recognizer.recognize()
            if text is not None:
                print('You said "', text, '"')
                if 'turn on the light' in text:
                    GPIO.output(26, GPIO.HIGH)
                elif 'turn off the light' in text:
                    GPIO.output(26, GPIO.LOW)
            else:
                print('Sorry, I did not hear you')