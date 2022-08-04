import pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
gender = 'male'
if gender == 'male':
    engine.setProperty('voice', voices[0].id)
else:
    engine.setProperty('voice', voices[1].id)

engine.setProperty('rate', 100)  # setting up new voice rate
engine.setProperty('volume', 0.8)  # setting up volume level  betw
engine.say("Hello")
engine.save_to_file("Hello", "jaymin.mp3")
engine.runAndWait()
