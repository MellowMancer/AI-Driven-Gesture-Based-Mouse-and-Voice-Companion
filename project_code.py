import speech_recognition as sr
import pyttsx3
import pyautogui as pyg
import platform
import os
import subprocess
import psutil
import time
import datetime
import webbrowser as web
import pyjokes


def open_application(application):
    if os_type=="Windows":
        try:
            # os.startfile(application)
            pyg.press('win')
            pyg.write(application)
            pyg.press('enter')
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
    # if os_type=="Windows":
    #     os.system("taskkill /f /im "+application+".exe")
    # elif os_type=="Darwin":
    #     subprocess.Popen(["killall", application])
    # else:
    #     subprocess.Popen(["killall", application])
        
    for proc in psutil.process_iter(['pid', 'name']):
        if application.lower() in proc.info['name'].lower():
            print(f"Terminating {proc.info['name']} (PID: {proc.info['pid']})")
            proc.terminate()
            return
        
def set_timer(seconds):
    start_time = time.time()
    end_time = start_time + seconds

    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        # print(f"Time remaining: {remaining_time} seconds", end='\r')
    
    speaker.say('Timer has completed!')
    speaker.runAndWait()


def respond(text):
    # print(f"Here is the list:{lst}")
    l1=text.split(' ')
    print(f"Here is the split list:{l1}")
    
    if 'open' in l1:
        #open a website
        if '.' in l1[l1.index('open')+1]:
            id=l1.index('open')
            speaker.say("Opening "+l1[id+1])
            speaker.runAndWait()
            web.open("https://"+l1[id+1], new=2, autoraise=True)
            
        #open an application
        else:
            id=l1.index('open')
            speaker.say("Opening "+l1[id+1])
            speaker.runAndWait()
            open_application(l1[id+1])
    
    # close application    
    elif 'close' in l1:
        if 'tab' in l1:
            speaker.say("Closing tab")
            speaker.runAndWait()
            if os_type=="Windows" or os_type=="Linux":
                pyg.hotkey('ctrl', 'w')
            else:
                pyg.hotkey('command', 'w')
                
        else:
            id=l1.index('close')
            speaker.say("Closing "+l1[id+1])
            speaker.runAndWait()
            close_application(l1[id+1])
            
    #day, date and time
    elif 'date' in l1 or 'day' in l1 or 'time' in l1:
        current = datetime.datetime.now()
        
        data={'day before yesterday': -2, 'yesterday': -1, 'today': 0, 'tomorrow': 1, 'day after tomorrow': 2}
        # day=0
        if 'date' in l1:
            months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            today = datetime.date.today()
            speaker.say('Todays date is'+str(today.day)+str(months[today.month-1])+","+str(today.year))
            speaker.runAndWait()
            
        if 'day' in l1:
            days={0: 'Monday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
            today = current.weekday()
            speaker.say('Today is a'+days[today])
            speaker.runAndWait()
            
        if 'time' in l1:
            formatted_time = current.strftime("%I:%M %p")
            speaker.say('It is')
            speaker.say(formatted_time)
            speaker.runAndWait()
    
    #sarch on google
    elif 'search' in l1:
        if l1[l1.index('search') + 1] == 'for':
            print(l1)
            l2 = l1[0].replace('search for', "")
            l2 = l2.replace(" ", "+")
            web.get().open("https://www.google.com/search?q="+l2)
            speaker.say("Here is what I found for "+l2)
            speaker.runAndWait()
        
    #play song on youtube
    
    # crack a joke
    elif 'joke' in l1:
        speaker.say(pyjokes.get_joke())
        speaker.runAndWait()
    
    #get location
        
    #quit
    elif ("exit" or "quit" or "goodbye") in l1:
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
        
        if len(text)!=0 and 'ash' in text:
            lst=text.split('ash')
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
            respond(lst[0])                

os_type=platform.system()         
speaker=pyttsx3.init()
voices=speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)
speaker.setProperty('rate', 120)
# speaker.say("Hello, my name is Ashlyn. I am your virtual assistant. I can help you with various things like playing a song, opening a website, opening an application, searching something on google, etc. You can ask me to do any of these things. Just invoke me by saying 'Ash' and I'll be at your service.")
speaker.say("I am Ash")
pyg.PAUSE=1

r=sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source) 
    speaker.say("How can I help you?")
    speaker.runAndWait()

while True:
    print("Start Speaking")
    listen(r)