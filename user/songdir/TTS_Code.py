import time

from gtts import gTTS
import os, shutil

def convert_to_speech(lang, desc, dir):
    if lang == "English":
        language = 'en'

    myobj = gTTS(text=desc, lang=language, slow=False)
    myobj.save("welcome.mp3")
    path = os.getcwd()

    if not os.path.exists(path+"\\user\\songdir\\"+dir):
        os.makedirs(path+"\\user\\songdir\\"+dir)

    src = path+"\\welcome.mp3"
    l = len(os.listdir(path+"\\user\\songdir\\"+dir)) + 1
    dest = path+"\\user\\songdir\\"+dir+"\\"+str(l)+".mp3"

    shutil.move(src, dest)

    return dir+"\\"+str(l)+".mp3"