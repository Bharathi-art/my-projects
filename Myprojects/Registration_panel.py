import tkinter as tk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import face_recognition

# Function to check if all fields are filled and enable/disable register button accordingly
def check_fields():
    if all(entry.get() for entry in (roll_number_entry, student_name_entry, phone_number_entry)):
        register_pic_button.config(state="normal")
    else:
        register_pic_button.config(state="disabled")

# Function to enable the register button
def enable_register_button():
    register_button.config(state="normal")

def register():
    roll_number = roll_number_entry.get()
    student_name = student_name_entry.get()
    phone_number = phone_number_entry.get()
    
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="student_attendance_records"
    )

    mycursor = mydb.cursor()

    # Insert data into the database
    sql = "INSERT INTO student_registration (Roll_number, Student_name, Phone_number) VALUES (%s, %s, %s)"
    val = (roll_number, student_name, phone_number)
    mycursor.execute(sql, val)

    mydb.commit()

    messagebox.showinfo("Success", "Registration successful!")
    root.destroy()  # Close the registration panel after registration is successful

def register_with_pic():
    student_name = student_name_entry.get()
    photo_dir = "C:/Users/bhara/OneDrive/Desktop/photo"
    image_path = os.path.join(photo_dir, f"{student_name}.jpg")

    # Check if image already exists
    if os.path.isfile(image_path):
        messagebox.showerror("Error", "Image already exists for this student.")
        return

    # Connect to camera
    cap = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open camera")
        return

    # Load face recognition model
    known_face_encodings = []
    known_face_names = []
    for file in os.listdir(photo_dir):
        if file.endswith(".jpg"):
            image = face_recognition.load_image_file(os.path.join(photo_dir, file))
            encoding = face_recognition.face_encodings(image)
            if encoding:
                known_face_encodings.append(encoding[0])
                known_face_names.append(os.path.splitext(file)[0])

    # Loop until face is detected
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert frame to RGB (required by face_recognition library)
        rgb_frame = frame[:, :, ::-1]

        # Find all face locations and encodings in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Draw rectangle around detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Check if any face is detected
        if len(face_encodings) > 0:
            # Compare face encodings with known faces
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                if True in matches:
                    messagebox.showinfo("Already Registered", "You are already registered with a picture.")
                    cap.release()
                    cv2.destroyAllWindows()
                    return

        # Display the frame
        cv2.imshow("Camera", frame)

        # Wait for 'r' key to be pressed
        key = cv2.waitKey(1)
        if key == ord('r'):
            # Save the captured frame as an image
            cv2.imwrite(image_path, frame)
            messagebox.showinfo("Success", "Picture captured and saved successfully")
            enable_register_button()  # Enable register button after picture is taken
            break

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Enable register button after the image is taken and saved
    enable_register_button()

root = tk.Tk()
root.title("Student Registration")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window width and height
window_width = 450
window_height = 400

# Calculate x and y position for centering window
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Set window size and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Background color
root.configure(bg="grey")

# Create labels and entry fields with padding
padx_value = 10
pady_value = 5

# Custom font
font_style = ("Arial", 12)

roll_number_label = tk.Label(root, text="Roll Number:", bg="grey", fg="white", font=font_style)
roll_number_label.grid(row=0, column=0, padx=padx_value, pady=pady_value)
roll_number_entry = tk.Entry(root, width=40, bd=2, font=font_style)
roll_number_entry.grid(row=0, column=1, padx=padx_value, pady=pady_value)
roll_number_entry.bind("<KeyRelease>", lambda event: check_fields())

student_name_label = tk.Label(root, text="Student Name:", bg="grey", fg="white", font=font_style)
student_name_label.grid(row=1, column=0, padx=padx_value, pady=pady_value)
student_name_entry = tk.Entry(root, width=40, bd=2, font=font_style)
student_name_entry.grid(row=1, column=1, padx=padx_value, pady=pady_value)
student_name_entry.bind("<KeyRelease>", lambda event: check_fields())

phone_number_label = tk.Label(root, text="Phone Number:", bg="grey", fg="white", font=font_style)
phone_number_label.grid(row=2, column=0, padx=padx_value, pady=pady_value)
phone_number_entry = tk.Entry(root, width=40, bd=2, font=font_style)
phone_number_entry.grid(row=2, column=1, padx=padx_value, pady=pady_value)
phone_number_entry.bind("<KeyRelease>", lambda event: check_fields())

register_pic_button = tk.Button(root, text="Register with Picture (Press 'r')", command=register_with_pic, bg="orange", font=font_style, state="disabled")
register_pic_button.grid(row=3, columnspan=2, padx=padx_value, pady=pady_value)

# Initially disable the Register button
register_button = tk.Button(root, text="Register", command=register, bg="lightgreen", font=font_style, state="disabled")
register_button.grid(row=4, columnspan=2, padx=padx_value, pady=pady_value)

# Ensure the photo directory exists
photo_dir = "C:/Users/bhara/OneDrive/Desktop/photo"
os.makedirs(photo_dir, exist_ok=True)

root.mainloop()
