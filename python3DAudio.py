from tkinter import *
from tkinter import filedialog
import pygame, math, os, time, threading

#User Settings
userGender = "male"
userHeight = 185
if userGender == "male":
    estimatedHeadCircumference = 42.4 + (0.08673 * userHeight)
else:
    estimatedHeadCircumference = 41.02 + (0.08673 * userHeight)
estimatedHeadDiameter = estimatedHeadCircumference/math.pi
itd = (estimatedHeadDiameter / 100) / 343   #Interaural timing difference (ITD)

#mathmatical Functions
def distanceBetweenPoints(x1,y1,x2,y2):
    changeInX = x2 - x1
    changeInY = y2 - y1
    distance = math.sqrt(changeInX**2 + changeInY**2)
    return distance

def angleBetweenPoints(x1, x2, hypotenuse):
    changeInX = x2 - x1
    angle = math.asin(changeInX/hypotenuse) #Gets angle in radians
    return angle



class Audio3DInterface:

    def __init__(self):
        self.root = Tk()
        self.root.title("3D Audio")
        self.root.geometry("800x700")
        
        self.mainFrame = Frame(self.root)
        self.mainFrame.grid(column=0, row=0, padx=10, pady=10)
        self.controlsFrame = Frame(self.root)
        self.controlsFrame.grid(column=0, row=1, padx=10, pady=10)

        self.filePath = ""
        self.fileName = ""
        self.playing = False
        self.paused = False

        pygame.mixer.init()
        self.channel0 = pygame.mixer.Channel(0) #left1
        self.channel0.set_volume(0.5, 0.0)
        self.channel1 = pygame.mixer.Channel(1) #right1
        self.channel1.set_volume(0.0, 0.5)

        self.playButtonImg = PhotoImage(file="play.png")
        self.pauseButtonImg = PhotoImage(file="pause.png")

        self.orbit = False
    
    #################### Subroutines ####################
    def run(self):
        self.createWidgets()
        self.root.mainloop()
    
    #Menu subroutines
    def openFile(self):
        self.filePath = filedialog.askopenfilename()
        self.fileName = os.path.basename(self.filePath)

    #Button subroutines
    def playMusic(self, playbackText):
        if not self.paused and self.playing == False:
            self.channel0.play(pygame.mixer.Sound(self.filePath))
            self.channel1.play(pygame.mixer.Sound(self.filePath))
            playbackText.config(text=f"Playing: {self.fileName}")
            self.playing = True
        else:
            pygame.mixer.unpause()
            self.paused = False
            playbackText.config(text=f"Playing: {self.fileName}")

    def pauseMusic(self, playbackText):
        pygame.mixer.pause()
        self.paused = True
        playbackText.config(text="Paused")
 
    #Canvas subroutines
    def move(self, event, audioSource, radius, canvas, canvasCentre):
        newX = event.x
        newY = event.y
        canvas.moveto(audioSource, newX - radius/2, newY - radius/2)
        self.volumeChange(newX, newY, canvasCentre)

    def orbitAudio(self, audioSource, radius, canvas, canvasCentre, orbitRadius):
        self.orbit = True
        canvas.moveto(audioSource, canvasCentre[0], canvasCentre[1] + orbitRadius)
        angle = 0
        while self.orbit == True and self.paused == False:
            angle += (1/72*math.pi)
            newX = canvasCentre[0] + (math.sin(angle) * orbitRadius)
            newY = canvasCentre[1] + (math.cos(angle) * orbitRadius)

            canvas.moveto(audioSource, newX - radius/2, newY - radius/2)
            self.volumeChange(newX, newY, canvasCentre)

            time.sleep(5/144)

    def volumeChange(self, newX, newY, canvasCentre):
        distance = distanceBetweenPoints(canvasCentre[0], canvasCentre[1], newX, newY)
        distanceScaled = distance/25
        if distanceScaled > 1:
            intensityMultiplier = 1/(distanceScaled**2)
        else:
            intensityMultiplier = 1

        angle = angleBetweenPoints(canvasCentre[0], newX, distance)

        leftIntensity = ((((math.sin(angle-math.pi)/2)+0.5)/(3/2))+(1/3)) * intensityMultiplier #minimum audio level of 1/3
        rightIntensity = ((((math.sin(angle)/2)+0.5)/(3/2))+(1/3)) * intensityMultiplier

        print(leftIntensity, rightIntensity)
        
        self.channel0.set_volume(leftIntensity, 0.0)
        self.channel1.set_volume(0.0, rightIntensity)

    def createWidgets(self):
        #################### GUI ####################
        #Canvas for Audio Simulation Visualisation
        radius = 25
        canvasWidth = 500
        canvasHeight = 500
        canvasCentre = [canvasWidth/2, canvasHeight/2]

        canvas = Canvas(self.mainFrame, width=canvasWidth, height=canvasHeight, bg="white")
        head = canvas.create_oval(canvasCentre[0]-radius, canvasCentre[1]-radius, canvasCentre[0]+radius, canvasCentre[1]+radius, outline="black", fill="wheat", width=2)
        audioSource = canvas.create_oval(canvasCentre[0]-radius/2, canvasCentre[1]-radius*2, canvasCentre[0]+radius/2, canvasCentre[1]-radius, outline="black", fill="Grey", width=2)
        canvas.grid(column=0, row=0)

        canvas.bind('<B1-Motion>', lambda event:self.move(event, audioSource, radius, canvas, canvasCentre))

        #Menu
        menubar = Menu(self.root)
        self.root.config(menu=menubar)    

        fileMenu = Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Open", command=self.openFile)

        #Info Bar
        playbackText = Label(self.controlsFrame, text = "No song playing")
        playbackText.grid(column=0, row=0, columnspan=2)

        #Buttons
        playButton = Button(self.controlsFrame, image=self.playButtonImg, borderwidth=0, command=lambda:self.playMusic(playbackText))
        pauseButton = Button(self.controlsFrame, image=self.pauseButtonImg, borderwidth=0, command=lambda:self.pauseMusic(playbackText))
        playButton.grid(row=1, column=0, padx=7, pady=10)
        pauseButton.grid(row=1, column=1, padx=7, pady=10)

        #orbit
        orbitButton = Button(self.controlsFrame, text="Orbit", command=lambda:threading.Thread(target=self.orbitAudio, args=(audioSource, radius, canvas, canvasCentre, 100)).start())
        orbitButton.grid(row=2, column=0, padx=7, pady=10)



def main():
    audioSys1 = Audio3DInterface()
    audioSys1.run()

main()