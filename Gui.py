from functools import partial
import customtkinter as ctk
import EPM

ctk.set_appearance_mode("dark")

# Selecting color theme - blue, green, dark-blue
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("500x500")
app.title("Login")


def Guilogin():
    if EPM.login(user_entry.get(), user_pass.get()):
        label.pack_forget()
        frame.pack_forget()
        user_entry.pack_forget()
        user_pass.pack_forget()
        button.pack_forget()
        scrollable_label_button_frame.pack(pady=10)
        addbutton.pack()
        login_page.pack(pady=20)
        readData()
    else:
        wrongpassword.pack(padx=20, pady=20)


def backtologin():
    label.pack(pady=12, padx=10)
    user_entry.pack(pady=12, padx=10)
    user_pass.pack(pady=12, padx=10)
    frame.pack(pady=20, padx=40, fill='both', expand=True)
    button.pack(pady=12, padx=10)
    scrollable_label_button_frame.pack_forget()
    addbutton.pack_forget()
    login_page.pack_forget()


frame = ctk.CTkFrame(master=app)


class ScrollableLabelButtonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = ctk.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, itemname, item, image=None):
        label = ctk.CTkLabel(self, text=itemname, image=image, compound="left", padx=5, anchor="w")
        button = ctk.CTkButton(self, text="Reveal Password", width=100, height=24, command=partial(showPassword, item))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):

        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return


def readData():
    lst = EPM.readpasswords()
    for i in lst:
        scrollable_label_button_frame.add_item(i[0], i)


def deleteRecords(item, newwindow):
    EPM.deletePassword(item)
    scrollable_label_button_frame.remove_item(item)
    newwindow.destroy()
    newwindow.update()


def showPassword(item):
    newwindow = ctk.CTkToplevel()
    newwindow.geometry('200x200')
    newwindow.title('Password')
    text = "Username: " + item[1] + '\n Password: ' + item[2]
    newlabel = ctk.CTkLabel(master=newwindow, text=text)
    newlabel.pack(padx=20, pady=20)

    # Delete Record
    delbutton = ctk.CTkButton(master=newwindow, text='Delete Record',
                              command=partial(deleteRecords, item[0], newwindow))
    delbutton.pack(padx=20, pady=20)


def addRecordGUI():
    newwindow = ctk.CTkToplevel()
    newwindow.geometry('200x200')
    newwindow.title('New Record')
    name_entry = ctk.CTkEntry(master=newwindow, placeholder_text='Name')
    user_entry = ctk.CTkEntry(master=newwindow, placeholder_text='Username')
    passwd_entry = ctk.CTkEntry(master=newwindow, placeholder_text='Password')
    addbutton = ctk.CTkButton(master=newwindow, text='Add Record',
                              command=partial(addRecord, name_entry, user_entry, passwd_entry, newwindow))
    name_entry.pack(padx=3, pady=3)
    user_entry.pack(padx=3, pady=3)
    passwd_entry.pack(padx=3, pady=3)
    addbutton.pack(padx=3, pady=3)


def addRecord(name, user, passwd, newwindow):
    i = [name.get(), user.get(), passwd.get()]
    EPM.addPassword(i[0], i[1], i[2])
    scrollable_label_button_frame.add_item(i[0], i)
    newwindow.destroy()
    newwindow.update()


# Login Page
label = ctk.CTkLabel(master=frame, text='Login')
user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
button = ctk.CTkButton(master=frame, text='Login', command=Guilogin)
wrongpassword = ctk.CTkLabel(master=frame, text='Wrong Password or Username', text_color='red')

# Record Page
scrollable_label_button_frame = ScrollableLabelButtonFrame(master=app, width=300, height=300, corner_radius=10)
addbutton = ctk.CTkButton(master=app, text='Add Record', command=addRecordGUI)
login_page = ctk.CTkButton(master=app, text='Back to Login', command=backtologin)
# scrollable_label_button_frame.pack(padx=10, pady=10)

# Initializing
label.pack(pady=12, padx=10)
user_entry.pack(pady=12, padx=10)
user_pass.pack(pady=12, padx=10)
frame.pack(pady=20, padx=40, fill='both', expand=True)
button.pack(pady=12, padx=10)

app.mainloop()
