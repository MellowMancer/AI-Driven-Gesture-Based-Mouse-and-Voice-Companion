from voice import Voice
from threading import *

def call_for_voice(terminate_queue):
    voice=Voice()
    r= voice.source()

    while True:
        print("Start Speaking")
        voice.listen(r)
        if not terminate_queue.empty():
            message = terminate_queue.get()
            if message == "terminate":
                break
        
# if __name__ == "__main__":
#     call_for_voice()