from tkinter import *
from tkinter import filedialog
import math
import pygame
import os
import time

#User Settings
userGender = "male"
userHeight = 185
if userGender == "male":
    estimatedHeadCircumference = 42.4 + (0.08673 * userHeight)
else:
    estimatedHeadCircumference = 41.02 + (0.08673 * userHeight)
estimatedHeadDiameter = estimatedHeadCircumference/math.pi
itd = (estimatedHeadDiameter / 100) / 343   #Interaural timing difference (ITD)


#Window
root = Tk()
root.title("3D Audio")
root.geometry("800x600")

#Music Playback Variables
filePath = ""
fileName = ""
paused = False

pygame.mixer.init()
channel0 = pygame.mixer.Channel(0) #left1
channel0.set_volume(0.5, 0.0)
channel1 = pygame.mixer.Channel(1) #right1
channel1.set_volume(0.0, 0.5)

#################### Subroutines ####################
#Menu subroutines
def open_file():
    global filePath, fileName
    filePath = filedialog.askopenfilename()
    fileName = os.path.basename(filePath)

#Button subroutines
def play_music():
    global paused, filePath, playbackText, fileName
    if not paused:
        channel0.play(pygame.mixer.Sound(filePath))
        channel1.play(pygame.mixer.Sound(filePath))
        playbackText.config(text=f"Playing: {fileName}")
    else:
        pygame.mixer.unpause()
        paused = False
        playbackText.config(text=f"Playing: {fileName}")

def pause_music():
    global paused, playbackText
    pygame.mixer.pause()
    paused = True
    playbackText.config(text="Paused")

#Canvas subroutines
def distanceBetweenPoints(x1,y1,x2,y2):
    changeInX = x2 - x1
    changeInY = y2 - y1
    distance = math.sqrt(changeInX**2 + changeInY**2)
    return distance

def angleBetweenPoints(x1, x2, hypotenuse):
    changeInX = x2 - x1
    angle = math.asin(changeInX/hypotenuse) #Gets angle in radians
    return angle

def move(event):
    global audioSource, radius
    newX = event.x
    newY = event.y
    canvas.moveto(audioSource, newX - radius/2, newY - radius/2)
    volumeChange(newX, newY)

def volumeChange(newX, newY):
    global canvasCentre, channel0, channel1

    distance = distanceBetweenPoints(canvasCentre[0], canvasCentre[1], newX, newY)
    distanceScaled = distance/25
    if distanceScaled > 1:
        intensityMultiplier = 1/(distanceScaled**2)
    else:
        intensityMultiplier = 1

    angle = angleBetweenPoints(canvasCentre[0], newX, distance)

    leftIntensity = ((math.sin(angle-math.pi)/2)+0.5) * intensityMultiplier
    rightIntensity = ((math.sin(angle)/2)+0.5) * intensityMultiplier

    if leftIntensity < 0.01:
        leftIntensity = 0.01 #(minimum volume level)
    
    if rightIntensity < 0.01:
        rightIntensity = 0.01 #(minimum volume level)

    print(leftIntensity, rightIntensity)
    
    channel0.set_volume(leftIntensity, 0.0)
    channel1.set_volume(0.0, rightIntensity)

#################### GUI ####################
#Canvas for Audio Simulation Visualisation
radius = 25
canvasWidth = 500
canvasHeight = 500
canvasCentre = [canvasWidth/2, canvasHeight/2]

canvas = Canvas(root, width=canvasWidth, height=canvasHeight, bg="white")
head = canvas.create_oval(canvasCentre[0]-radius, canvasCentre[1]-radius, canvasCentre[0]+radius, canvasCentre[1]+radius, outline="black", fill="wheat", width=2)
audioSource = canvas.create_oval(canvasCentre[0]-radius/2, canvasCentre[1]-radius*2, canvasCentre[0]+radius/2, canvasCentre[1]-radius, outline="black", fill="Grey", width=2)
canvas.pack()

canvas.bind('<B1-Motion>', move)

#Menu
menubar = Menu(root)
root.config(menu=menubar)    

file_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)

playbackText = Label(root, text = "No song playing")
playbackText.pack()

#Buttons
playButtonImg = PhotoImage(file="play.png")
pauseButtonImg = PhotoImage(file="pause.png")

control_frame = Frame(root)
control_frame.pack()
playButton = Button(control_frame, image=playButtonImg, borderwidth=0, command=play_music)
pauseButton = Button(control_frame, image=pauseButtonImg, borderwidth=0, command=pause_music)
playButton.grid(row=0, column=0, padx=7, pady=10)
pauseButton.grid(row=0, column=1, padx=7, pady=10)

#Loop
root.mainloop()