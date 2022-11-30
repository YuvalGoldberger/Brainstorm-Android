import socket
import threading
from tkinter import *
from tkinter.font import Font
import pyglet

class GUI:

    SCREEN_WIDTH = 1270
    SCREEN_HEIGHT = 720
    FOLDER_LOCATION = r'D:\Yuval_Python\Yuval_Final_Proj\Projects-Github\Brainstorm-Android\Brainstorm-Android\Python-Tkinter\Fonts'
    MAX_CLIENTS = 5

    def __init__(self):
        self.screen = Tk()
        self.associationsList = []

        self.screen.title("Brainstorm by Yuval Goldberger")
        self.screen.geometry(f'{self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}')

        # ----- Set Font -----
        pyglet.font.add_file(f'{self.FOLDER_LOCATION}\Assistant-ExtraBold.ttf')
        pyglet.font.add_file(f'{self.FOLDER_LOCATION}\Assistant-Bold.ttf')
        pyglet.font.add_file(f'{self.FOLDER_LOCATION}\Assistant-Medium.ttf')

        self.AssistantFont = Font(
            family="Assistant",
            size=12
        )
        # ----- Shows the main label in the top of the screen -----
        mainLabel = Label(self.screen, font=("Assistant", 50, 'bold'), text="BrainStorm").pack()
        # ----- Text above the textbox ----- 
        ideaLabel = Label(self.screen, font=("Assistant", 30, 'normal'), text="Enter Idea").pack()
        # ----- Creates a textbox for idea -----
        self.ideaBox = Text(self.screen, height=10, width=100).pack()
        sendIdea = Button(self.screen, font=self.AssistantFont, text="Send Idea", command=self.sendIdea).pack()
        
        # ----- Button to open scrollbar -----        
        openScrollbarButton = Button(self.screen, font=self.AssistantFont, text="Choose amount of participants")
        openScrollbarButton.place(x = 70, y = 20)
        self.screen.update()

        openScrollbarButton.config(command= lambda : self.showScrollbar(xLoc=openScrollbarButton.winfo_width() / 2, button=openScrollbarButton))

        # ----- Show associations -----
        showAssociations = Button(self.screen, font=("Assistant", 30, 'normal'), text="Refresh Associations", command=self.refresh).pack()

        # ----- Mainloop -----
        self.screen.mainloop()


    # ----- Scrollbar to choose amount of participants ------
    def showScrollbar(self, xLoc, button):
            
        _button = button
        button.place_forget()

        self.closeScrollbarButton = Button(self.screen, font= self.AssistantFont, \
                text="Close Scrollbar", command=lambda : self.hideScrollbar(button=_button))
        self.closeScrollbarButton.place(x=90, y=20)

        self.scrollbar = Scrollbar(self.screen)
        self.scrollbar.place( x=xLoc-20, in_=self.closeScrollbarButton, rely=1.0, bordermode="outside", height=100 )

        self.listbox = Listbox(self.screen, yscrollcommand = self.scrollbar.set, font=self.AssistantFont.config(size=10))
        for line in range(100):
            self.listbox.insert(END, f'{line+1} Participant(s)')

        self.listbox.place( x=xLoc- 50, in_=self.closeScrollbarButton, rely=1.0, bordermode="outside", height=100 )
        self.scrollbar.config( command = self.listbox.yview )

        self.screen.update()
        

    def hideScrollbar(self, button):
           
        self.listbox.place_forget()
        self.scrollbar.place_forget()
        button.place(x=70, y=20)
        self.closeScrollbarButton.place_forget()
        
        self.screen.update()

    def sendIdea(self):
        _subject = self.ideaBox.get(1.0, "end-1c")
        server = socket.socket()
        server.bind(('0.0.0.0', 25565))
        server.listen(self.MAX_CLIENTS)

        while True:
            newClient, newAddress = server.accept()
            print(newAddress, "connected")
            threading.Thread(self.clientHandler(client=newClient, address=newAddress, subject=_subject)).start()   

    def clientHandler(self, client, address, subject):
        client.send(subject.encode())
        data = client.recv(1024).decode()
        
        while True:
            data = client.recv(1024).decode()
            self.associationsList.append(data)

    def refresh(self):
        assoNoName = []
        for a in self.associationsList:
            assoNoName.append(a.split(":breakHere:")[0])
        assoList = Listbox(self.screen)
    

if __name__ == '__main__':
    GUI()