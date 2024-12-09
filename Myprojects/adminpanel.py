import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import subprocess
import os

# Define tree as a global variable
tree = None

def mark_attendance():
    subprocess.run(["python", "MarkAttendance.py"])
    messagebox.showinfo("Attendance Marked", "Attendance marked successfully!")

def show_attendance_list():
    global tree  # Access the global variable

    def close_attendance_window():
        attendance_window.destroy()

    def edit_record(record_id):
        selected_item = tree.focus()
        if selected_item:
            data = tree.item(selected_item)['values']
            edit_window = tk.Toplevel(root)
            edit_window.title("Edit Record")

            labels = ["ID", "Roll Number", "Student Name", "Phone Number", "Attendance Date", "Attendance Time"]
            entries = []
            for i, label in enumerate(labels):
                tk.Label(edit_window, text=label).grid(row=i, column=0, padx=5, pady=5)
                entry = tk.Entry(edit_window)
                entry.insert(0, data[i])
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)

            def update_record():
                try:
                    connection = mysql.connector.connect(host='localhost',
                                                         database='student_attendance_records',
                                                         user='root',
                                                         password='')
                    if connection.is_connected():
                        cursor = connection.cursor()
                        update_query = """UPDATE student_attendance_records 
                                          SET roll_number = %s, student_name = %s, phone_number = %s, 
                                              attendance_date = %s, attendance_time = %s
                                          WHERE id = %s"""
                        updated_data = [entry.get() for entry in entries[1:]] + [data[0]]
                        cursor.execute(update_query, updated_data)
                        connection.commit()
                        messagebox.showinfo("Success", "Record updated successfully!")
                        edit_window.destroy()
                        show_attendance_list()
                    else:
                        messagebox.showerror("Database Error", "Failed to connect to the database.")
                except Error as e:
                    messagebox.showerror("Database Error", f"Error updating record: {e}")
                finally:
                    if 'connection' in locals() and connection.is_connected():
                        cursor.close()
                        connection.close()

            tk.Button(edit_window, text="Update", command=update_record).grid(row=len(labels), column=0, columnspan=2, padx=5, pady=10)

    def delete_record(record_id):
        selected_item = tree.focus()
        if selected_item:
            confirmation = messagebox.askokcancel("Confirmation", "Are you sure you want to delete this record?")
            if confirmation:
                try:
                    connection = mysql.connector.connect(host='localhost',
                                                         database='student_attendance_records',
                                                         user='root',
                                                         password='')
                    if connection.is_connected():
                        cursor = connection.cursor()
                        record_id = tree.item(selected_item)['values'][0]
                        delete_query = "DELETE FROM student_attendance_records WHERE id = %s"
                        cursor.execute(delete_query, (record_id,))
                        connection.commit()
                        messagebox.showinfo("Success", "Record deleted successfully!")
                        show_attendance_list()
                    else:
                        messagebox.showerror("Database Error", "Failed to connect to the database.")
                except Error as e:
                    messagebox.showerror("Database Error", f"Error deleting record: {e}")
                finally:
                    if 'connection' in locals() and connection.is_connected():
                        cursor.close()
                        connection.close()

    def checkbox_selection(event):
        selected_item = tree.focus()
        if selected_item:
            tree.selection_toggle(selected_item)

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='student_attendance_records',
                                             user='root',
                                             password='')
        if connection.is_connected():
            cursor = connection.cursor()

            sql_select_query = """SELECT id, roll_number, student_name, phone_number, attendance_date, attendance_time FROM student_attendance_records"""
            cursor.execute(sql_select_query)
            records = cursor.fetchall()

            if records:
                attendance_window = tk.Toplevel(root)
                attendance_window.title("Attendance List")

                tree = ttk.Treeview(attendance_window)
                tree["columns"] = ("ID", "Roll Number", "Student Name", "Phone Number", "Attendance Date", "Attendance Time")

                tree.heading("#0", text="", anchor=tk.CENTER)
                tree.heading("ID", text="ID", anchor=tk.CENTER)
                tree.heading("Roll Number", text="Roll Number", anchor=tk.CENTER)
                tree.heading("Student Name", text="Student Name", anchor=tk.CENTER)
                tree.heading("Phone Number", text="Phone Number", anchor=tk.CENTER)
                tree.heading("Attendance Date", text="Attendance Date", anchor=tk.CENTER)
                tree.heading("Attendance Time", text="Attendance Time", anchor=tk.CENTER)

                tree.column("#0", width=0, stretch=tk.NO)
                tree.column("ID", width=100, anchor=tk.CENTER)
                tree.column("Roll Number", width=100, anchor=tk.CENTER)
                tree.column("Student Name", width=200, anchor=tk.CENTER)
                tree.column("Phone Number", width=150, anchor=tk.CENTER)
                tree.column("Attendance Date", width=150, anchor=tk.CENTER)
                tree.column("Attendance Time", width=150, anchor=tk.CENTER)

                for record in records:
                    tree.insert("", tk.END, values=record)

                tree.pack(fill="both", expand=True)

                button_frame = tk.Frame(attendance_window)
                button_frame.pack(pady=10)

                close_button = tk.Button(button_frame, text="Close", command=close_attendance_window, bg="red", fg="black")
                close_button.pack(side=tk.LEFT, padx=5)

                edit_button = tk.Button(button_frame, text="Edit", command=lambda: edit_record(tree.selection()), bg="orange", fg="black")
                edit_button.pack(side=tk.LEFT, padx=5)

                delete_button = tk.Button(button_frame, text="Delete", command=lambda: delete_record(tree.selection()), bg="dark green", fg="black")
                delete_button.pack(side=tk.LEFT, padx=5)

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

def open_registration_panel():
    subprocess.run(["python", "Registration_panel.py"])
    messagebox.showinfo("Registration", "Register successfully!")
    registration_window = tk.Toplevel(root)
    registration_window.withdraw()
    registration_window.update()
    messagebox.showinfo("Registration", "Register successfully!")
    registration_window.destroy()

def logout():
    root.destroy()
    os.system("python mainpanel.py")

root = tk.Tk()
root.title("Face Recognition Attendance System")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}+0+0")
root.configure(bg="#f0f0f0")

mark_attendance_img = Image.open(r"C:\Users\bhara\OneDrive\Documents\python\mark attendance.jpg")
mark_attendance_img.thumbnail((200, 200))
mark_attendance_img = ImageTk.PhotoImage(mark_attendance_img)

store_registration_img = Image.open(r"C:\Users\bhara\OneDrive\Documents\python\new register.jpg")
store_registration_img.thumbnail((200, 200))
store_registration_img = ImageTk.PhotoImage(store_registration_img)

show_attendance_list_img = Image.open(r"C:\Users\bhara\OneDrive\Documents\python\view attendance list.png")
show_attendance_list_img.thumbnail((200, 200))
show_attendance_list_img = ImageTk.PhotoImage(show_attendance_list_img)

logout_button = tk.Button(root, text="Logout", command=logout,bg="Red", fg="black")
logout_button.pack(anchor=tk.NE, padx=90, pady=10)

panel = tk.Frame(root, bg="#ffffff")
panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

mark_attendance_button = tk.Button(panel, image=mark_attendance_img, command=mark_attendance)
mark_attendance_button.grid(row=0, column=0, padx=20, pady=20)
mark_attendance_label = tk.Label(panel, text="Mark Attendance", font=("Helvetica", 12))
mark_attendance_label.grid(row=1, column=0, pady=(0, 20))

store_registration_button = tk.Button(panel, image=store_registration_img, command=open_registration_panel)
store_registration_button.grid(row=0, column=1, padx=20, pady=20)
store_registration_label = tk.Label(panel, text="Store Registration", font=("Helvetica", 12))
store_registration_label.grid(row=1, column=1, pady=(0, 20))

show_attendance_list_button = tk.Button(panel, image=show_attendance_list_img, command=show_attendance_list)
show_attendance_list_button.grid(row=0, column=2, padx=20, pady=20)
show_attendance_list_label = tk.Label(panel, text="Show Attendance List", font=("Helvetica", 12))
show_attendance_list_label.grid(row=1, column=2, pady=(0, 20))

root.mainloop()
