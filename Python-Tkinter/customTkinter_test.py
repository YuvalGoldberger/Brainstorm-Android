import customtkinter
from customtkinter import *
from tkinter import *
import socket
import threading
import math

class GUI:

    # ----- Basic values -----
    SCREEN_WIDTH = 1270
    SCREEN_HEIGHT = 720
    FOLDER_LOCATION = r'D:\Yuval_Python\Yuval_Final_Proj\Projects-Github\Brainstorm-Android\Brainstorm-Android\Python-Tkinter\Fonts\static'
    IMAGE_FOLDER = r'D:\Yuval_Python\Yuval_Final_Proj\Projects-Github\Brainstorm-Android\Brainstorm-Android\Python-Tkinter\CTk_Images'
    MAX_CLIENTS = 5
    RED_FG = "#7d070f"
    GREEN_FG = "#077d0f"
    BLUE_FG = "#12bdc9"
    SERVER_STARTED = False
    SUBJECT = ''
    associations = []

    # ------------------------- INITIATE CLASS -------------------------

    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")

        self.server = socket.socket()
        self.server.bind(('0.0.0.0', 25565))
        self.server.listen(self.MAX_CLIENTS)

        self.screen = CTk()

        self.screen.title("Brainstorm by Yuval Goldberger")
        self.screen.geometry(f'{self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}')

        # ----- Set basic emojis for server up / down -----
        self.redCircle = PhotoImage(file=self.IMAGE_FOLDER+r"\redCircle.png")
        self.greenCircle = PhotoImage(file=self.IMAGE_FOLDER+r"\greenCircle.png")
        brain = PhotoImage(file=self.IMAGE_FOLDER+r"\brain.png")

        # ----- Main label (Welcome to brainstorm) -----
        mainLabel = CTkLabel(self.screen, text="!סיעור מוחות", text_font=("Assistant ExtraBold", 60))
        mainLabel.pack()

        # ----- Scrollbar to choose amount of partifipants -----
        options = []
        for i in range(30):
            options.append(f'{i+1} Participants')

        optionsLabel = CTkLabel(self.screen, text="בחר כמות משתתפים", text_font=("Assistant SemiBold", 25))
        optionsLabel.place(relx = 0.25, rely = 0.25, anchor=E)
        self.optionsParticipants = CTkOptionMenu(self.screen, values=options, text_color="#000000", fg_color="#c3ecf7", command=self.getParticipantsAmount)
        self.optionsParticipants.place(relx = 0.2, rely=0.3, anchor=E)
        # ----- Entry and label for subject -----
        addSubject = CTkLabel(self.screen, text="הכנס נושא בתיבת הטקסט", text_font=("Assistant Bold", 35))
        addSubject.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.subjectEntry = CTkEntry(self.screen, placeholder_text="..הכנס נושא", text_font=("Assistant Medium", 15), justify='right', width=550, height=100)
        self.subjectEntry.place(relx=0.5, rely = 0.43, anchor=CENTER)

        # ----- Button to show server's state -----
        self.serverUpButton = CTkButton(self.screen, image=self.redCircle, text_font=("Assistant Medium", 15), text=".השרת לא פעיל", hover=False, fg_color=self.RED_FG)
        self.serverUpButton.place(relx=0.01, rely = 0.98, anchor=SW)

        # ----- Button to start brainstorm (send subject and start server) -----

        sendSubjectButton = CTkButton(self.screen, text="התחל סיעור מוחות", image=brain, text_font=("Assistant Medium", 15), command= lambda: self.startServer())
        sendSubjectButton.place(relx = 0.5, rely = 0.55, anchor=CENTER)

        # ----- Mainloop -----
        threading.Thread(target=self.screen.mainloop(), daemon=True).start()


    # ------------------------- SERVER RELATED -------------------------

    # ----- Start the server thread -----
    def startServer(self):
        
        if self.SERVER_STARTED == False:
            startServer = threading.Thread(target= lambda: self.sendSubject(), daemon=True)
            self.SUBJECT = self.subjectEntry.get()
            self.changeWindow()
            startServer.start()
            self.SERVER_STARTED = True
        else:
            pass

    # ----- Send subject to client (application) -----
    def sendSubject(self):

        while True:
            try:
                newClient, newAddress = self.server.accept()
                print(newAddress, "connected")
                
                if self.SUBJECT == '' or self.SUBJECT is None:
                    self.SUBJECT = "No subject has been chosen."

                newClient.send(f'{self.SUBJECT}\n'.encode())
                recvd = newClient.recv(1024).decode()
                print(f'{newAddress} sent {recvd}')
                threading.Thread(self.clientHandler(client=newClient, address=newAddress), daemon=True).start()
            except:
                pass
    
    # ----- Get associations from clients -----
    def clientHandler(self, client, address):
        while True:
            try:
                data = client.recv(1024).decode()
                name = data.split(":breakHere:")[0]
                msg = data.split(":breakHere:")[1]
                print(f"{name} sent {msg}")
                self.associations.append((name, msg))
                print(f"added {name}, {msg} to associations. it is now {self.associations}")
                self.updateAssociations()
            except:
                pass

    # ------------------------- GUI RELATED -------------------------
    
    # ----- Change the window after server starts -----
    def changeWindow(self):
        # ----- Reset last window -----
        for widget in self.screen.winfo_children():
            widget.destroy()

        # ----- Create new window for new server -----
        subjectLabel = CTkLabel(self.screen, text=self.SUBJECT, text_font=("Assistant ExtraBold", 65))
        subjectLabel.pack()

        # ----- Server status -----
        self.serverUpButton = CTkButton(self.screen, image=self.greenCircle, text_font=("Assistant Medium", 15), text=".השרת פעיל", hover=False, fg_color=self.GREEN_FG)
        self.serverUpButton.place(relx=0.01, rely = 0.98, anchor=SW)

        # ----- Associations textbox -----
        self.associationsText = CTkTextbox(self.screen, font=("Assistant Medium", 20), text_color="#FFFFFF", state='disabled')

        # ----- Associations Canvas -----
        self.canvas = Canvas(self.screen, width=500, height=500, bg='#2c2c2c')
        def draw(angle, text):
            x = math.cos(math.radians(angle)) * 50 + 250
            y = math.sin(math.radians(angle)) * 50 + 250
            obj = self.canvas.create_text(250, 250, text=text, fill="green")
            self.canvas.itemconfig(obj, angle=-angle)
            self.canvas.coords(obj, x, y)
            return obj

        

        self.canvas.pack()

    # ----- Get selected Participants amount -----
    def getParticipantsAmount(self, choice):
        self.MAX_CLIENTS = choice.split(" ")[0]
        print(self.MAX_CLIENTS)
        self.optionsParticipants.set(choice)
        
    def updateAssociations(self): 
        # ----- Show the associations -----
        for a in self.associations:
            if a[1] not in self.associationsText.textbox.get('0.0', END):
                self.associationsText.configure(state='normal')
                self.associationsText.textbox.insert(END, a[1]+"\n")
                self.associationsText.configure(state='disabled')
                print(f"added {a[1]} to associationsTEXTBOX")
                
                def draw(angle, text):
                    x = math.cos(math.radians(angle)) * 50 + 250
                    y = math.sin(math.radians(angle)) * 50 + 250
                    obj = self.canvas.create_text(250, 250, text=text, fill="white", font=("Assistant Medium", 15))
                    self.canvas.itemconfig(obj, angle=-angle)
                    self.canvas.coords(obj, x, y)
                    return obj
                
                for i, word in zip(range(0,360,15), a[1]):
                    draw(i, word)
       
        self.associationsText.pack()
        self.screen.update()

    

if __name__ == '__main__':
    GUI()