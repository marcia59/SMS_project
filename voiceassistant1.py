import tkinter.scrolledtext
from tkinter.ttk import *
from tkinter import *
import os
import pyttsx3


import speech_recognition


from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


class talking:
    def __init__(self,root):
        self.root=root
        self.root.geometry("500x570+100+30")
        self.root.title("Chatbox")
        self.root.configure(bg="lightgray")
        self.askpic = PhotoImage(file='ask-for-help.png')
        self.audpic = PhotoImage(file='sound.png')
        self.bot = ChatBot('Monica')
        self.trainer = ListTrainer(self.bot)

        self.data_list = ['Hello',
                          'Hi',
                          'Hi',
                          'Hello',
                          'What is your name',
                          'Monica,I am your voice assistant in Student Management System',
                          "What's your name",
                          'Monica,I am your voice assistant in Student Management System',

                          ]


        for files in os.listdir('english\\'):
            self.data = open('english\\'+files,'r',encoding='utf-8').readlines()
            self.trainer.train(self.data)
        self.trainer.train(self.data_list)

        self.centreFrame = Frame(self.root)
        self.centreFrame.pack()

        self.txt_area=tkinter.scrolledtext.ScrolledText(self.centreFrame,wrap=WORD)
        self.txt_area.pack(padx=20,pady=5,expand=True,side=LEFT)

        self.questionField=Entry(self.root,font=("Laboo",12))
        self.questionField.pack(padx=20,pady=20,fill=X)

        self.askButton = Button(self.root,image=self.askpic,command=self.botrep)
        self.askButton.pack()

        self.audButton = Button(self.root,image=self.audpic,command=self.AudtoTxt)
        self.audButton.pack()

        def click(event):
            self.askButton.invoke()
        self.root.bind('<Return>',click)

        # self.thread = threading.Thread(target=self.AudtoTxt)
        # self.thread.setDaemon(True)
        # self.thread.start()
    def texttovoice(self, text):
        txt = pyttsx3.init()
        voice = txt.getProperty("voices")
        txt.setProperty('voice', voice[1].id)
        txt.say(text)
        txt.runAndWait()

    def botrep(self):
        self.question = self.questionField.get()
        self.question = self.question.capitalize()
        self.answer = self.bot.get_response(self.question)
        self.txt_area.insert(END,'You: '+self.question+'\n\n')
        self.txt_area.insert(END, 'Teiv: ' + str(self.answer)+'\n\n')
        self.texttovoice(self.answer)
        self.questionField.delete(0,END)
    def AudtoTxt(self):
        # while True:
            self.temp = speech_recognition.Recognizer()
            try:
                with speech_recognition.Microphone() as m:
                    self.temp.adjust_for_ambient_noise(m,duration=0.2)
                    self.aud = self.temp.listen(m)
                    self.txtfromaud = self.temp.recognize_google(self.aud)

                    self.questionField.delete(0,END)
                    self.questionField.insert(0,self.txtfromaud)
                    self.botrep()
            except Exception as e:
                print(e)

if __name__ == "__main__":
        root=Tk()
        obj=talking(root)
        root.mainloop()