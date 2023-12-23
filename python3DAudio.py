from tkinter import *
from tkinter import filedialog
import math
import pygame
import time

root = Tk()
root.title("3D Audio")
root.geometry("800x500")

pygame.mixer.init()


#User Settings
userGender = "male"
userHeight = 185
if userGender == "male":
    estimatedHeadCircumference = 42.4 + (0.08673 * userHeight)
else:
    estimatedHeadCircumference = 41.02 + (0.08673 * userHeight)
estimatedHeadDiameter = estimatedHeadCircumference/math.pi
itd = (estimatedHeadDiameter / 100) / 343                       #Interaural timing difference (ITD)


#Music Playback
filePath = ""
paused = False

def open_file():
    global filePath
    filePath = filedialog.askopenfilename()

def play_music():
    global paused, filePath
    if not paused:
        channel = pygame.mixer.find_channel()#Getting a Free Channel
        channel.set_volume(1.0, 0.0)#1.0 volume for left and 0.0 for right
        channel.play(pygame.mixer.Sound(filePath))
        time.sleep(0.006)
        channel2 = pygame.mixer.find_channel()
        channel2.set_volume(0.0, 1.0)
        channel2.play(pygame.mixer.Sound(filePath))
    else:
        pygame.mixer.unpause()
        paused = False

def pause_music():
    global paused
    pygame.mixer.pause()
    paused = True



#menus & buttons
menubar = Menu(root)
root.config(menu=menubar)    

file_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)

currentFile = Label(root, text = "yes")
currentFile.pack()

playButtonImg = PhotoImage(file="play.png")
pauseButtonImg = PhotoImage(file="pause.png")

control_frame = Frame(root)
control_frame.pack()
playButton = Button(control_frame, image=playButtonImg, borderwidth=0, command=play_music)
pauseButton = Button(control_frame, image=pauseButtonImg, borderwidth=0, command=pause_music)
playButton.grid(row=0, column=0, padx=7, pady=10)
pauseButton.grid(row=0, column=1, padx=7, pady=10)


root.mainloop()