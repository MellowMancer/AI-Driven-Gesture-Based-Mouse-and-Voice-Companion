import speech_recognition as sr
import pyttsx3
import pyautogui as pyg
import platform
import os
import subprocess
import psutil
import time
import webbrowser as web
import pyjokes

class Voice:
    def __init__(self):
        self.os_type=platform.system()         
        self.speaker=pyttsx3.init()
        self.voices=self.speaker.getProperty('voices')
        self.speaker.setProperty('voice', self.voices[1].id)
        self.speaker.setProperty('rate', 120)
        self.speaker.say("Hello, my name is Ashlyn. I am your virtual assistant. I can help you with various things like playing a song, opening a website, opening an application, searching something on google, etc. You can ask me to do any of these things. Just invoke me by saying 'Ash' and I'll be at your service.")
        # self.speaker.say("I am Ash")
        pyg.PAUSE=1

    def source(self):
        r=sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source) 
            self.speaker.say("How can I help you?")
            self.speaker.runAndWait()
        return r
    
    def open_application(self, application):
        if self.os_type=="Windows":
            try:
                # os.startfile(application)
                pyg.press('win')
                pyg.write(application)
                pyg.press('enter')
            except:
                self.speaker.say("Sorry, I cannot find "+application+" on your computer.")
                # speaker.runAndWait()
                
        elif self.os_type=="Darwin":
            try:
                subprocess.Popen(["open", "-a", application])
            except:
                self.speaker.say("Sorry, I cannot find "+application+" on your computer.")
                # speaker.runAndWait()
        else:
            try:
                subprocess.Popen(["xdg-open", application])
            except:
                self.speaker.say("Sorry, I cannot find "+application+" on your computer.")
                # speaker.runAndWait()
        
    def close_application(self, application):
        # if self.os_type=="Windows":
        #     os.system("taskkill /f /im "+application+".exe")
        # elif self.os_type=="Darwin":
        #     subprocess.Popen(["killall", application])
        # else:
        #     subprocess.Popen(["killall", application])
        for proc in psutil.process_iter(['pid', 'name']):
            if application.lower() in proc.info['name'].lower():
                # print(f"Terminating {proc.info['name']} (PID: {proc.info['pid']})")
                proc.terminate()
                # return
        
    def listen(self, r):
        with sr.Microphone() as source:
            audio=r.listen(source)
            print(" Recognizing speech")
            
            text=""
            try:
                text=r.recognize_google(audio)
            except:
                pass

            text=text.lower()
            print(text)
            
            if len(text)!=0 and 'ash' in text:
                lst=text.split('ash')
                # print(lst)
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
                # print(lst)
                self.respond(lst[0])    
                
    def respond(self, text):
        l1=text.split(' ')
        print(f"Here is the split list:{l1}")
        
        #open application
        if 'open' in l1:
            id=l1.index('open')
            self.speaker.say("Opening "+l1[id+1])
            self.speaker.runAndWait()
            self.open_application(l1[id+1])
        
        # close application    
        elif 'stop' in l1:
            id=l1.index('stop')
            self.speaker.say("Closing "+l1[id+1])
            self.speaker.runAndWait()
            self.close_application(l1[id+1])
            
        #open website
        elif 'open' in l1 and "." in l1:
            id=l1.index('open')
            self.speaker.say("Opening "+l1[id+1])
            self.speaker.runAndWait()
            web.open_new_tab("https://"+l1[id+1], new=2, autoraise=True)
            
        #close website
        elif ('close' and 'tab') in l1:
            self.speaker.say("Closing tab")
            self.speaker.runAndWait()
            if self.os_type=="Windows" or self.os_type=="Linux":
                pyg.hotkey('ctrl', 'w')
            else:
                pyg.hotkey('command', 'w')
        
        #sarch on google
        elif 'search' in l1:
            if l1[l1.index('search') + 1] == 'for':
                l2 = lst[0].replace('search for', "")
                l2 = l2.replace(" ", "+")
                web.get().open("https://www.google.com/search?q="+l2)
                self.speaker.say("Here is what I found for "+l2)
                self.speaker.runAndWait()
            
        #play song on youtube
        
        # crack a joke
        elif 'joke' in l1:
            self.speaker.say(pyjokes.get_joke())
            self.speaker.runAndWait()
        
        #quit
        elif ("exit" or "quit" or "goodbye") in l1:
            self.speaker.speak("going to rest. Goodbye")
            exit()
            
        elif 'restart' in l1:
            self.speaker.say("Restarting your computer")
            self.speaker.runAndWait()
            os.system('shutdown /r /t 0')
            
        elif 'shutdown' in l1:
            self.speaker.say("Shutting down your computer")
            self.speaker.runAndWait()
            os.system('shutdown /s /t 0')

        else:
            self.speaker.say("Sorry, I didn't get that.")
            self.speaker.runAndWait()
            