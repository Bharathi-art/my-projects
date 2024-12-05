import tkinter as tk
from tkinter import messagebox
import mysql.connector
import os

def admin_login():
    username = username_var.get()
    password = password_var.get()

    # Show loading message
    loading_var.set("Logging in...")

    # Connect to MySQL
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='student_attendance_records',
            user='root',
            password=''
        )
        
        cursor = conn.cursor()

        # Execute query to check admin credentials
        query = "SELECT * FROM admin_login WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            if result[1] == password:
                messagebox.showinfo("Admin Login", "Login Successful")
                # Execute the Python script upon successful login
                os.system('python adminpanel.py')
                root.destroy()  # Close the login window
            else:
                messagebox.showerror("Admin Login", "Incorrect Password")
        else:
            messagebox.showerror("Admin Login", "Username not found")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Admin Login", f"Database Error: {err}")

    # Reset loading message
    loading_var.set("")

# Create Tkinter window
root = tk.Tk()
root.title("Admin Login")

# Calculate the window position to center it on a 14.5-inch screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 400
window_height = 450
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create frame to hold login interface
login_frame = tk.Frame(root, bg="#f0f0f0")
login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# StringVars for username and password
username_var = tk.StringVar()
password_var = tk.StringVar()

# Username label and entry
username_label = tk.Label(login_frame, text="Username:", bg="#f0f0f0", font=("Helvetica", 14))
username_label.grid(row=0, column=0, padx=10, pady=(20, 5))
username_entry = tk.Entry(login_frame, textvariable=username_var, font=("Helvetica", 14))
username_entry.grid(row=0, column=1, padx=10, pady=(20, 5))

# Password label and entry
password_label = tk.Label(login_frame, text="Password:", bg="#f0f0f0", font=("Helvetica", 14))
password_label.grid(row=1, column=0, padx=10, pady=(5, 5))
password_entry = tk.Entry(login_frame, textvariable=password_var, show="*", font=("Helvetica", 14))
password_entry.grid(row=1, column=1, padx=10, pady=(5, 5))

# Login button
login_button = tk.Button(login_frame, text="Login", command=admin_login, bg="#4CAF50", fg="white", font=("Helvetica", 14))
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=(5, 20))

# Label for loading message
loading_var = tk.StringVar()
loading_label = tk.Label(login_frame, textvariable=loading_var, bg="#f0f0f0", font=("Helvetica", 14))
loading_label.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 20))

root.mainloop()
