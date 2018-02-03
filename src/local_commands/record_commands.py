#!/usr/bin/env python3

import os
import sys
import tempfile
import shutil
#import wave

import src.aiy.assistant.grpc
import src.aiy.audio
import src.aiy.cloudspeech

import local_commands.text_to_speech_commands as gtts

sys.path.append(os.path.realpath(os.path.join(__file__, '..', '..')) + '/src/')
print(os.path)

        
    
def record_playback_simple():
    temp_file, temp_path = tempfile.mkstemp(suffix='.wav')
    os.close(temp_file)

    try:
        input("When you're ready, press enter and say 'Testing, 1 2 3'...")
        print('Recording...')
        gtts.speak('recording')
        src.aiy.audio.record_to_wave(temp_path, 5)
        src.aiy.audio.play_wave(temp_path)
    finally:
        try:
            os.unlink(temp_path)
        except FileNotFoundError:
            pass


def record_save_wav():
    assistant = src.aiy.assistant.grpc.get_assistant()
    temp_file, temp_path = tempfile.mkstemp(suffix='.wav')
    os.close(temp_file)
    perm_path = os.path.expanduser('~/' + str(temp_file) + '.wav')

    try:
        gtts.speak('recording')
        print('Recording...')
        src.aiy.audio.record_to_wave(temp_path, 5)
        src.aiy.audio.play_wave(temp_path)
        
        gtts.speak('would you like to save the file?')
        text, audio = assistant.recognize()
        print(text)
        
        if text == 'yes':
            # move to perm_path
            shutil.move(temp_path, perm_path)
            gtts.speak('saved as ' + str(temp_file))
        if text == 'no':
            gtts.speak('ok file was not saved')
    
    except:
        gtts.speak('i did not get that')
        print('Problems with recording')
        pass
        
    finally:
        try:
            os.unlink(temp_path)
        except FileNotFoundError:
            pass

        
def find_wav_file():
    assistant = src.aiy.assistant.grpc.get_assistant()
    
    # refer to file by temp_file integer referenced when saving file
    text, audio = assistant.recognize()
    file_queried = os.path.expanduser('~/' + text + '/.wav')
    
    try:
        if os.path.isfile(file_queried):
            return file_queried
        
    except FileNotFoundError:
        gtts.speak("file wasn't found")
        print('file not found')
        pass


def play_wav_file():
    gtts.speak("what file do you want to play?")
    wav_file = find_wav_file()
    
    if wav_file:
        src.aiy.audio.play_wave(wav_file)
        
    else:
        gtts.speak("i can't find the file")
        print('file not found')
        pass


def _delete_wav_file():
    gtts.speak("what file would you like to delete?")
    wav_file = find_wav_file()
    
    if wav_file:
        gtts.speak('i have deleted ' + wav_file)
        os.remove(wav_file)
        
    else:
        gtts.speak("i can't find the file")
        print('file not found')
        pass
        



    #local commands - repeat
    #built in already. don't need it. 
# =============================================================================
#     def repeat_after_me():
#         assistant = aiy.assistant.grpc.get_assistant()
#         with aiy.audio.get_recorder():
#             while True:
#                 print('Listening ...')
#                 text, audio = assistant.recognize()
#                 if text is not None:
#                     print('You said, "', text, '"')
#                     gtts.speak(text)
#                 else:
#                     print('I did not hear you')
#     
#     def delete_file(wave_file):
#         try:
#             print('deleting file ...')
#         except FileNotFoundError:
#             pass 
# =============================================================================
