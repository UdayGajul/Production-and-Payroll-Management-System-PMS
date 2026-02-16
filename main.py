# Import the Tkinter module and alias it as "tk"
import tkinter as tk

# Import messagebox for popup messages
from tkinter import messagebox, simpledialog

# Import the Image, ImageTk from the Pillow module for working with images
from PIL import Image, ImageTk

# Import Subprocess for redirecting to new page
import subprocess

# Importing the ttkbootstrap for better UI
from ttkbootstrap.constants import *
from ttkbootstrap import Style
import ttkbootstrap as tb
import json
import sys, os


def open_first_page(num=None):
    # --==--== old code --==--==
    # entered_password = password_entry.get() # Check the entered password is correct or not
    # if entered_password == password:
    #     try:
    #         subprocess.Popen(["python", "PPMS.py"])
    #         root.destroy() # Close the current window after opening the new one
    #     except Exception as ex:
    #         messagebox.showerror("Oops!", str(ex))
    # --==--== new code --==--==
    entered_password = password_entry.get()
    if entered_password == password:
        try:
            # Check if running as EXE or Python script
            if getattr(sys, "frozen", False):
                # Running as EXE - launch PPMS.exe
                pms_path = os.path.join(os.path.dirname(sys.executable), "PPMS.exe")
                subprocess.Popen([pms_path])
            else:
                # Running as Python script - launch PPMS.py
                subprocess.Popen(["python", "PPMS.py"])
            root.destroy()
        except Exception as ex:
            messagebox.showerror("Oops!", str(ex))
    else:
        # Show invalid password popup
        messagebox.showerror(
            "Invalid Password", "Maybe only authentic Gajul's possess the secret code!"
        )


# Function to change the password
def change_password():
    global password

    # Prompt the user for the old password
    old_password = simpledialog.askstring(
        "Change Password", "Enter Old Password:", parent=root
    )
    if old_password != password:
        messagebox.showerror("Invalid Password", "Old password is incorrect.")
        return

    # Prompt the user for the new password
    new_password = simpledialog.askstring(
        "Change Password", "Enter new password:", parent=root
    )
    if new_password:
        password = new_password
        # Save the new password to a file
        with open("password.json", "w") as file:
            json.dump({"password": password}, file)
        messagebox.showinfo(
            "Password Changed", "Password has been successfully changed."
        )


# Function to load the password from file
def load_password():
    try:
        with open("password.json", "r") as file:
            data = json.load(file)
            return data["password"]
    except FileNotFoundError:
        # Default password if the file doesn't exist
        return "up"


# Create the main Tkinter window
root = tk.Tk()

# Apply 'superhero' theme
style = Style(theme="superhero")

# Give the title for your project
root.title("Production Management System")
# Set the geometry of the window
root.geometry("1440x900")  # This could be useful after Restoring Down
# Give the fix size of the window
root.state("zoomed")
# Set the icon
root.iconbitmap("images/favicon.ico")

# Dynamic Title inside the window
txt = "Step into Gajul Fabrics - Your Welcome!"
count = 0
text1 = ""
title_label = tk.Label(root, text=txt, font=("Garamond", 50, "bold"))
title_label.pack()


def slider():
    global count, text1
    if count >= len(txt):
        count = -1
        text1 = ""
        title_label.config(text=text1)
    else:
        text1 = text1 + txt[count]
        title_label.config(text=text1)
    count += 1
    title_label.after(150, slider)


slider()

# Load password from file
password = load_password()

# Load and display the image
image_path = "images/android-chrome-512x512.png"
img = Image.open(image_path)
img = img.resize((300, 300))
img = ImageTk.PhotoImage(img)
# Creating the label to hold the image
image_label = tk.Label(root, image=img)
image_label.image = img
image_label.pack(pady=20)  # Display widget within a container

# Add Password label
password_label = tk.Label(
    root, text="Only true Gajul's holds the key to the word.", font=("Garamond, 16")
)
password_label.pack()

# Add textbox or password entry
password_entry = tk.Entry(root, show="•", font=("Garamond", 16), justify=CENTER)
password_entry.pack(pady=10)

# Creating the button that is going to open 1st Page
next_page_button = tk.Button(
    root,
    text="Let's Start!",
    command=open_first_page,
    font=("Garamond", 20, "bold"),
    height=2,
    width=12,
    cursor="hand2",
)
next_page_button.pack(pady=30)  # Display widget within a container

# For enter button
root.bind("<Return>", open_first_page)

# Creating the button that'll change the password
change_password_button = tb.Button(
    root, text="Change Password", bootstyle=("link"), command=change_password
)
change_password_button.pack(pady=10)


# Function for forgot password
def forgot_password():
    # Ask the user a security question
    security_question = "Whom do you love the most in the world?"
    answer = simpledialog.askstring("Forgot Password", security_question, parent=root)
    try:
        # Check if the answer matches the expected answer
        if answer.lower() == "suvarna":
            # If the answer is correct, show the current password
            current_password = load_password()
            messagebox.showinfo(
                "Forgot Password", f"Your current password is: {current_password}"
            )
        else:
            # If the answer is incorrect, show an error message
            messagebox.showerror("Oops!", "Incorrect answer to security question")
    except Exception:
        pass


# Creating the button for forget password
forgot_password_button = tb.Button(
    root, text="Forgot Password", bootstyle=("link"), command=forgot_password
)
forgot_password_button.pack()


def exit_window():
    root.quit()


exit_button = tk.Button(
    root,
    text="Exit",
    command=exit_window,
    font=("Garamond", 15, "bold"),
    height=1,
    width=6,
    cursor="hand2",
)
exit_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
