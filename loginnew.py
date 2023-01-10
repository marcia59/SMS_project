from tkinter import *
from tkinter import messagebox
from PIL import ImageTk


import pymysql
# Funtionality


# GUI
class Login():
    def __init__(self, window):
        self.login_window = window
        self.login_window.geometry('990x660+50+50')
        self.login_window.resizable(0, 0)
        self.login_window.title('Login Page')

        self.bg_image = ImageTk.PhotoImage(file='bg1.jpg')
        self.bg_label = Label(self.login_window, image=self.bg_image)
        self.bg_label.place(x=0, y=0)

        self.heading = Label(self.login_window, text='USER LOGIN', font=('microsoft yahei ui light', 23, 'bold'),
                             bg='white',
                             fg='firebrick')
        self.heading.place(x=605, y=120)

        self.username_entry = Entry(self.login_window, width=25, font=('microsoft yahei ui light', 11, 'bold'),bd=0,
                                    bg='white', fg='firebrick',
                                    highlightbackground='white', highlightcolor='white')
        self.username_entry.place(x=580, y=200)
        self.username_entry.insert(0, 'Username')
        self.username_entry.bind('<FocusIn>', self.user_enter)

        self.frame1 = Frame(self.login_window, width=250, height=2, bg='firebrick')
        self.frame1.place(x=580, y=230)

        self.password_entry = Entry(self.login_window, width=25, font=('microsoft yahei ui light', 11, 'bold'), bd=0,
                                    bg='white', fg='firebrick',
                                    highlightbackground='white', highlightcolor='white')
        self.password_entry.place(x=580, y=260)
        self.password_entry.insert(0, 'Password')
        self.password_entry.bind('<FocusIn>', self.password_enter)

        self.frame2 = Frame(self.login_window, width=250, height=2, bg='firebrick')
        self.frame2.place(x=580, y=290)

        self.openeye = PhotoImage(file='openeye.png')
        self.eye_button = Button(self.login_window, image=self.openeye, bd=0, bg='white', activebackground='white',
                                 cursor='hand2', command=self.hide)
        self.eye_button.place(x=800, y=258)

        self.forget_button = Button(self.login_window, text='Forget password?', font=('microsoft yahei ui light', 12), bd=0, bg='white',
                                    activebackground='white',
                                    highlightbackground='white', highlightcolor='white', fg='firebrick', cursor='hand2',
                                    command=self.hide)
        self.forget_button.place(x=690, y=300)

        self.login_button = Button(self.login_window, text='Login', font=('Open Sans', 16, 'bold'), fg='white',
                                   bg='firebrick',activeforeground='white',activebackground='firebrick1',
                                   bd=0,cursor='hand2', width=20,command=self.login_user)
        self.login_button.place(x=570, y=350)
        self.orLabel=Label(self.login_window,text='---------------OR---------------', font=('open sans',16),
                           fg='firebrick1',bg='white')
        self.orLabel.place(x=580,y=400)

        self.facebook_logo = PhotoImage(file='facebook.png')
        self.fbLabel = Label(self.login_window,
                             image=self.facebook_logo, bg='white')
        self.fbLabel.place(x=640,y=440)

        self.gg_logo = PhotoImage(file='google.png')
        self.ggLabel = Label(self.login_window,
                             image=self.gg_logo, bg='white')
        self.ggLabel.place(x=690, y=440)

        self.twitter_logo = PhotoImage(file='twitter.png')
        self.twitterLabel = Label(self.login_window,
                             image=self.twitter_logo, bg='white')
        self.twitterLabel.place(x=740, y=440)


        self.signup_label = Label(self.login_window, text='Don\'t have an account?', font=('open sans',9, 'bold'), bg='white',
                                  fg='firebrick')
        self.signup_label.place(x=590, y=500)

        self.newaccount_button = Button(self.login_window, text='Create new one', font=('open sans', 9, 'bold underline'), fg='blue',
                                        bg='white',bd=0,cursor='hand2',
                                        activeforeground='blue', activebackground='white', width=15,
                                        command=self.signup_page)
        self.newaccount_button.place(x=727, y=500)

    # Function
    def user_enter(self,event):
        if self.username_entry.get() == 'Username':
            self.username_entry.delete(0, END)

    def password_enter(self,event):
        if self.password_entry.get() == 'Password':
            self.password_entry.delete(0, END)

    def hide(self):
        self.openeye.config(file='closeye.png')
        self.password_entry.config(show='*')
        self.eye_button.config(command=self.show)

    def show(self):
        self.openeye.config(file='openeye.png')
        self.password_entry.config(show='')
        self.eye_button.config(command=self.hide)

    def signup_page(self):
        from signup import Signup
        self.new_window = Toplevel(self.login_window)
        self.app = Signup(self.new_window)
    def login_user(self):
        if self.username_entry.get()=='' or self.password_entry.get=='':
            messagebox.showerror('Error', 'All fields required!')

        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='mai59')
                mycursor = con.cursor()
            except:
                messagebox.showerror('Error', 'Connect failed.')
                return
            query = 'use userdata'
            mycursor.execute(query)
            query = 'select *from data where username=%s and password=%s'
            mycursor.execute(query,(self.username_entry.get(),self.password_entry.get()))
            row = mycursor.fetchone()
            if row == None:
                messagebox.showerror('Error', 'Invalid username or password')
            else:
                messagebox.showinfo('Success','Login is successfull!')

if __name__ == '__main__':
    window = Tk()
    obj = Login(window)
    window.mainloop()