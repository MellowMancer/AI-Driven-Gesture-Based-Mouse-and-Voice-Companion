from voice import Voice
from threading import *

def call_for_voice():
    voice=Voice()
    r= voice.source()

    while True:
        print("Start Speaking")
        voice.listen(r)
        
# if __name__ == "__main__":
#     call_for_voice()