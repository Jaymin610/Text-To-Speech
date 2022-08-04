import time

from gtts import gTTS
import os, shutil
import pyttsx3


def convert_to_speech_GTTS(is_preview, lang, desc, dir):
    myobj = gTTS(text=desc, lang=lang, slow=False)
    myobj.save("welcome.mp3")
    path = os.getcwd()

    src = path + "\\welcome.mp3"
    l = len(os.listdir(path + "\\user\\songdir\\" + dir)) + 1
    if is_preview:
        dest = path + "\\user\\songdir\\" + dir + "\\" + "preview.mp3"
        shutil.move(src, dest)
        return dir + "/preview.mp3"
    else:
        dest = path + "\\user\\songdir\\" + dir + "\\" + str(l) + ".mp3"
        shutil.move(src, dest)
        return dir + "/" + str(l) + ".mp3"


def convert_to_speech_PTTS(is_preview, gender, desc, dir, speech_rate):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    if (gender == 'male'):
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)

    engine.setProperty('rate', speech_rate)  # setting up new voice rate
    engine.setProperty('volume', 0.8)  # setting up volume level  between 0 and 1

    path = os.getcwd()
    l = len(os.listdir(path + "\\user\\songdir\\" + dir)) + 1

    if is_preview:
        save_dir = path + "\\user\\songdir\\" + dir + "\\preview.MP3"
        engine.save_to_file(desc, save_dir)
        engine.runAndWait()
        return dir + "/preview.mp3"
    else:
        engine.save_to_file(desc, path + "\\user\\songdir\\" + dir + "\\" + str(l) + ".mp3")
        engine.runAndWait()
        return dir + "/" + str(l) + ".mp3"
