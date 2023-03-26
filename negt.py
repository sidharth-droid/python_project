import tkinter as tk
import random
from cryptography.fernet import Fernet
import os


l = os.listdir()
if "k.key" not in l:
    with open("k.key", "wb") as f:
        a = Fernet.generate_key()
        f.write(a)
with open("k.key", "rb") as f:
    fernet = Fernet(f.read())

root = tk.Tk()
root.title("Password Manager")


def add_password():

    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    encrypted_password = fernet.encrypt(password.encode())

    with open("passwords.txt", "a") as file:
        file.write(website + " " + username + " " +
                   encrypted_password.decode() + "\n")

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


def get_password():
    website = website_entry.get()
    username = username_entry.get()
    try:
        with open("passwords.txt", "r") as file:
            lines = file.readlines()

        for line in lines:
            parts = line.split()
            if len(parts) == 3:
                stored_website, stored_username, stored_password = parts
                if website == stored_website and username == stored_username:
                    decrypted_password = fernet.decrypt(
                        stored_password.encode()).decode()
                    password_entry.delete(0, tk.END)
                    password_entry.insert(0, decrypted_password)
                    break
        else:
            password_entry.delete(0, tk.END)
            password_entry.insert(0, "Password not found")
    except:
        password_entry.delete(0, tk.END)
        password_entry.insert(0, "Password not found!")


def delete_password():
    website = website_entry.get()
    username = username_entry.get()

    with open("passwords.txt", "r") as file:
        lines = file.readlines()

    with open("passwords.txt", "w") as file:
        for line in lines:
            parts = line.split()
            if len(parts) == 3:
                stored_website, stored_username, stored_password = parts
                if not (website == stored_website and username == stored_username):
                    file.write(line)

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


def generate_password():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-="
    password = "".join(random.choice(chars) for i in range(12))

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


tk.Label(root, text="Website:").grid(row=0, column=0)
website_entry = tk.Entry(root)
website_entry.grid(row=0, column=1)

tk.Label(root, text="Username:").grid(row=1, column=0)
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1)

tk.Label(root, text="Password:").grid(row=2, column=0)
password_entry = tk.Entry(root)
password_entry.grid(row=2, column=1)

add_button = tk.Button(root, text="Add Password", command=add_password)
add_button.grid(row=3, column=0)

get_button = tk.Button(root, text="Get Password", command=get_password)
get_button.grid(row=3, column=1)

delete_button = tk.Button(
    root, text="Delete Password", command=delete_password)
delete_button.grid(row=3, column=2)

generate_button = tk.Button(
    root, text="Generate Password", command=generate_password)
generate_button.grid(row=4, column=1)
root.mainloop()
