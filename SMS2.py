from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox,filedialog
from PIL import Image
from PIL import ImageTk
import pyttsx3
import pymysql
import pandas

class Student_management_system:
    def __init__(self, root):
        self.root = root
        self.root.configure(background='white')
        self.root.geometry('1174x680+0+0')
        self.root.resizable(0, 0)
        self.root.title('Student Management System')
        self.text = ''
        self.count = 0

        self.datetimeLabel = Label(self.root, font=('arial', 16, 'bold'), background='white')
        self.datetimeLabel.place(x=5, y=5)
        self.clock()

        self.s = 'NEU Student Management System'  # s[count]=t when count is 1
        self.sliderLabel = Label(self.root, font=('arial', 28, 'bold'), width=30, background='white')
        self.sliderLabel.place(x=200, y=0)
        self.slider()

        self.connectButton = ttk.Button(self.root, text='Connect database', command= self.connect_database)
        self.connectButton.place(x=980, y=0)

        #### LEFT FRAME ######
        self.leftFrame = Frame(self.root)
        self.leftFrame.configure(background='white')
        self.leftFrame.place(x=75, y=80, width=300, height=600)

        self.img = Image.open('logoneu.png')
        self.img = self.img.resize((75, 75), Image.ANTIALIAS)
        self.logo_image = ImageTk.PhotoImage(self.img)
        self.logo_label = Label(self.leftFrame, image=self.logo_image, background='white')
        self.logo_label.grid(row=0, column=0)

        self.addstudentButton = ttk.Button(self.leftFrame, text='Add Student', width=25, state=DISABLED,
                                           command=lambda : self.toplevel_data('Add Student','Add',self.add_data))
        self.addstudentButton.grid(row=1, column=0, pady=20)


        self.searchstudentButton = ttk.Button(self.leftFrame, text='Search Student', width=25, state=DISABLED,
                                              command=lambda :self.toplevel_data('Search Student','Search',self.search_data))
        self.searchstudentButton.grid(row=2, column=0, pady=20)

        self.deletestudentButton = ttk.Button(self.leftFrame, text='Delete Student', width=25, state=DISABLED, command=self.delete_student)
        self.deletestudentButton.grid(row=3, column=0, pady=20)

        self.updatestudentButton = ttk.Button(self.leftFrame, text='Update Student', width=25, state=DISABLED,
                                              command=lambda :self.toplevel_data('Update Student','Update',self.update_data))
        self.updatestudentButton.grid(row=4, column=0, pady=20)

        self.showstudentButton = ttk.Button(self.leftFrame, text='Show Student', width=25, state=DISABLED, command=self.show_student)
        self.showstudentButton.grid(row=5, column=0, pady=20)

        self.exportstudentButton = ttk.Button(self.leftFrame, text='Export data', width=25, state=DISABLED, command=self.export_data)
        self.exportstudentButton.grid(row=6, column=0, pady=20)

        self.exitButton = ttk.Button(self.leftFrame, text='Exit', width=25,command=self.iexit)
        self.exitButton.grid(row=7, column=0, pady=20)


        ######## RIGHT FRAME #############

        self.rightFrame = Frame(self.root)
        self.rightFrame.place(x=350, y=80, width=820, height=600)

        self.scrollBarX = Scrollbar(self.rightFrame, orient=HORIZONTAL)
        self.scrollBarY = Scrollbar(self.rightFrame, orient=VERTICAL)

        self.studentTable = ttk.Treeview(self.rightFrame, show='headings',
                                         columns=('ID', 'Name', 'Phone', 'Email', 'Address', 'Gender',
                                                  'Date of Birth', 'Faculty', 'Major', 'Added Date','Added Time'),
                                         xscrollcommand=self.scrollBarX.set,
                                         yscrollcommand=self.scrollBarY.set)
        self.scrollBarX.config(command=self.studentTable.xview)
        self.scrollBarY.config(command=self.studentTable.yview)

        self.scrollBarX.pack(side=BOTTOM, fill=X)
        self.scrollBarY.pack(side=RIGHT, fill=Y)

        self.studentTable.pack(expand=1, fill=BOTH)

        self.studentTable.heading('ID', text='ID')
        self.studentTable.heading('Name', text='Name')
        self.studentTable.heading('Phone', text='Phone')
        self.studentTable.heading('Email', text='Email Address')
        self.studentTable.heading('Address', text='Address')
        self.studentTable.heading('Gender', text='Gender')
        self.studentTable.heading('Date of Birth', text='Date of Birth')
        self.studentTable.heading('Faculty', text='Faculty')
        self.studentTable.heading('Major', text='Major')
        self.studentTable.heading('Added Date', text='Added Date')
        self.studentTable.heading('Added Time', text='Added Time')

        self.studentTable.column('ID', width=100)
        self.studentTable.column('Name', width=150, anchor=CENTER)
        self.studentTable.column('Phone', width=150, anchor=CENTER)
        self.studentTable.column('Email', width=200, anchor=CENTER)
        self.studentTable.column('Address', width=200, anchor=CENTER)
        self.studentTable.column('Gender', width=150, anchor=CENTER)
        self.studentTable.column('Date of Birth', width=150, anchor=CENTER)
        self.studentTable.column('Faculty', width=250, anchor=CENTER)
        self.studentTable.column('Major', width=250, anchor=CENTER)
        self.studentTable.column('Added Date', width=200, anchor=CENTER)
        self.studentTable.column('Added Time', width=200, anchor=CENTER)

        self.style = ttk.Style()
        self.style.configure('Treeview', rowheight=25, font=('arial', 10), background='#99CCFF',
                        fieldbackground='white')
        self.style.configure('Treeview.Heading', font=('arial', 12, 'bold'))

    ######## FUNCTION PART #################
    def clock(self):
        self.date = time.strftime('%d/%m/%Y')
        self.currenttime = time.strftime('%H:%M:%S')
        self.datetimeLabel.config(text=f'   Date: {self.date}\nTime: {self.currenttime}')
        self.datetimeLabel.after(1000, self.clock)

    def slider(self):

        if self.count == len(self.s):
            self.count = 0
            self.text = ''
        self.text = self.text + self.s[self.count]
        self.sliderLabel.config(text=self.text)
        self.count += 1
        self.sliderLabel.after(300, self.slider)

    def connect_database(self):

        def connect():
            self.texttovoice('Connecting database')
            try:
                global mycursor, con
                con = pymysql.connect(host=hostEntry.get(), user=usernameEntry.get(), password=passwordEntry.get())
                mycursor = con.cursor()
            except:
                messagebox.showerror('Error', 'Invalid Details', parent=connectWindow)
                return

            try:
                query = 'create database sms2'
                mycursor.execute(query)
                query = 'use sms2'
                mycursor.execute(query)
                query = 'create table student(id int  not null primary key, name varchar(30),phone varchar(10),email varchar(30),' \
                        'address varchar(100),gender varchar(20), dob varchar(20),faculty varchar(100), ' \
                        'major varchar(100),date varchar(50), time varchar(50))'
                mycursor.execute(query)
            except:
                query = 'use sms2'
                mycursor.execute(query)
            messagebox.showinfo('Success', 'Database Connection is successful', parent=connectWindow)
            connectWindow.destroy()
            self.addstudentButton.config(state=NORMAL)
            self.searchstudentButton.config(state=NORMAL)
            self.updatestudentButton.config(state=NORMAL)
            self.showstudentButton.config(state=NORMAL)
            self.exportstudentButton.config(state=NORMAL)
            self.deletestudentButton.config(state=NORMAL)

        connectWindow = Toplevel()
        connectWindow.grab_set()
        connectWindow.geometry('470x250+730+230')
        connectWindow.title('Database Connection')
        connectWindow.configure(background='white')
        connectWindow.resizable(0,0)

        hostnameLabel = Label(connectWindow, text='Host Name', font=('arial', 20, 'bold'), background='white')
        hostnameLabel.grid(row=0, column=0, padx=20)

        hostEntry = Entry(connectWindow, font=('times new roman', 15, 'bold'), bd=2, background='white')
        hostEntry.grid(row=0, column=1, padx=40, pady=20)

        usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'), background='white')
        usernameLabel.grid(row=1, column=0, padx=20)

        usernameEntry = Entry(connectWindow, font=('times new roman', 15, 'bold'), bd=2, background='white')
        usernameEntry.grid(row=1, column=1, padx=40, pady=20)

        passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'), background='white')
        passwordLabel.grid(row=2, column=0, padx=20)

        passwordEntry = Entry(connectWindow, font=('times new roman', 15, 'bold'), bd=2, background='white')
        passwordEntry.grid(row=2, column=1, padx=40, pady=20)

        connectButton = ttk.Button(connectWindow, text='CONNECT', command=connect)
        connectButton.grid(row=3, columnspan=2)

    def toplevel_data(self, title, button_text, command):
        global idEntry, phoneEntry, nameEntry, emailEntry, addressEntry, genderEntry, dobEntry, facultyEntry, majorEntry, screen
        screen = Toplevel()
        screen.title(title)
        screen.configure(background='white')
        screen.grab_set()
        screen.resizable(False, False)
        idLabel = Label(screen, text='ID', font=('times new roman', 20, 'bold'), background='white')
        idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
        idEntry = Entry(screen, font=('times new roman', 15, 'bold'), width=24)
        idEntry.grid(row=0, column=1, pady=15, padx=10)

        nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'), background='white')
        nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
        nameEntry = Entry(screen, font=('times new roman', 15, 'bold'), width=24)
        nameEntry.grid(row=1, column=1, pady=15, padx=10)

        phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'), background='white')
        phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
        phoneEntry = Entry(screen, font=('times new roman', 15, 'bold'), width=24)
        phoneEntry.grid(row=2, column=1, pady=15, padx=10)

        emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'), background='white')
        emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
        emailEntry = Entry(screen, font=('times new roman', 15, 'bold'), width=24)
        emailEntry.grid(row=3, column=1, pady=15, padx=10)

        addressLabel = Label(screen, text='Address', font=('times new roman', 20, 'bold'), background='white')
        addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
        addressEntry = Entry(screen, font=('times new roman', 15, 'bold'), width=24)
        addressEntry.grid(row=4, column=1, pady=15, padx=10)

        genderLabel = Label(screen, text='Gender', font=('times new roman', 20, 'bold'), background='white')
        genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
        genderEntry = Entry(screen, font=('times new roman', 15, 'bold'), width=24)
        genderEntry.grid(row=5, column=1, pady=15, padx=10)

        dobLabel = Label(screen, text='Date of Birth', font=('times new roman', 20, 'bold'), background='white')
        dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
        dobEntry = Entry(screen, font=('times new roman', 15, 'bold'), width=24)
        dobEntry.grid(row=6, column=1, pady=15, padx=10)

        facultyLabel = Label(screen, text='Faculty', font=('times new roman', 20, 'bold'), background='white')
        facultyLabel.grid(row=7, column=0, padx=30, pady=15, sticky=W)
        facultyEntry = Entry(screen, font=('times new roman', 15, 'bold'), width=24)
        facultyEntry.grid(row=7, column=1, pady=15, padx=10)

        majorLabel = Label(screen, text='Major', font=('times new roman', 20, 'bold'), background='white')
        majorLabel.grid(row=8, column=0, padx=30, pady=15, sticky=W)
        majorEntry = Entry(screen, font=('times new roman', 15, 'bold'), width=24)
        majorEntry.grid(row=8, column=1, pady=15, padx=10)

        student_button = ttk.Button(screen, text=button_text, command=command)
        student_button.grid(row=9, columnspan=2, pady=15)

        if title == 'Update Student':
            indexing = self.studentTable.focus()
            content = self.studentTable.item(indexing)
            listdata = content['values']
            idEntry.insert(0, listdata[0])
            nameEntry.insert(0, listdata[1])
            phoneEntry.insert(0, listdata[2])
            emailEntry.insert(0, listdata[3])
            addressEntry.insert(0, listdata[4])
            genderEntry.insert(0, listdata[5])
            dobEntry.insert(0, listdata[6])
            facultyEntry.insert(0, listdata[7])
            majorEntry.insert(0, listdata[8])

    def texttovoice(self, text):
        txt = pyttsx3.init()
        voice = txt.getProperty("voices")
        txt.setProperty('voice',voice[1].id)
        txt.say(text)
        txt.runAndWait()

    def add_data(self):
        self.texttovoice('adding student')
        if idEntry.get() == '' or nameEntry.get() == '' or phoneEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' \
                or genderEntry.get() == '' or dobEntry.get() == '' or facultyEntry.get() == '' or majorEntry.get() == '':
            messagebox.showerror('Error', 'All Feilds are required', parent=screen)

        else:
            try:
                query = 'insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                mycursor.execute(query, (
                idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
                genderEntry.get(), dobEntry.get(), facultyEntry.get(), majorEntry.get(), self.date, self.currenttime))
                con.commit()
                result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clean the form?',
                                             parent=screen)
                if result:
                    idEntry.delete(0, END)
                    nameEntry.delete(0, END)
                    phoneEntry.delete(0, END)
                    emailEntry.delete(0, END)
                    addressEntry.delete(0, END)
                    genderEntry.delete(0, END)
                    dobEntry.delete(0, END)
                    facultyEntry.delete(0, END)
                    majorEntry.delete(0, END)
                else:
                    pass
            except:
                messagebox.showerror('Error', 'Id cannot be repeated', parent=screen)
                return

            self.show_student()

            # query = 'select *from student'
            # mycursor.execute(query)
            # fetched_data = mycursor.fetchall()
            # self.studentTable.delete(*self.studentTable.get_children())
            # for data in fetched_data:
            #     self.studentTable.insert('', END, values=data)

    def search_data(self):
        self.texttovoice('searching student')
        query = 'select * from student where id=%s or name=%s or email=%s or phone=%s or address=%s' \
                ' or gender=%s or dob=%s or faculty=%s or major=%s'
        mycursor.execute(query, (idEntry.get(), nameEntry.get(), emailEntry.get(), phoneEntry.get(), addressEntry.get(),
                                 genderEntry.get(), dobEntry.get(), facultyEntry.get(), majorEntry.get()))
        self.studentTable.delete(*self.studentTable.get_children())
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            self.studentTable.insert('', END, values=data)

    def delete_student(self):
        self.texttovoice('deleting student')
        indexing = self.studentTable.focus()
        print(indexing)
        content = self.studentTable.item(indexing)
        content_id = content['values'][0]
        query = 'delete from student where id=%s'
        mycursor.execute(query, content_id)
        con.commit()
        messagebox.showinfo('Deleted', f'Id {content_id} is deleted succesfully')
        query = 'select * from student'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        self.studentTable.delete(*self.studentTable.get_children())
        for data in fetched_data:
            self.studentTable.insert('', END, values=data)

    def show_student(self):
        self.texttovoice('showing student')
        query = 'select * from student'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        self.studentTable.delete(*self.studentTable.get_children())
        for data in fetched_data:
            self.studentTable.insert('', END, values=data)

    def update_data(self):
        self.texttovoice('Updating information')
        query = 'update student set name=%s, phone=%s, email=%s, address=%s, gender=%s, dob=%s, faculty=%s, major=%s,' \
                'date=%s, time=%s where id=%s'
        mycursor.execute(query,
                         (nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(),
                          dobEntry.get(), facultyEntry.get(), majorEntry.get(), self.date, self.currenttime, idEntry.get()))
        con.commit()
        messagebox.showinfo('Success', f'Id {idEntry.get()} is modified successfully', parent=screen)
        screen.destroy()
        self.show_student()

    def export_data(self):
        self.texttovoice('Exporting data')
        url = filedialog.asksaveasfilename(defaultextension='.csv')
        indexing = self.studentTable.get_children()
        newlist = []
        for index in indexing:
            content = self.studentTable.item(index)
            datalist = content['values']
            newlist.append(datalist)

        table = pandas.DataFrame(newlist, columns=['ID', 'Name', 'Phone', 'Email', 'Address', 'Gender',
                                                   'Date of Birth', 'Faculty', 'Major', 'Added Date', 'Added Time'])
        table.to_csv(url, index=False, encoding='utf-8-sig')
        messagebox.showinfo('Success', 'Data is saved succesfully.')

    def iexit(self):
        result = messagebox.askyesno('Confirm', 'Do you want to exit?')
        if result:
            self.root.destroy()
        else:
            pass


if __name__ == '__main__':
    # root = Tk()
    root = ttkthemes.ThemedTk()
    root.get_themes()
    root.set_theme('arc')
    obj = Student_management_system(root)
    root.mainloop()