from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    my_password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_list = [choice(letters) for _ in range(randint(8, 10))]
    symbols_list = [choice(symbols) for _ in range(randint(2, 4))]
    numbers_list = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = letters_list + symbols_list + numbers_list
    shuffle(password_list)

    password = "".join(password_list)
    my_password_entry.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website_info = my_website_entry.get()
    email_info = my_email_entry.get()
    password_info = my_password_entry.get()

    new_data = {
        website_info: {
            "Email": email_info,
            "Password": password_info,
        },
    }

    if len(website_info) == 0 or len(password_info) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            my_website_entry.delete(0, END)
            my_password_entry.delete(0, END)
            my_website_entry.focus()


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    website = my_website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo("Error", "No data file found.")
    else:
        if website in data:
            messagebox.showinfo(website, f"Email: {data[website]['Email']}\n Password: {data[website]['Password']}")
        else:
            messagebox.showinfo("Error", f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

my_logo = PhotoImage(file="logo.png")

my_canvas = Canvas(width=200, height=200)
my_canvas.create_image(100, 100, image=my_logo)
my_canvas.grid(column=1, row=0)

# Labels
my_website = Label(text="Website:")
my_website.config(padx=10, pady=10)
my_website.grid(column=0, row=1)

my_email = Label(text="Email/Username:")
my_email.config(padx=10, pady=10)
my_email.grid(column=0, row=2)

my_password = Label(text="Password:")
my_password.config(padx=10, pady=10)
my_password.grid(column=0, row=3)

# Entries
my_website_entry = Entry(width=33)
my_website_entry.focus()
my_website_entry.grid(column=1, row=1)

my_email_entry = Entry(width=53)
my_email_entry.insert(0, "dummy_email@gmail.com")
my_email_entry.grid(column=1, row=2, columnspan=2)

my_password_entry = Entry(width=33)
my_password_entry.grid(column=1, row=3)

# Buttons
my_search = Button(text="Search", width=15, command=find_password)
my_search.grid(column=2, row=1)

my_generate = Button(text="Generate Password", command=generate_password)
my_generate.grid(column=2, row=3)

my_add = Button(text="Add", width=45, command=save)
my_add.grid(column=1, row=4, columnspan=2)

window.mainloop()
