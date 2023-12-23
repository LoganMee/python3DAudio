from tkinter import *
from tkinter import filedialog
import math
import pygame
import os

root = Tk()
root.title("3D Audio")
root.geometry("800x600")

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
fileName = ""
paused = False

channel = pygame.mixer.find_channel()
channel.set_volume(0.5, 0.5)
#channel2 = pygame.mixer.find_channel()
#channel2.set_volume(0.0, 0.5)


def open_file():
    global filePath, fileName
    filePath = filedialog.askopenfilename()
    fileName = os.path.basename(filePath)

def play_music():
    global paused, filePath, currentFile, fileName
    if not paused:
        channel.play(pygame.mixer.Sound(filePath))
        currentFile.config(text=f"Playing: {fileName}")
        #channel2.play(pygame.mixer.Sound(filePath))
    else:
        pygame.mixer.unpause()
        paused = False
        currentFile.config(text=f"Playing: {fileName}")

def pause_music():
    global paused, currentFile
    pygame.mixer.pause()
    paused = True
    currentFile.config(text="Paused")


#Audio Simulation Visualisation
radius = 25
canvasWidth = 500
canvasHeight = 500
canvasCentre = [canvasWidth/2, canvasHeight/2]

canvas = Canvas(root, width=canvasWidth, height=canvasHeight, bg="white")
canvas.pack()
head = canvas.create_oval(canvasCentre[0]-radius, canvasCentre[1]-radius, canvasCentre[0]+radius, canvasCentre[1]+radius, outline="black", fill="wheat", width=2)
audioSource = canvas.create_oval(canvasCentre[0]-radius/2, canvasCentre[1]-radius*2, canvasCentre[0]+radius/2, canvasCentre[1]-radius, outline="black", fill="Grey", width=2)
canvas.pack()

def distanceBetweenPoints(x1,y1,x2,y2):
    changeInX = x2 - x1
    changeInY = y2 - y1
    distance = math.sqrt(changeInX**2 + changeInY**2)
    return distance

def angleBetweenPoints(x1,y1,x2,y2, hypotenuse):
    changeInX = x2 - x1
    changeInY = y2 - y1
    angle = math.asin(changeInX/hypotenuse) # gets angle in radians
    return angle

def move(event):
    global audioSource, radius, canvasCentre, channel, channel2
    canvas.moveto(audioSource, event.x - radius/2, event.y - radius/2)

    distance = distanceBetweenPoints(canvasCentre[0], canvasCentre[1], event.x, event.y)
    distanceScaled = distance/25
    if distanceScaled > 1:
        intensityMultiplier = 1/(distanceScaled**2)
    else:
        intensityMultiplier = 1
    #print(intensityMultiplier)

    angle = angleBetweenPoints(canvasCentre[0], canvasCentre[1], event.x, event.y, distance)
    #print(angle)

    leftIntensity = ((math.sin(angle-math.pi)/2)+0.5) * intensityMultiplier
    rightIntensity = ((math.sin(angle)/2)+0.5) * intensityMultiplier
    print(leftIntensity)
    
    pygame.mixer.Channel(0).set_volume(leftIntensity, rightIntensity)
    #pygame.mixer.Channel(1).set_volume(0.0, rightIntensity)

canvas.bind('<B1-Motion>', move)


#menus & buttons
menubar = Menu(root)
root.config(menu=menubar)    

file_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)

currentFile = Label(root, text = "No song playing")
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