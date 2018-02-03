import smtplib
import sys
print(sys.path)
import os

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
#from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

import aiy.audio
import aiy.voicehat
import aiy.assistant.grpc.get_assistant as assistant

import local_commands.text_to_speech_commands as gtts


user = ''
password = ''
can_start_conversation = False 


def send_files(recipient, files):
    assert type(recipient) == list
    assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = COMMASPACE.join(recipient)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'files from the cardboard'
    # msg.attach(MIMEText(body))

    for file in files:
        try:
            part = MIMEBase('application', "octet-stream")
            with open(file, 'rb') as fp:
                part.set_payload(fp.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            msg.attach(part)
        except:
            print('Unable to open one of the attachments. Error: ', sys.exc_info()[0])
            raise

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(user, password)
            s.sendmail(user, recipient, msg.as_string())
            s.close()
        print('Email sent!')
        gtts.speak('email sent')
        s.quit()
    except:
        print('Unable to send the email. Error: ', sys.exc_info()[0])
        gtts.speak('unable to send email')
        
        try_again(send_files)
    finally:
        recipient = []
        files = []


def set_recipients():
    gtts.speak('who should i send the email to?')
    print('Listening ...')
    recipient, audio = assistant.recognize()
    
    if recipient is not None:
        gtts.speak('You said ' + recipient)
        print('You said, "', recipient, '"')
        
        confirm_user_response('ok email will be sent to', recipient, set_recipients)
    else:
        print('i did not hear you')
        gtts.speak('i did not hear you')
        
        try_again(set_recipients)    



### confirmation prompts  ###
def try_again(function):
    status_ui = aiy.voicehat.get_status_ui()
    gtts.speak('would you like to try again?')
    text, audio = assistant.recognize()
    
    if text == 'yes':
        function()
    else: 
        gtts.speak('ok. aborting email service')
        status_ui.status('ready')
        can_start_conversation = True  


def confirm_user_response(phrase, response, function):
    gtts.speak('is this correct?')
    text, audio = assistant.recognize()
    
    if text == 'yes':
        gtts.speak(phrase)
        gtts.speak(response)
        return response
    elif text == 'no':
        try_again(function)

    
def confirm_information():
    status_ui = aiy.voicehat.get_status_ui()
    recipient = set_recipients()
    
    gtts.speak('let\'s confirm. you would like audio.wav sent to ' + recipient + '. is this correct?')
    
    text, audio = assistant.recognize()
    
    if text == 'yes':
        gtts.speak('ok sending email')
        send_files(recipient, ['audio.wav'])
    elif text == 'no':
        gtts.speak('ok. aborting email service')
        status_ui.status('ready')
        can_start_conversation = True  


# =============================================================================
#     def _set_files():
#         assistant = aiy.assistant.grpc.get_assistant()
#         
#         aiy.audio.say('what file should i send?')
#         print('Listening ...')
#         text, audio = assistant.recognize()
#         
#         if text is not None:
#             print('You said, "', text, '"')
#             aiy.audio.say('you said', text, 'is this correct?')
#             
#             confirm_user_response('ok email will be sent to', text, set_files)
#             
#             
#             file_name = text
#             return file_name
#         else:
#             print('i did not hear you')
#             aiy.audio.say('i did not hear you')
#             try_again(set_attachment)
# =============================================================================

