import tkinter as tk
from threading import Thread
from voice_main import call_for_voice
from hand_main import call_for_gesture
from tkinter import ttk
import multiprocessing


def start_hand_detection():
    pool.apply_async(call_for_gesture)  # Run function1 asynchronously

def start_speech_detection():
    pool.apply_async(call_for_voice)  # Run function2 asynchronously

def open_user_manual():
    #to open manual
    pass


def change_button_color(event):
    event.widget.configure(style="TButton.Clicked")


if __name__ == '__main__':

    root = tk.Tk()
    root.title("Hand and Speech Detection")

    root.configure(bg="#F4E869")


    style = ttk.Style()
    style.configure("TButton", borderwidth=0, relief="flat", background="red", padding=(20, 20))
    style.map("TButton", background=[("active", "green")])

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    top_margin = int(0.3 * screen_height)

    header_label = tk.Label(root, text="Hand and Speech Detection App", font=("Arial", 16, "bold"), bg="#F4E869")
    user_manual_button = ttk.Button(root, text="User Manual", command=open_user_manual, style="TButton")


    header_label.place(relx=0.5, rely=0.05, anchor="center")
    user_manual_button.place(relx=0.95, rely=0.03, anchor="ne")


    hand_button = ttk.Button(root, text="Start Hand Detection", command=start_hand_detection, style="TButton")
    speech_button = ttk.Button(root, text="Start Speech Detection", command=start_speech_detection, style="TButton")

    hand_button.place(relx=0.5, rely=0.35, anchor="center")
    speech_button.place(relx=0.5, rely=0.45, anchor="center")


    root.geometry(f"{screen_width}x{screen_height}+0+0")

    pool = multiprocessing.Pool(processes=2)  # Create a pool with 2 worker processes
    # pool.close()  # Close the pool, preventing any more tasks from being submitted
    # pool.join()  # Wait for all the tasks to complete
    root.mainloop()










    # from voice_main import call_for_voice
    # from threading import *
    # from hand_main import call_for_gesture
    # from multiprocess import Process

    # t1=Thread(target=call_for_voice)
    # t1=Process(target=call_for_voice)
    # t2=Thread(target=call_for_gesture)

    # t2=Process(target=call_for_gesture)
    # t1.start()
    # print('T1 started')
    # t2.start()
    # print('T2 started')

    # t1.join()
    # print('T1 ended')
    # t2.join()
    # print('T2 ended')
