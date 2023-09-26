import speech_recognition as sr
import pyttsx3
import pyautogui as pyg
import pygetwindow as gw
import platform
import os
import subprocess
import psutil
import time
import datetime
import webbrowser as web
import pywhatkit as kit 
from translate import Translator
import wikipedia
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
    
def fetch_summary(search_query):
    try:
        summary = wikipedia.summary(search_query)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation pages by picking the first option
        summary = wikipedia.summary(e.options[0])
        return summary
    except wikipedia.exceptions.PageError:
        return "Page not found."

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
            web.open("https://www."+l1[id+1], new=2, autoraise=True)
            
        #open on yt
        elif 'youtube' in text:
            id1=l1.index('open')
            id2=l1.index('youtube')
            query=''
            if id1+1==id2 or id1+2==id2:
                comm=text.split('youtube')
                query=comm[1].strip()
            else:
                comm=text.split('open')
                comm=comm[1].split(' ')
                del comm[-1]
                if comm[-1]=='on':
                    del comm[-1]
                query=' '.join(comm)
            speaker.say("Opening on Youtube")
            speaker.runAndWait()
            url = f"https://www.youtube.com/results?search_query={query.strip()}"
            web.open(url)
            
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
                
        elif '.' in l1[1]:
            windows = gw.getWindowsWithTitle('')
            print(l1[1])
            url='https://www.'+l1[1]
            for window in windows:
                if l1[1] in window.title:
                    speaker.say("Closing"+l1[1])
                    speaker.runAndWait()
                    window.activate()
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
    
    #sarch on google, or weather
    elif 'search for' in text:
        # if 'search for' in text:
        query=text.split('search for')
        kit.search(query[1].strip())
        speaker.say("Here is what I found for "+query[1].strip())
        speaker.runAndWait()
        # elif 'weather' in text:
        #     kit.search('weather')
        #     speaker.say("Here is what I found for "+query[1].strip())
        #     speaker.runAndWait()
        # url = f"https://www.google.com/search?q={query[1].strip()}"
        # web.open(url)
        
    #search from wikipedia
    elif 'who' or 'what' or 'how' in l1:
        if 'who' in l1:
            id=l1.index('who')
        elif 'what' in l1:
            id=l1.index('what')
        query=' '.join(l1[id+2:])
        # print(query)
        summary = fetch_summary(query).split('.')
        # print(summary)
        # summ=[]
        for line in summary[:2]:
            print(line)
            if '\n' in line:
                line.replace('\n', '')
                # summ.append(line)
                speaker.say(line)
                speaker.runAndWait()    

    #play song on youtube
    elif 'play' in text:
        if 'song' in text:
            query=text.split('play song')
        else:
            query=text.split('play')
        # url = f"https://www.youtube.com/results?search_query={query[1].strip()}"
        # web.open(url)
        kit.playonyt(query[1].strip())
        speaker.say("Playing "+query[1].strip())
        speaker.runAndWait()
        
    #send whatsapp message
    elif 'send' in text and 'whatsapp' in text:
        try:
            query=text.split('send')
            query=query[1].split('whatsapp')
            query=query[0].split('to')
            # print(query)
            kit.sendwhatmsg_instantly(phone_no="+91"+query[1].strip(), message=query[0].strip())
            speaker.say("Message sent to "+query[1].strip())
            speaker.runAndWait()
        except:
            speaker.say("Sorry, I cannot send the message")
            speaker.runAndWait()
            
    #send email
    elif 'send' in text and 'email' in text:
        try:
            query=text.split('send')
            query=query[1].split('email')
            query=query[0].split('to')
            # print(query)
            kit.send_mail(query[1].strip(), query[0].strip(), "This is a test mail", "This is a test mail")
            
            speaker.say("Email sent to "+query[1].strip())
            speaker.runAndWait()
        except:
            speaker.say("Sorry, I cannot send the email")
            speaker.runAndWait()
            
    #translate 
    elif 'translate' in text:
        # curr=l1[l1.index('from')+1]
        target=l1[l1.index('to')+1]
        translator = Translator(from_lang='en', to_lang=target)
        speaker.say("What do you want to translate?")
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
        speaker.say("Here is the translation")
        speaker.runAndWait()    
        translation = translator.translate(text)
        speaker.say(translation)
        speaker.runAndWait()
        
    #operations on todo
    elif 'to do' in text:
        try:
            # f=open('todo.txt', 'a')
            a=['to to do list', 'to my to do list', 'to to do', 'to my to do', 'to do', 'from my to do list', 'from my to do', 'from to do list', 'from to do']
            for i in a:
                if i in text:
                    text=text.replace(i, '')
                    
            if 'add' in text:
                f=open('todo.txt', 'w')
                query=text.split('add')
                f.write(query[1].strip()+'\n')
                speaker.say("Added "+query[1].strip()+" to your to do list")
                speaker.runAndWait()
                
            elif 'read' in text:
                f=open('todo.txt', 'r')
                speaker.say("Here is your to do list")
                speaker.runAndWait()
                # f=open('todo.txt', 'r')
                lines=f.readlines()
                for line in lines:
                    if '\n' in line:
                        line.replace('\n', '')
                    speaker.say(lines)
                    speaker.runAndWait()
                    
            elif 'remove' or 'delete' in text:
                f=open('todo.txt', 'a+')
                speaker.say("Removing from your to do list")
                speaker.runAndWait()
                if 'remove' in text:
                    query=text.split('remove')
                elif 'delete' in text:
                    query=text.split('delete')
                    
                lines=f.readlines()
                data=[]
                for line in lines:
                    if line != query[1].strip()+'\n' or line != 'all':
                        data.append(line.strip())
                        
                f.seek(0)
                f.truncate()
                for line in data:
                    f.write(line+'\n')
            
            else:
                speaker.say("Sorry, I didn't get that")
                speaker.runAndWait()                
                            
            f.close()
            
        except:
            speaker.say("Sorry, I cannot find your to do list, Perhaps, you can create one!")
            speaker.runAndWait()
    
    #set a timer
    elif 'timer' in text:
        # command=text.split('')
        id=l1.index('seconds')
        set_timer(int(l1[id-1]))
        
    #take a screenshot
    elif 'screenshot' in l1 or 'capture' in l1:
        speaker.say("Taking screenshot")
        speaker.runAndWait()
        pyg.screenshot("screenshot.png")
        
    #left click, right click or double click
    elif 'click' in l1:
        if 'left' in l1:
            pyg.click()
        elif 'right' in l1:
            pyg.click(button='right')
        elif 'double' in l1:
            pyg.doubleClick()
        speaker.say("Clicked")
        speaker.runAndWait()
        
    # crack a joke
    elif 'joke' in l1:
        speaker.say(pyjokes.get_joke())
        speaker.runAndWait()
        
    #quit
    elif "exit" in l1 or 'quit' in l1 or 'bye' in l1 or 'goodbye' in l1:
        speaker.say("going to rest. Goodbye")
        speaker.runAndWait()
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
sec=0

r=sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source) 
    speaker.say("How can I help you?")
    speaker.runAndWait()

while True:
    print("Start Speaking")
    listen(r)