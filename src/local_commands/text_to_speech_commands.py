#!/usr/bin/env python3
import src.aiy.audio

from gtts import gTTS
 
def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    wav_file = tts.save('audio.wav')
    src.aiy.audio.play_wave(wav_file)


#speak('Hi, what can I do for you?')