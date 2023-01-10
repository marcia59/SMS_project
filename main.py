from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql
from SMS2 import Student_management_system
from voiceassistant import talking

class Supporting_system:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x550+0+0")
        self.root.resizable(0,0)
        self.root.title('Education support system')


        image = Image.open('slogan.jpg')
        image = image.resize((800,150), Image.ANTIALIAS)
        self.photoimg =ImageTk.PhotoImage(image)

        # label image
        f_label = Label(self.root, image=self.photoimg)
        f_label.place(x=0,y=0,width=800, height=150)

        #Bg image
        bgimg = Image.open('blue1.jpg')
        bgimg = bgimg.resize((800, 600), Image.ANTIALIAS)
        self.photoimg1 = ImageTk.PhotoImage(bgimg)

        self.bg_img = Label(self.root, image=self.photoimg1)
        self.bg_img.place(x=0, y=130, width=800, height=600)

        self.title_lbl = Label(self.bg_img, text='EDUCATION SUPPORTING SYSTEM',
                          font=('Times new roman',20,'bold'),
                          bg='white', fg='darkblue')
        self.title_lbl.place(x=0,y=0,width=800, height=35)

        #student management button
        stuimg = Image.open('svneu.jpg')
        stuimg = stuimg.resize((200, 200), Image.ANTIALIAS)
        self.photoimg2 = ImageTk.PhotoImage(stuimg)

        self.sms_button = Button(self.bg_img, image= self.photoimg2, cursor='hand2',
                            state=DISABLED,command= self.sms_data)
        self.sms_button.place(x=30, y=100, width=200, height=200)

        self.sms_button1 = Button(self.bg_img, text='Student Details', cursor='hand2',
                             font=('arial',10,'bold'),state=DISABLED,
                             bg= 'white', fg='blue', command=self.sms_data)
        self.sms_button1.place(x=30,y=300,width=200, height=20)


        #forum button
        forumimg = Image.open('forum.jpg')
        forumimg = forumimg.resize((200,200), Image.ANTIALIAS)
        self.photoimg3 = ImageTk.PhotoImage(forumimg)
        self.forum_button = Button(self.bg_img, image= self.photoimg3, state=DISABLED,
                              cursor='hand2', command=self.forum_data)
        self.forum_button.place(x=300, y=100, width=200, height=200)
        self.forum_button1 = Button(self.bg_img, text='Forum', cursor='hand2',
                             font=('arial',10,'bold'), state=DISABLED,
                             bg= 'white', fg='blue')
        self.forum_button1.place(x=300,y=300,width=200, height=20)

        #Assistant button
        assist = Image.open('voiceassistant.jpg')
        assist = assist.resize((200,200), Image.ANTIALIAS)
        self.photoimg4 = ImageTk.PhotoImage(assist)
        self.assist_button = Button(self.bg_img, image= self.photoimg4, state=DISABLED,
                              cursor='hand2', command=self.assistant_data)
        self.assist_button.place(x=570,y=100,width=200,height=200)
        self.assist_button1 = Button(self.bg_img, text='Voice assistant', cursor='hand2',
                             font=('arial',10,'bold'), state=DISABLED,
                             bg= 'white', fg='blue', command=self.assistant_data)
        self.assist_button1.place(x=570, y=300, width=200, height=20)

        #login button
        self.login_button = Button(self.bg_img, cursor='hand2', text='Log in',bd=0,
                              font=('Calibri',10), command=self.login_data)
        self.login_button.place(x=600,y=40, width=80, height=20)

        #logout button
        self.logout_button = Button(self.bg_img, cursor='hand2', text='Log out',bd=0,
                              font=('Calibri',10), command=self.logout_data)
        self.logout_button.place(x =700, y=40,width=80, height=20)




        ### Function ###
    def sms_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Student_management_system(self.new_window)
    def login_data(self):
        def user_enter(event):
            if self.username_entry.get() == 'Username':
                self.username_entry.delete(0, END)

        def password_enter(event):
            if self.password_entry.get() == 'Password':
                self.password_entry.delete(0, END)

        def hide():
            self.openeye.config(file='closeye.png')
            self.password_entry.config(show='*')
            self.eye_button.config(command=show)

        def show():
            self.openeye.config(file='openeye.png')
            self.password_entry.config(show='')
            self.eye_button.config(command=hide)

        def signup_page():
            from signup import Signup
            self.new_window = Toplevel(self.login_window)
            self.app = Signup(self.new_window)

        def login_user():
            if self.username_entry.get() == '' or self.password_entry.get == '':
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
                mycursor.execute(query, (self.username_entry.get(), self.password_entry.get()))
                row = mycursor.fetchone()
                if row == None:
                    messagebox.showerror('Error', 'Invalid username or password')
                else:
                    messagebox.showinfo('Success', 'Login is successfull!')
                    self.sms_button.config(state=NORMAL)
                    self.sms_button1.config(state=NORMAL)
                    self.forum_button.config(state=NORMAL)
                    self.forum_button1.config(state=NORMAL)
                    self.assist_button.config(state=NORMAL)
                    self.assist_button1.config(state=NORMAL)
                    self.login_window.destroy()

        def forgot_password():
            from forgotpassword import Forgot_password
            self.new_window = Toplevel(self.login_window)
            self.app = Forgot_password(self.new_window)


        # self.new_window = Toplevel(self.root)
        # self.app = Login(self.new_window)
        self.login_window = Toplevel()
        # self.login_window.grab_set()
        self.login_window.geometry('990x660+50+50')
        self.login_window.resizable(0, 0)
        self.login_window.title('Login Page')

        self.bg_image = ImageTk.PhotoImage(file='bglogin.png')
        self.bg_label = Label(self.login_window, image=self.bg_image)
        self.bg_label.place(x=0, y=0)

        self.username_entry = Entry(self.login_window, width=28, font=('manrope', 11),
                                    bg='#e8f7fb', fg='#03045e', borderwidth=3,
                                    highlightbackground='#03045e', highlightcolor='#03045e')

        self.username_entry.place(x=568, y=300)
        self.username_entry.insert(0, 'Username')
        self.username_entry.bind('<FocusIn>', user_enter)

        self.password_entry = Entry(self.login_window, width=28, font=('manrope', 11),
                                    bg='#e8f7fb', fg='#03045e', borderwidth=3,
                                    highlightbackground='#03045e', highlightcolor='#03045e')

        self.password_entry.place(x=568, y=350)
        self.password_entry.insert(0, 'Password')
        self.password_entry.bind('<FocusIn>', password_enter)

        self.openeye = PhotoImage(file='openeye.png')
        self.eye_button = Button(self.login_window, image=self.openeye, bd=0, bg='#e8f7fb', activebackground='#e8f7fb',
                                 cursor='hand2', height=15, command=hide)
        self.eye_button.place(x=768, y=354)

        self.forget_button = Button(self.login_window, text='Forget password?', font=('manrope', 10, 'underline'),
                                    bd=0, bg='white',
                                    activebackground='white',
                                    highlightbackground='white', highlightcolor='white', fg='#03045e', cursor='hand2',
                                    command=forgot_password)
        self.forget_button.place(x=690, y=380)

        self.login_button = Button(self.login_window, text='Login', font=('Open Sans', 16, 'bold'), fg='white',
                                   bg='#03045e', activeforeground='white', activebackground='#0077b6',
                                   bd=0, cursor='hand2', width=16, command=login_user)
        self.login_button.place(x=578, y=420)

        self.signup_label = Label(self.login_window, text='Don\'t have an account?', font=('manrope', 9),
                                  bg='white',
                                  fg='#03045e')
        self.signup_label.place(x=580, y=480)

        self.newaccount_button = Button(self.login_window, text='Create',
                                        font=('open sans', 9, 'bold underline'), fg='#03045e',
                                        bg='white', bd=0, cursor='hand2',
                                        activeforeground='#03045e', activebackground='white', width=10,
                                        command=signup_page)
        self.newaccount_button.place(x=715, y=480)


    def logout_data(self):
            result = messagebox.askyesno('Confirm', 'Do you want to log out?')
            if result:
                self.root.destroy()
            else:
                pass

    def forum_data(self):
        from client import Client
    def assistant_data(self):
        self.new_window = Toplevel(self.root)
        self.app = talking(self.new_window)













if __name__ == '__main__':
    root = Tk()
    obj = Supporting_system(root)
    root.mainloop()