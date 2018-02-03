#!/usr/bin/env python3

import os
import sys
import tempfile
import shutil
#import wave

import aiy.assistant.grpc
import aiy.audio
import aiy.cloudspeech


sys.path.append(os.path.realpath(os.path.join(__file__, '..', '..')) + '/src/')
print(os.path)

class AudioAssistant():
    
    def __init__(self):
        self._wav_file = self._record_temp_wav()
        
    
    def _record_playback_basic(self):
        temp_file, temp_path = tempfile.mkstemp(suffix='.wav')
        os.close(temp_file)
    
        try:
            input("When you're ready, press enter and say 'Testing, 1 2 3'...")
            print('Recording...')
            aiy.audio.record_to_wave(temp_path, 5)
            print('Playing back recorded audio...')
            aiy.audio.play_wave(temp_path)
        finally:
            try:
                os.unlink(temp_path)
            except FileNotFoundError:
                pass
    
    
    def _record_save_wav(self):
        assistant = aiy.assistant.grpc.get_assistant()
        temp_file, temp_path = tempfile.mkstemp(suffix='.wav')
        os.close(temp_file)
        perm_path = os.path.expanduser('~/' + str(temp_file) + '.wav')

        try:
            aiy.audio.say('recording')
            print('Recording...')
            aiy.audio.record_to_wave(temp_path, 5)
            aiy.audio.play_wave(temp_path)
            
            aiy.audio.say('would you like to save the file?')
            text, audio = assistant.recognize()
            print(text)
            
            if text == 'yes':
                # move to perm_path
                shutil.move(temp_path, perm_path)
                aiy.audio.say('saved as' + str(temp_file))
        
        except:
            aiy.audio.say('something went wrong')
            print('Problems with recording')
            pass
            
        finally:
            try:
                os.unlink(temp_path)
            except FileNotFoundError:
                pass
    
            
    def _find_wav_file(self):
        assistant = aiy.assistant.grpc.get_assistant()
        
        # refer to file by temp_file integer referenced when saving file
        aiy.audio.say('what is the file name?')
        text, audio = assistant.recognize()
        
        file_queried = os.path.expanduser('~/' + text + '/.wav')
        
        try:
            if os.path.isfile(file_queried):
                return file_queried
            
        except FileNotFoundError:
            aiy.audio.say('file not found')
            print('file not found')
            pass
    
    
    def _play_wav_file(self):
        assistant = aiy.assistant.grpc.get_assistant()
        
        aiy.audio.say('what would you like to play?')
        text, audio = assistant.recognize()
        
        if self._find_wav_file():
            file_to_play = self._find_wav_file()
            aiy.audio.play_wave(file_to_play)
            
        else:
            aiy.audio.say('something went wrong')
            print('file not found')
            pass
    
#    def _delete_wav_file(self):
        


#def main():
    #AudioAssistant._create_wav_file()

#if __name__ == '__main__':
    #main()


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
#                     aiy.audio.say(text)
#                 else:
#                     print('I did not hear you')
#     
#     def delete_file(wave_file):
#         try:
#             print('deleting file ...')
#         except FileNotFoundError:
#             pass 
# =============================================================================
