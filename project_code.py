import speech_recognition as sr
import pyttsx3
import pyautogui as pyg
import platform
import os
import subprocess
import time
import webbrowser as web
import pyjokes

def open_application(application):
    if os_type=="Windows":
        try:
            os.startfile(application)
        except:
            speaker.say("Sorry, I cannot find "+application+" on your computer.")
            # speaker.runAndWait()
            
    elif os_type=="Darwin":
        try:
            subprocess.Popen(["open", "-a", application])
        except:
            speaker.say("Sorry, I cannot find "+application+" on your computer.")
            # speaker.runAndWait()
    else:
        try:
            subprocess.Popen(["xdg-open", application])
        except:
            speaker.say("Sorry, I cannot find "+application+" on your computer.")
            # speaker.runAndWait()
        
def close_application(application):
    if os_type=="Windows":
        os.system("taskkill /f /im "+application+".exe")
    elif os_type=="Darwin":
        subprocess.Popen(["killall", application])
    else:
        subprocess.Popen(["killall", application])

def respond(lst, n):
    l1=lst[0].split(' ')
    #open application
    if 'open' in l1:
        id=l1.index('open')
        speaker.say("Opening "+l1[id+1])
        speaker.runAndWait()
        open_application(l1[id+1])
    
    #close application    
    elif 'close' in l1:
        id=l1.index('close')
        speaker.say("Closing "+l1[id+1])
        speaker.runAndWait()
        close_application(l1[id+1])
        
    #open website
    elif 'open' in l1 and "." in l1:
        id=l1.index('open')
        speaker.say("Opening "+l1[id+1])
        speaker.runAndWait()
        web.open_new_tab("https://"+l1[id+1], new=2, autoraise=True)
        
    #close website
    elif 'close tab' in l1:
        speaker.say("Closing tab")
        speaker.runAndWait()
        if os_type=="Windows" or os_type=="Linux":
            pyg.hotkey('ctrl', 'w')
        else:
            pyg.hotkey('command', 'w')
    
    #sarch on google
    elif 'search for' in l1:
        l2=l1.split('search_for')
        web.get().open("https://www.google.com/search?q="+l2[-1])
        speaker.say("Here is what I found for "+l2[-1])
        speaker.runAndWait()
        
    #play song on youtube
    
    # crack a joke
    elif 'joke' in l1:
        speaker.say(pyjokes.get_joke())
        speaker.runAndWait()
    
    #get location
        
    #quit
    elif ["exit", "quit", "goodbye"] in l1:
        speaker.speak("going to rest. Goodbye")
        exit()
        
    elif 'restart' in l1:
        speaker.say("Restarting your computer")
        speaker.runAndWait()
        os.system('shutdown /r /t 0')
        
    elif 'shutdown' in l1:
        speaker.say("Shutting down your computer")
        speaker.runAndWait()
        os.system('shutdown /s /t 0')

    else:
        speaker.say("Sorry, I didn't get that.")
        speaker.runAndWait()

def listen(r):
    # r=sr.recognizer()
    with sr.Microphone() as source:
        # r.adjust_for_ambient_noise(source)
        # print("Please say something")
        audio=r.listen(source)
        print(" Recognizing speech")
        
        text=""
        try:
            text=r.recognize_google(audio)
            # sr.recognize_sphinx(audio, language_model='en-us', keyword_entries=[("whisper", 1.0)])
        except:
            pass

        text=text.lower()
        print(text)
        
        if len(text)!=0 and 'grace' in text:
            lst=text.split('grace')
            print(lst)
            del lst[0]
            n=len(lst)
            i=0
            while i<n:
                lst[i]=lst[i].strip()
                if len(lst[i])==0:
                    del lst[i]
                    n-=1
                else:
                    i+=1
            print(lst)
            respond(lst, len(lst))                

os_type=platform.system()         
speaker=pyttsx3.init()
voices=speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)
speaker.setProperty('rate', 120)
# speaker.say("Hello, my name is Grace. I am your virtual assistant. I can help you with various things like playing a song, opening a website, opening an application, searching something on google, etc. You can ask me to do any of these things. Just invoke me by saying 'Grace' and I'll be at your service.")
speaker.say("I am Grace")
pyg.PAUSE=1

r=sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source) 
    speaker.say("You can start speaking.")
    speaker.runAndWait()

while True:
    print("Start Speaking")
    listen(r)