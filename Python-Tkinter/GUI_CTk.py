import customtkinter
from customtkinter import *
from tkinter import *
from PIL import *
import socket
import threading
import glob
import pyglet
import time
import os

from labelDesign import TextDesign


class GUI:
    
    # ----- Get CurrentWorkingDirectory Path -----
    folderLocation = os.getcwd()

    # ----- Basic values -----
    SCREEN_WIDTH = 1270
    SCREEN_HEIGHT = 720
    FONT_FOLDER = folderLocation + r'\Fonts'
    IMAGE_FOLDER = folderLocation + r'\CTk_Images'
    RED_FG = "#7d070f"
    GREEN_FG = "#077d0f"
    BLUE_FG = "#12bdc9"
    

    # ----- Set fonts for Tkinter.Canvas (cannot use external fonts like customtkinter) -----
    fonts = glob.glob(f"{FONT_FOLDER}" + r"\random\*.ttf")
    for font in fonts:
        pyglet.font.add_file(font)
    # ------------------------- INITIATE CLASS -------------------------

    def __init__(self):
        '''
        ----- Sets defualt values, creates a screen and a server. -----
        '''
        # ----- Some defualt Values (that need to be restarted when restarting (calling __init__ again)) -----
        self.MAX_CLIENTS = 50
        self.SERVER_STARTED = False
        self.SUBJECT = ''
        self.associations = []
        self.SHOW_NAMES = False

        # ----- Set screen appearance + start server -----
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")

        self.server = socket.socket()
        self.server.bind(('0.0.0.0', 25565))
        self.server.listen(self.MAX_CLIENTS)

        self.screen = CTk()

        # ----- Set basic emojis for server up / down -----
        self.redCircle = CTkImage(light_image=Image.open(self.IMAGE_FOLDER+r"\redCircle.png"))
        self.greenCircle = CTkImage(light_image=Image.open(self.IMAGE_FOLDER+r"\greenCircle.png"))
        brain = CTkImage(light_image=Image.open(self.IMAGE_FOLDER+r"\brain.png"))

        self.screen.title("Brainstorm by Yuval Goldberger")
        self.screen.geometry(f'{self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}')

        # ----- Main label (Welcome to brainstorm) -----
        mainLabel = CTkLabel(self.screen, text="!סיעור מוחות", font=("Assistant ExtraBold", 60))
        mainLabel.pack()

        # ----- Scrollbar to choose amount of partifipants -----
        options = []
        options.append(f"{self.MAX_CLIENTS} Participants (Default)")
        for i in range(30):
            options.append(f'{i+1} Participants')

        optionsLabel = CTkLabel(self.screen, text="בחר כמות משתתפים", font=("Assistant SemiBold", 25))
        optionsLabel.place(relx = 0.25, rely = 0.25, anchor=E)
        self.optionsParticipants = CTkOptionMenu(self.screen, values=options, text_color="#000000", fg_color="#c3ecf7", command=self.getParticipantsAmount)
        self.optionsParticipants.place(relx = 0.2, rely=0.3, anchor=E)
        # ----- Entry and label for subject -----
        addSubject = CTkLabel(self.screen, text="הכנס נושא בתיבת הטקסט", font=("Assistant Bold", 35))
        addSubject.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.subjectEntry = CTkEntry(self.screen, placeholder_text="..הכנס נושא", font=("Assistant Medium", 15), justify='right', width=550, height=100)
        self.subjectEntry.place(relx=0.5, rely = 0.43, anchor=CENTER)

        # ----- Button to show server's state -----
        self.serverUpButton = CTkButton(self.screen, image=self.redCircle, font=("Assistant Medium", 15), text=".השרת לא פעיל", hover=False, fg_color=self.RED_FG)
        self.serverUpButton.place(relx=0.01, rely = 0.98, anchor=SW)

        # ----- Button to start brainstorm (send subject and start server) -----

        sendSubjectButton = CTkButton(self.screen, text="התחל סיעור מוחות", image=brain, font=("Assistant Medium", 15), command= self.startServer)
        sendSubjectButton.place(relx = 0.5, rely = 0.55, anchor=CENTER)

        # ----- Mainloop -----
        threading.Thread(target=self.screen.mainloop(), daemon=True).start()

    # ------------------------- SERVER RELATED -------------------------

    # ----- Start the server thread -----
    def startServer(self):
        '''
        ----- Starts the server thread -----
        '''
        if self.SERVER_STARTED == False:
            self.SUBJECT = self.subjectEntry.get()
            if len(self.SUBJECT) > 21:
                # ----- Set text limit -----
                topLevel = Toplevel(self.screen, bg='#000000')
                topLevel.geometry('300x100')
                tempLabel = CTkLabel(topLevel, text="הנושא צריך להיות פחות מ-20 תווים", font=("Assistant Medium", 20), text_color='#ffffff')
                tempLabel.pack()
                topLevel.update()
                self.screen.update()
                time.sleep(3)
                topLevel.destroy()
                return
            else:
                startServer = threading.Thread(target= lambda: self.sendSubject(), daemon=True)
                self.changeWindow()
                startServer.start()
                self.SERVER_STARTED = True
        else:
            pass

    # ----- Send subject to client (application) -----
    def sendSubject(self):
        '''
        ----- Handles multi-client connections and sends them the subject when they connect -----
        '''
        # ----- Starting amount of participants -----
        check = 0
        while True:
            try:
                newClient, newAddress = self.server.accept()
                print(newAddress, "connected")
                
                if self.SUBJECT == '' or self.SUBJECT is None:
                    self.SUBJECT = "No subject has been chosen."

                newClient.send(f'{self.SUBJECT}\n'.encode())
                recvd = newClient.recv(1024).decode()
                print(f'{newAddress} sent {recvd}')
                if check < self.MAX_CLIENTS:
                    threading.Thread(target=self.clientHandler, args=(newClient, newAddress), daemon=True).start()
                    print("will wait to a new client.")
            except:
                pass
    
    # ----- Get associations from clients -----
    def clientHandler(self, client, address):
        '''
        ----- Handles multi-client messages and appends it the the associations list ----- 
        '''
        while True:
            try:
                data = client.recv(1024).decode()
                name = data.split(":breakHere:")[0]
                msg = data.split(":breakHere:")[1]
                print(f"{name} sent {msg}")


                print("adding")
                self.associations.append((name, msg))
                print(f"added {name}, {msg} to associations. it is now {self.associations}")
                self.updateAssociations()
            except:
                pass

    # ------------------------- GUI RELATED -------------------------
    
    # ----- Change the window after server starts -----
    def changeWindow(self):
        '''
        ----- Destroys the first settings window and creates the Brainstorm window ----- 
        '''

        # ----- Set values for images needed for buttons -----
        stop = CTkImage(light_image=Image.open(self.IMAGE_FOLDER+r"\stop.png"))
        # ----- Reset last window -----
        for widget in self.screen.winfo_children():
            widget.destroy()

        # ----- Create new window for new server -----
        subjectLabel = CTkLabel(self.screen, text=self.SUBJECT, font=("Assistant ExtraBold", 65))
        subjectLabel.pack()

        # ----- Associations Canvas -----
        self.canvas = Canvas(self.screen, width=1270, height=720, bg='#2c2c2c')
        self.canvas.pack()

        # ----- Server status -----
        self.serverUpButton = CTkButton(self.screen, image=self.greenCircle, font=("Assistant Medium", 15), text=".השרת פעיל", hover=False, fg_color=self.GREEN_FG)
        self.serverUpButton.place(relx=0.01, rely = 0.98, anchor=SW)

        # ----- Close Brainstorm Button -----
        namesStateButton = CTkButton(self.screen, image=stop, font=("Assistant Medium", 15), text="הצג / הסתר שמות", command=self.nameStateChange)
        namesStateButton.place(relx=0.98, rely = 0.98, anchor=SE)

    # ----- Change Name State -----
    def nameStateChange(self):
        '''
        ----- NameStateButton command that changes the associations in the screen (shows the name / removes them) -----
        '''
        self.SHOW_NAMES = not self.SHOW_NAMES
        self.updateAssociations()

    # ----- Get selected Participants amount -----
    def getParticipantsAmount(self, choice):
        '''
        ----- Gets chosen participants amount and sets it to the server -----
        '''
        self.MAX_CLIENTS = choice.split(" ")[0]
        print(self.MAX_CLIENTS)
        self.optionsParticipants.set(choice)
        
    def updateAssociations(self): 
        '''
        ----- Resets associations and updates it to the newest form (happens when nameState changes or a new Association has been recieved) -----
        '''
        self.canvas.delete('all')
        # ----- Show the associations -----
        for a in self.associations:
            name = a[0]
            message = a[1]
            textDesign = TextDesign()
            fontName = textDesign.font.split(":")[0]
            fontStyle = textDesign.font.split(":")[1]

            if self.SHOW_NAMES:      
                text = self.canvas.create_text((textDesign.x, textDesign.y), text=f'{name}\n{message}', font=(fontName, textDesign.fontSize, fontStyle), fill=textDesign.color)            
            else:
                text = self.canvas.create_text((textDesign.x, textDesign.y), text=message, font=(fontName, textDesign.fontSize, fontStyle), fill=textDesign.color)
               
            self.canvas.itemconfig(text, angle=textDesign.angle)
            self.canvas.pack()
            self.screen.update()    

if __name__ == '__main__':
    GUI()