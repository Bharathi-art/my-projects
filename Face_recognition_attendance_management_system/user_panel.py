import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import os

# Global variable to store the username of the currently logged-in user
current_user = None

def show_attendance_list():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='student_attendance_records',
                                             user='root',
                                             password='')
        if connection.is_connected():
            cursor = connection.cursor()

            # Retrieve attendance records from the database
            sql_select_query = """SELECT id, roll_number, student_name, phone_number, attendance_date, attendance_time FROM student_attendance_records"""
            cursor.execute(sql_select_query)
            records = cursor.fetchall()

            if records:
                # Create a new window to display attendance records
                attendance_window = tk.Toplevel(root)
                attendance_window.title("Attendance List")
                
                # Create a Treeview widget
                tree = ttk.Treeview(attendance_window)
                tree["columns"] = ("ID", "Roll Number", "Student Name", "Phone Number", "Attendance Date", "Attendance Time")
                
                # Set column headings
                tree.heading("#0", text="", anchor=tk.CENTER)
                tree.heading("ID", text="ID", anchor=tk.CENTER)
                tree.heading("Roll Number", text="Roll Number", anchor=tk.CENTER)
                tree.heading("Student Name", text="Student Name", anchor=tk.CENTER)
                tree.heading("Phone Number", text="Phone Number", anchor=tk.CENTER)
                tree.heading("Attendance Date", text="Attendance Date", anchor=tk.CENTER)
                tree.heading("Attendance Time", text="Attendance Time", anchor=tk.CENTER)

                # Set column widths
                tree.column("#0", width=0, stretch=tk.NO)
                tree.column("ID", width=100, anchor=tk.CENTER)
                tree.column("Roll Number", width=100, anchor=tk.CENTER)
                tree.column("Student Name", width=200, anchor=tk.CENTER)
                tree.column("Phone Number", width=150, anchor=tk.CENTER)
                tree.column("Attendance Date", width=150, anchor=tk.CENTER)
                tree.column("Attendance Time", width=150, anchor=tk.CENTER)
                
                # Insert attendance records into the Treeview
                for i, record in enumerate(records, start=1):
                    tree.insert("", tk.END, text=str(i), values=record)
                
                tree.pack(fill="both", expand=True)

                # Close button
                close_button = tk.Button(attendance_window, text="Close", command=attendance_window.destroy, bg="red", fg="black")
                close_button.pack(side="bottom", pady=10)
            else:
                messagebox.showinfo("Attendance List", "No attendance records found.")
        else:
            messagebox.showerror("Database Error", "Failed to connect to the database.")
    except Error as e:
        messagebox.showerror("Database Error", f"Error while retrieving attendance records: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def open_request_page():
    # Function to open request page
    request_window = tk.Toplevel(root)
    request_window.title("Request Page")
    request_window.geometry("400x450")  # Set the size to 400x450

    # Title label for request page
    title_label = tk.Label(request_window, text="Request Page", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=(10, 20))

    # Request field with a larger input box
    request_field = tk.Text(request_window, height=10, width=50, bd=2, relief=tk.SOLID)
    request_field.pack(pady=(0, 10))

    # Submit button with green background and black text color
    submit_button = tk.Button(request_window, text="Submit", command=lambda: submit_request(request_field.get("1.0", "end-1c")), bg="#00FF00", fg="#000000")
    submit_button.pack()
def logout():
    root.destroy()  # Close the current window
    os.system("python mainpanel.py")  # Execute the mainpanel.py


def submit_request(request_text):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='student_attendance_records',
                                             user='root',
                                             password='')
        if connection.is_connected():
            cursor = connection.cursor()

            # Prepare the INSERT query
            sql_insert_query = """INSERT INTO student_registration (username, request) VALUES (%s, %s)"""
            cursor.execute(sql_insert_query, (current_user, request_text,))
            connection.commit()
            messagebox.showinfo("Success", "Request submitted successfully!")
    except Error as e:
        messagebox.showerror("Database Error", f"Error while submitting request: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

# Create Tkinter window
root = tk.Tk()
root.title("Student Panel")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size and position
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Title label
title_label = tk.Label(root, text="Student panel", font=("Helvetica", 16, "bold"))
title_label.pack(pady=(10, 20))

# Create big panel
panel = tk.Frame(root, bg="#ffffff")
panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

show_attendance_list_img = Image.open(r"C:\Users\bhara\OneDrive\Desktop\python\view attendance list.png")
show_attendance_list_img.thumbnail((200, 200))
show_attendance_list_img = ImageTk.PhotoImage(show_attendance_list_img)

# Show Attendance List button and icon
show_attendance_list_button = tk.Button(panel, image=show_attendance_list_img, command=show_attendance_list)
show_attendance_list_button.grid(row=0, column=2, padx=20, pady=20)
show_attendance_list_label = tk.Label(panel, text="Show Attendance List", font=("Helvetica", 12))
show_attendance_list_label.grid(row=1, column=2, pady=(0, 20))

# Logout button
logout_button = tk.Button(root, text="Logout", command=logout,bg="Red", fg="black")
logout_button.pack(anchor=tk.NE, padx=90, pady=10)

root.mainloop()
