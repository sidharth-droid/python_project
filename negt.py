import tkinter as tk
import random
from cryptography.fernet import Fernet


# with open("k.key","wb") as f:
#     a = Fernet.generate_key()
#     f.write(a)
with open("k.key","rb") as f:
    fernet = Fernet(f.read())

# create a tkinter window
root = tk.Tk()
root.title("Password Manager")

# function to add a new password
def add_password():
    # get the website, username, and password from the user
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    # encrypt the password
    encrypted_password = fernet.encrypt(password.encode())

    # write the website, username, and encrypted password to a text file
    with open("passwords.txt", "a") as file:
        file.write(website + " " + username + " " + encrypted_password.decode() + "\n")

    # clear the input fields
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# function to retrieve a password
def get_password():
    # get the website and username from the user
    website = website_entry.get()
    username = username_entry.get()

    # read the passwords from the text file
    with open("passwords.txt", "r") as file:
        lines = file.readlines()

    # loop through the lines and find the matching website and username
    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            stored_website, stored_username, stored_password = parts
            if website == stored_website and username == stored_username:
                # decrypt the password and display it
                decrypted_password = fernet.decrypt(stored_password.encode()).decode()
                password_entry.delete(0, tk.END)
                password_entry.insert(0, decrypted_password)
                break
    else:
        # if no matching website and username is found, display an error message
        password_entry.delete(0, tk.END)
        password_entry.insert(0, "Password not found")

# function to delete a password
def delete_password():
    # get the website and username from the user
    website = website_entry.get()
    username = username_entry.get()

    # read the passwords from the text file
    with open("passwords.txt", "r") as file:
        lines = file.readlines()

    # open the text file for writing
    with open("passwords.txt", "w") as file:
        # loop through the lines and write them to the file, except for the matching website and username
        for line in lines:
            parts = line.split()
            if len(parts) == 3:
                stored_website, stored_username, stored_password = parts
                if not (website == stored_website and username == stored_username):
                    file.write(line)

    # clear the input fields
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# function to generate a new password
def generate_password():
    # generate a random password of length 12
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-="
    password = "".join(random.choice(chars) for i in range(12))

    # display the new password
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# create the
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

delete_button = tk.Button(root, text="Delete Password", command=delete_password)
delete_button.grid(row=3, column=2)

generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.grid(row=4, column=1)
root.mainloop()