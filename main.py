import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip




# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


    password_list = []

    for char in range(random.randint(8, 10)):
        password_list.append(random.choice(letters))

    for char in range(random.randint(2, 4)):
        password_list += random.choice(symbols)

    for char in range(random.randint(2, 4)):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = ""
    password="".join(password_list)
    password_entry.delete(0,END)
    password_entry.insert(0,password)
    return password

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    data_dict = {
        website : {
            'email' : username ,
            'password' : password

        }

    }
    if len(website) ==0 or len(username) == 0 or len(password) ==0 :
        messagebox.showwarning('ERROR' , message="Please don't leave any fields empty" )

    else :
        is_okay = messagebox.askokcancel(title = website , message=f"These are the details entered : \n Username/Email : {username} , \nPassword : {password} \n Is this ok to save ?")

        if is_okay :
            try :
                with open('data.json', mode='r') as data_file :
                    data = json.load(data_file)

            except FileNotFoundError :
                with open('data.json', 'w') as data_file :
                    json.dump(data_dict ,data_file, indent=4)
            else :

                data.update(data_dict)
                with open('data.json' , 'w') as data_file :

                    json.dump(data,data_file , indent=4)

            finally :
                username_entry.delete(0,END)
                password_entry.delete(0, END)
                website_entry.delete(0, END)
                pyperclip.copy(password)

#------------------------------SEARCH---------------------------------------#
def search() :
    try :
        with open('data.json' , 'r') as data_file :
            search_parameter = website_entry.get()
            data = json.load(data_file)
    except FileNotFoundError :
        messagebox.showwarning('ERROR' , message='No Data File Found')

    else :
        if search_parameter in data :
            password= data[search_parameter]["password"]
            messagebox.showinfo(f'Password for {search_parameter}', message=f"The password for {search_parameter} is : \n {password}")
        else :
            messagebox.showinfo('ERROR',message=f'The password for {search_parameter} has not been saved ')
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('PassWord Manager')

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file='logo.png')
canvas.create_image(100,100,image=logo)
window.config(padx=20, pady=20)
canvas.grid(row=0,column=1)

website_label = Label(text='Website :', padx=5 , pady=5)
website_label.grid(row=1,column=0)

username_label = Label(text='Username/Email :',padx=5, pady=5)
username_label.grid(row=2,column=0)

password_label = Label(text='Password :',padx=5 , pady=5)
password_label.grid(row=3,column=0)


website_entry = Entry(width=55)
website_entry.grid(row = 1 , column=1 , columnspan=2)

username_entry = Entry(width=55)
username_entry.grid(row=2,column=1,columnspan=2)

password_entry = Entry(width=35)
password_entry.grid(row=3,column=1)

generate_password = Button(text='Generate Password',command=generate)

generate_password.grid(row=3 , column=2)

add = Button(text='Add',width=45 , command=save)
add.grid(row=4,column=1, columnspan=2)


search = Button(text='Search',width=15, command = search)
search.grid(row=1,column=2)

window.mainloop()