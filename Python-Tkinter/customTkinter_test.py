import customtkinter
from customtkinter import *
from tkinter import *
import socket
import threading

class GUI:

    SCREEN_WIDTH = 1270
    SCREEN_HEIGHT = 720
    FOLDER_LOCATION = r'D:\Yuval_Python\Yuval_Final_Proj\Projects-Github\Brainstorm-Android\Brainstorm-Android\Python-Tkinter\Fonts'
    IMAGE_FOLDER = r'D:\Yuval_Python\Yuval_Final_Proj\Projects-Github\Brainstorm-Android\Brainstorm-Android\Python-Tkinter\CTk_Images'
    MAX_CLIENTS = 5
    RED_FG = "#7d070f"
    GREEN_FG = "#077d0f"
    BLUE_FG = "#12bdc9"
    SERVER_STARTED = False

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
        mainLabel = CTkLabel(self.screen, text="Welcome to Brainstorm!", text_font=("Assistant ExtraBold", 60))
        mainLabel.pack()

        # ----- Entry and label for subject -----
        addSubject = CTkLabel(self.screen, text="Enter your subject", text_font=("Assistant Bold", 35))
        addSubject.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.subjectEntry = CTkEntry(self.screen, placeholder_text="Enter your subject here...", text_font=("Assistant Medium", 15), width=550, height=100)
        self.subjectEntry.place(relx=0.5, rely = 0.43, anchor=CENTER)

        # ----- Button to show server's state -----
        self.serverUpButton = CTkButton(self.screen, image=self.redCircle, text_font=("Assistant Medium", 15), text="Server is down.", hover=False, fg_color=self.RED_FG)
        self.serverUpButton.place(relx=0.285, rely = 0.55)

        # ----- Button to start brainstorm (send subject and start server) -----

        sendSubjectButton = CTkButton(self.screen, image=brain, text="Send Subject", text_font=("Assistant Regular", 15), command= lambda: self.startServer())
        sendSubjectButton.place(relx = 0.573, rely = 0.55)

        # ----- Mainloop -----
        threading.Thread(target=self.screen.mainloop()).start()

    def startServer(self):
        
        if self.SERVER_STARTED == False:
            startServer = threading.Thread(target= lambda: self.sendSubject())
            startServer.setDaemon = True
            startServer.start()
            self.SERVER_STARTED = True
        else:
            pass

    def sendSubject(self):
        self.serverUpButton.configure(image=self.greenCircle, text="Server is up.", fg_color= self.GREEN_FG, state="disabled")
        self.subjectEntry.configure(state="disabled")
        while True:
            try:
                newClient, newAddress = self.server.accept()
                print(newAddress, "connected")
                subject = self.subjectEntry.get()
                if subject == '' or subject is None:
                    subject = "No subject has been chosen."

                newClient.send(f'{subject}\n'.encode())
                recvd = newClient.recv(1024).decode()
                print(f'{newAddress} sent {recvd}')
                threading.Thread(self.clientHandler(client=newClient, address=newAddress)).start()
            except:
                pass

    def clientHandler(self, client, address):

        while True:
            try:
                data = client.recv(1024).decode()
                name = data.split(":breakHere:")[0]
                msg = data.split(":breakHere:")[1]
                print(f"{name} sent {msg}")
            except:
                pass
            
    

if __name__ == '__main__':
    GUI()