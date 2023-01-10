import email
from tkinter import messagebox
from tkinter import *

import pymysql
from PIL import ImageTk


class Signup():
    def __init__(self, window):
        self.signup_window=window
        self.signup_window.geometry('990x660+50+50')
        self.signup_window.resizable(0,0)
        self.signup_window.title('Signup Page')

        self.bg_image=ImageTk.PhotoImage(file='bgsignup.png')
        self.bg_label=Label(self.signup_window, image=self.bg_image)
        self.bg_label.grid()

        self.email_label=Label(self.signup_window, text='Email', font=('manrope', 12,'bold'),
                               bg='white', fg='#03045e')
        self.email_label.place(x=568, y=190)
        self.email_entry=Entry(self.signup_window, width=26, font=('manrope',12),
                               fg='#03045e', bg='#e8f7fb',borderwidth=3,
                               highlightbackground='#03045e', highlightcolor='#03045e')
        self.email_entry.place(x=565, y=220)
        #
        self.username_label=Label(self.signup_window, text='Username', font=('manrope', 12, 'bold'),
                                  bg='white', fg='#03045e')
        self.username_label.place(x=568, y=250)
        self.username_entry=Entry(self.signup_window, width=26, font=('manrope', 12),
                                  fg='#03045e', bg='#e8f7fb', borderwidth=3,
                                  highlightbackground='#03045e', highlightcolor='#03045e')
        self.username_entry.place(x=565, y=280)

        self.password_label=Label(self.signup_window, text='Password', font=('manrope', 12, 'bold'),
                                  bg='white', fg='#03045e')
        self.password_label.place(x=568, y=310)
        self.password_entry=Entry(self.signup_window, width=26, font=('manrope', 12),
                                  fg='#03045e', bg='#e8f7fb', borderwidth=3,
                                  highlightbackground='#03045e', highlightcolor='#03045e')
        self.password_entry.place(x=565, y=340)
        #
        self.confirm_label=Label(self.signup_window, text='Confirm Password', font=('manrope', 12, 'bold'),
                                 bg='white', fg='#03045e')
        self.confirm_label.place(x=568, y=370)
        self.confirm_entry=Entry(self.signup_window, width=26, font=('manrope', 12),
                                 fg='#03045e', bg='#e8f7fb', borderwidth=3,
                                 highlightbackground='#03045e', highlightcolor='#03045e')
        self.confirm_entry.place(x=565, y=400)
        #
        self.check = IntVar()
        self.termandcond=Checkbutton(self.signup_window, text='I agree to the Terms & Conditions',
                                     font=('manrope', 9),
                                     bg='white', fg='#03045e',variable= self.check,
                                     activebackground='white', activeforeground='#03045e', cursor='hand2')
        self.termandcond.place(x=563, y=430)
        #
        self.signup_button=Button(self.signup_window, text='Signup', font=('manrope', 16, 'bold'),
                                  bd=0, bg='#03045e', fg='white', command=self.connect_db,
                                  activebackground='#03045e', activeforeground='white',
                                  cursor='hand2', width=17, height=1)
        self.signup_button.place(x=573, y=460)
        #
        self.alreadyaccount=Label(self.signup_window, text='Already have an account?', font=('manrope', 9),
                                  bg='white', fg='#03045e')
        self.alreadyaccount.place(x=570,y = 510)

        self.login_button=Button(self.signup_window, text='Login', font=('manrope', 9, 'bold underline'),
                                 fg='#03045e', cursor='hand2', bd=0,width=9, command=self.login_page,
                                 activeforeground='#03045e')
        self.login_button.place(x=730, y=510)




    def connect_db(self):
        if self.email_entry.get()=='' or self.username_entry.get()=='' or self.password_entry.get()=='' or self.confirm_entry.get()=='':
            messagebox.showerror('Error', 'All Fields Are required!')
        elif self.password_entry.get() != self.confirm_entry.get():
            messagebox.showerror('Error', 'Password not match!')
        elif self.check.get()==0:
            messagebox.showerror('Error', 'Please accept Terms and Conditions!')
        else:
            try:
                global con, mycursor
                con = pymysql.connect(host='localhost', user='root', password='mai59')
                mycursor = con.cursor()
            except:
                messagebox.showerror('Error', 'Database connectivity issue. Please try again!')
                return
            try:
                query = 'create database userdata'
                mycursor.execute(query)
                query = 'use userdata'
                mycursor.execute(query)
                query = 'create table data(id int auto_increment primary key not null,' \
                        'email varchar(50), username varchar(100), password varchar(20))'
                mycursor.execute(query)
            except:
                mycursor.execute('use userdata')

            query='select *from data where username =%s'
            mycursor.execute(query,(self.username_entry.get()))

            row = mycursor.fetchone()
            if row != None:
                messagebox.showerror('Error', 'Username already exist!')
                return

            query = 'select *from data where email =%s'
            mycursor.execute(query, (self.email_entry.get()))
            row = mycursor.fetchone()
            if row != None:
                messagebox.showerror('Error', 'Email already used!')
                return

            else:
                query = 'insert into data(email,username,password) values(%s,%s,%s)'
                mycursor.execute(query,(self.   email_entry.get(), self.username_entry.get(), self.password_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'Registration successful!')
                self.clear()
                self.login_page()
                self.signup_window.destroy()


    def clear(self):
        self.email_entry.delete(0,END)
        self.username_entry.delete(0, END)
        self.password_entry.delete(0,END)
        self.confirm_entry.delete(0, END)
        self.check.set(0)


    def login_page(self):
        from login import Login
        self.new_window = Toplevel(self.signup_window)
        self.app = Login(self.new_window)

if __name__ == '__main__':
    window = Tk()
    obj = Signup(window)
    window.mainloop()