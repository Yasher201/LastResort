import sqlite3, hashlib
from tkinter import *
import os
from tkinter import simpledialog
from functools import partial
import random
import string


class App:

    def __init__(self, main):
        self.main = main
        file_exists = os.path.exists(os.getcwd()+'/database.db')
        if file_exists:
            self.SignScreen()
        else:
            self.MakeMasterPass()

        self.main.mainloop()


    def generatePass(self):
        lowercase = "abcdefghijklmnopqrstuvwxyz"
        uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        special_char = "!@#$%^&*:;?+-/"
        num = "0123456789"
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        num = string.digits
        special_char = string.punctuation
        auto_pass = uppercase + lowercase + special_char + num
        total_len = random.randint(8, 12)
        final_pass = "".join(random.sample(auto_pass, total_len))
        self.main.clipboard_clear()
        self.main.clipboard_append(final_pass)
        self.main.update()

    def hashPassword(self, storing):
        hashing = hashlib.md5(storing)
        return hashing.hexdigest()

    
    def MakeMasterPass(self):
        for widget in self.main.winfo_children():
            widget.destroy()

        self.main.geometry("400x200")
        label = Label(self.main, text= "Enter Master Key", fg="green")
        label.config(anchor=CENTER)
        label.pack()
        
        txt_entry = Entry(self.main, width=25, show="*")
        txt_entry.pack()
        txt_entry.focus()
        
        label1 = Label(self.main, text= "Confirm Master Key", fg="green")
        label1.pack()


        txt_entry2 = Entry(self.main, width=25, show="*")
        txt_entry2.pack()

        label2 = Label(self.main)
        label2.pack()

        def SecurePass():
            if txt_entry.get() == txt_entry2.get():
                hash_pass = self.hashPassword(txt_entry.get().encode('utf-8'))
                put_password = """INSERT INTO passvault(password)
                VALUES(?)"""
                
                
                with sqlite3.connect("database.db") as self.db:
                    self.cursor = self.db.cursor()


                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS passvault(
                id INTEGER PRIMARY KEY,
                password TEXT NOT NULL);
                """)

                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS vault(
                id INTEGER PRIMARY KEY,
                source TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL);""")


                self.cursor.execute(put_password, ([hash_pass]))
                self.db.commit()
                self.Vault()
            else:
                label2.config(text="Entered Password are not same ", fg='red')


        button = Button(self.main, text="Create Key", command=SecurePass)
        button.pack()

        
    def window_source(self, text):
        user_entry = simpledialog.askstring("Type in Source", text)
        return user_entry
    def window_username(self, text):
        user_entry = simpledialog.askstring("Type in User ID", text)
        return user_entry
    def window_pass(self, text):
        user_entry = simpledialog.askstring("Type in Credentials", text)
        return user_entry

    
    def SignScreen(self):
        with sqlite3.connect("database.db") as self.db:
            self.cursor = self.db.cursor()
        
        self.main.geometry("400x200")
        label = Label(self.main, text= "Enter Master Key", fg="green")
        label.config(anchor=CENTER)
        label.pack()
        
        label1 = Label(self.main, text= "")
        label1.pack()
        
        txt_entry = Entry(self.main, width=25, show="*")
        txt_entry.pack()
        txt_entry.focus()    

        def checkPass():
            inspectHashPass = self.hashPassword(txt_entry.get().encode('utf-8'))
            self.cursor.execute("SELECT * FROM passvault WHERE id = 1 AND password = ?", [(inspectHashPass)])
            return self.cursor.fetchall()


        def ScanPass():
            TrueMatch = checkPass()
            if TrueMatch:
                self.Vault()
            else:
                txt_entry.delete(0,"end")
                label1.config(text="Invalid Password", fg="red")
        
        button = Button(self.main, text="ENTER", command=ScanPass)
        button.pack()
            

    def Vault(self):
        for widget in self.main.winfo_children():
            widget.destroy()
        def Entering():
            textSource = "Source"
            textUsername = "Username"
            textPassword = "Password"
            source = self.window_source(textSource)
            username = self.window_username(textUsername)
            password = self.window_pass(textPassword)

            place_fields = """INSERT INTO vault(source,username,password)
            VALUES(?, ?, ?)"""
            if (source == None or username == None or password == None):
                return
            if (len(source) == 0) or (len(username) == 0) or (len(password) == 0):
                return
            self.cursor.execute(place_fields, (source, username, password))
            self.db.commit()
            self.Vault()
        
        def withdraw(input):
            self.cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
            self.db.commit()
            self.Vault()

        self.main.geometry("800x400")
        self.mark = Label(self.main, text="List of Login Information:", fg="green")
        self.mark.grid(column=1)
        button = Button(self.main, text="Add Information", command=Entering)
        button.grid(column=1, pady=10)

        generatePasswordButton = Button(self.main, text="Copy Random Password", command=lambda:self.generatePass())
        generatePasswordButton.grid(column=1, pady=10, padx=0)
        
        
        self.mark = Label(self.main, text="Source:")
        self.mark.grid(row=3, column=0, padx=80)
        self.mark = Label(self.main, text="Username:")
        self.mark.grid(row=3, column=1, padx=80)
        self.mark = Label(self.main, text="Password:")
        self.mark.grid(row=3, column=2, padx=80)

        self.cursor.execute("SELECT * FROM vault")
        if(self.cursor.fetchall() != None):
            num = 0 
            while True:
                self.cursor.execute("SELECT * FROM vault")
                lists = self.cursor.fetchall()
                if (len(lists) == 0):
                    break
                self.mark1 = Label(self.main, text=(lists[num][1]), font=("Times New Roman", 15))
                self.mark1.grid(column=0, row=num+4)
                self.mark1 = Label(self.main, text=lists[num][2], font=("Times New Roman", 15))
                self.mark1.grid(column=1, row=num+4)
                self.mark1 = Label(self.main, text=lists[num][3], font=("Times New Roman", 15))
                self.mark1.grid(column=2, row=num+4)
            
                button1 = Button(self.main, text="Delete", command= partial(withdraw, lists[num][0]))
                button1.grid(column=3, row=num+4, pady=10)
                num = num+1
                self.cursor.execute("SELECT * FROM vault")
                if(len(self.cursor.fetchall()) <= num):
                    break

main = Tk()
main.title("LAST RESORT")
app = App(main)