import tkinter 
import cv2
import PIL.Image, PIL.ImageTk 
from functools import partial
import threading
import time
import imutils 
import os

# Get the absolute path to the Images directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "Images")

# Video choices
video_choices = {
    "Default Video": "video.mp4",
    "Alternative 1": "alternative1.mp4",
    "Alternative 2": "alternative2.mp4"
}

# Initialize stream as None
stream = None
flag = True

def load_video(video_filename):
    global stream
    if stream:
        stream.release()
    video_path = os.path.join(IMAGES_DIR, video_filename)
    stream = cv2.VideoCapture(video_path)

def play(speed):
    global flag
    if not stream:
        return
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        return
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(134, 26, fill="black", font="Times 26 bold", text="Decision Pending")
    flag = not flag
    

def pending(decision):
    decision_pending_path = os.path.join(IMAGES_DIR, "Decision Pending.png")
    frame = cv2.cvtColor(cv2.imread(decision_pending_path), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    time.sleep(1.5)

    # Skip displaying codeplay.png, go directly to out/not out
    if decision == 'out':
        decisionImg = os.path.join(IMAGES_DIR, "OUT.png")
    else:
        decisionImg = os.path.join(IMAGES_DIR, "NOT OUT.png")
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)


def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    

def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    

def change_video(selection):
    selected_file = video_choices[selection]
    load_video(selected_file)


# Width and height of our main screen
SET_WIDTH = 650
SET_HEIGHT = 368

# Tkinter gui starts here
window = tkinter.Tk()
window.title("Third Umpire Decision Review Kit")

# Load initial image
drs_image_path = os.path.join(IMAGES_DIR, "Drs.png")
cv_img = cv2.cvtColor(cv2.imread(drs_image_path), cv2.COLOR_BGR2RGB)
cv_img = imutils.resize(cv_img, width=SET_WIDTH, height=SET_HEIGHT)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
canvas.pack()

# Dropdown to select video
video_var = tkinter.StringVar(window)
video_var.set("Default Video")  # Default choice
dropdown = tkinter.OptionMenu(window, video_var, *video_choices.keys(), command=change_video)
dropdown.pack()

# Load default video
load_video(video_choices["Default Video"])

# Buttons to control playback
tkinter.Button(window, text="<< Previous (fast)", width=50, command=partial(play, -25)).pack()
tkinter.Button(window, text="<< Previous (slow)", width=50, command=partial(play, -2)).pack()
tkinter.Button(window, text="Next (slow) >>", width=50, command=partial(play, 2)).pack()
tkinter.Button(window, text="Next (fast) >>", width=50, command=partial(play, 25)).pack()
tkinter.Button(window, text="Give Out", width=50, command=out).pack()
tkinter.Button(window, text="Give Not Out", width=50, command=not_out).pack()

window.mainloop()
