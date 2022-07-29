import time

from gtts import gTTS
import os, shutil

def convert_to_speech(is_preview, lang, desc, dir):
    if lang == "English":
        language = 'en'
    elif lang == "Hindi":
        language = 'hi'

    myobj = gTTS(text=desc, lang=language, slow=False)
    myobj.save("welcome.mp3")
    path = os.getcwd()

    src = path+"\\welcome.mp3"
    l = len(os.listdir(path+"\\user\\songdir\\"+dir)) + 1
    if is_preview:
        dest = path + "\\user\\songdir\\" + dir + "\\" + "preview.mp3"
        shutil.move(src, dest)
        return dir + "/preview.mp3"
    else:
        dest = path+"\\user\\songdir\\"+dir+"\\"+str(l)+".mp3"
        shutil.move(src, dest)
        return dir+"/"+str(l)+".mp3"