from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql

class Forgot_password:
    def __init__(self,window):
        self.forgot_window = window
        self.forgot_window.geometry('990x660+50+50')
        self.forgot_window.resizable(0, 0)
        self.forgot_window.title('Forgot Password')

        self.bg_image = ImageTk.PhotoImage(file='resetpass.png')
        self.bg_label = Label(self.forgot_window, image=self.bg_image)
        self.bg_label.place(x=0, y=0)

        self.username_label = Label(self.forgot_window, text='Username', font=('manrope', 12, 'bold'),
                                    bg='white', fg='#03045e')
        self.username_label.place(x=568, y=200)
        self.username_entry = Entry(self.forgot_window, width=26, font=('manrope', 12),
                                    fg='#03045e', bg='#e8f7fb', borderwidth=3,
                                    highlightbackground='#03045e', highlightcolor='#03045e')
        self.username_entry.place(x=565, y=230)

        self.newpw_label = Label(self.forgot_window, text='Password', font=('manrope', 12, 'bold'),
                                    bg='white', fg='#03045e')
        self.newpw_label.place(x=568, y=260)
        self.newpw_entry = Entry(self.forgot_window, width=26, font=('manrope', 12),
                                    fg='#03045e', bg='#e8f7fb', borderwidth=3,
                                    highlightbackground='#03045e', highlightcolor='#03045e')
        self.newpw_entry.place(x=565, y=290)

        self.cfpw_label = Label(self.forgot_window, text='Confirm password', font=('manrope', 12, 'bold'),
                                 bg='white', fg='#03045e')
        self.cfpw_label.place(x=568, y=320)
        self.cfpw_entry = Entry(self.forgot_window, width=26, font=('manrope', 12),
                                 fg='#03045e', bg='#e8f7fb', borderwidth=3,
                                 highlightbackground='#03045e', highlightcolor='#03045e')
        self.cfpw_entry.place(x=565, y=350)

        self.reset_button = Button(self.forgot_window, text='Reset Password', font=('Open Sans', 16, 'bold'), fg='white',
                                   bg='#03045e', activeforeground='white', activebackground='#0077b6',
                                   bd=0, cursor='hand2', width=16, command=self.change_pass)
        self.reset_button.place(x=578, y=420)

    def change_pass(self):
        if self.username_entry.get()=='' or self.newpw_entry.get()=='' or self.cfpw_entry.get()=='':
            messagebox.showerror('Error', 'All fields are required', parent=self.forgot_window)
        elif self.newpw_entry.get() != self.cfpw_entry.get():
            messagebox.showerror('Error','Password doesn\'t match', parent=self.forgot_window)
        else:
            con = pymysql.connect(host='localhost', user='root', password='mai59')
            mycursor = con.cursor()
            query = 'use userdata'
            mycursor.execute(query)
            query = 'select *from data where username=%s'
            mycursor.execute(query,(self.username_entry.get()))
            row = mycursor.fetchone()
            if row == None:
                messagebox.showerror('Error', 'Incorrect username', parent=self.forgot_window)
            else:
                query = 'update data set password=%s where username=%s'
                mycursor.execute(query,(self.newpw_entry.get(), self.username_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'Your password is reset',parent=self.forgot_window)
                self.forgot_window.destroy()










if __name__ == '__main__':
    window = Tk()
    obj = Forgot_password(window)
    window.mainloop()