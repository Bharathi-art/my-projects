import mysql.connector
from mysql.connector import Error
import os
import face_recognition
import cv2
import pandas as pd
from datetime import datetime

def load_images_from_folder(folder_path):
    image_paths = []
    known_face_encodings = {}
    known_face_names = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            name = os.path.splitext(filename)[0]
            image_path = os.path.join(folder_path, filename)
            image_paths.append(image_path)
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            if len(face_encodings) > 0:
                encoding = face_encodings[0]  # Take the first face encoding if multiple faces are detected
                known_face_encodings[name] = encoding
                known_face_names.append(name)
            else:
                print(f"No face detected in {filename}")

    return known_face_names, known_face_encodings, image_paths

def fetch_student_details():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='student_attendance_records',
                                             user='root',
                                             password='')

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT Roll_number, Student_name, Phone_number FROM student_registration")
            records = cursor.fetchall()
            student_details = {record['Student_name']: {'Roll_number': record['Roll_number'], 'Phone_number': record['Phone_number']} for record in records}
            return student_details

    except Error as e:
        print("Error while connecting to MySQL", e)
        return None
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def record_attendance(name, roll_number, phone_number, attendance_date, attendance_time, connection):
    try:
        if connection.is_connected():
            cursor = connection.cursor()

            sql_insert_query = """INSERT INTO student_attendance_records (Roll_Number, Student_name, Phone_Number, Attendance_date, Attendance_time) 
                                  VALUES (%s, %s, %s, %s, %s)"""
            insert_tuple = (roll_number, name, phone_number, attendance_date, attendance_time)
            cursor.execute(sql_insert_query, insert_tuple)
            connection.commit()
            print("Record inserted successfully into student_attendance_records table")

    except Error as e:
        print("Error while inserting record:", e)

def export_to_excel(records):
    if not records:
        print("No attendance records to export.")
        return

    try:
        df = pd.DataFrame(records)
        filename = f"attendance_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        df.to_excel(writer, index=False)
        
        # Adjust column widths
        worksheet = writer.sheets['Sheet1']
        for i, col in enumerate(df.columns):
            width = max(df[col].astype(str).str.len().max(), len(col) + 2)
            worksheet.set_column(i, i, width)

        writer.save()
        print(f"Attendance records exported to {filename}")
    except Exception as e:
        print("Error while exporting to Excel:", e)

folder_path = r"C:\Users\bhara\OneDrive\Desktop\photo"

known_face_names, known_face_encodings, image_paths = load_images_from_folder(folder_path)
student_details = fetch_student_details()

if not student_details:
    print("Failed to fetch student details. Exiting program.")
    exit()

video_capture = cv2.VideoCapture(0)

face_locations = []
face_encodings = []
face_names = []
attendance_records = []
recognized_faces = set()  # Set to store recognized faces

# Set the face recognition threshold
face_recognition_threshold = 0.6

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='student_attendance_records',
                                         user='root',
                                         password='')

    while True:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # Increase the scale factor for faster face detection
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        attendance_date = datetime.now().strftime("%Y-%m-%d")
        attendance_time = datetime.now().strftime("%H:%M:%S")

        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            name = "Unknown"  # Default name if face not recognized
            
            matches = face_recognition.compare_faces(list(known_face_encodings.values()), face_encoding, tolerance=face_recognition_threshold)
            if True in matches:
                matched_index = matches.index(True)
                name = list(known_face_encodings.keys())[matched_index]

            if name in student_details:
                roll_number = student_details[name]['Roll_number']
                # Draw a rectangle around the face
                cv2.rectangle(frame, (left * 2, top * 2), (right * 2, bottom * 2), (0, 0, 255), 2)
                # Display name and roll number on the frame
                text = f"{name} ({roll_number})"
                cv2.putText(frame, text, (left * 2 + 6, bottom * 2 + 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
            else:
                # Draw a rectangle around the face
                cv2.rectangle(frame, (left * 2, top * 2), (right * 2, bottom * 2), (0, 0, 255), 2)
                # Display "Unknown" on the frame
                cv2.putText(frame, "Unknown", (left * 2 + 6, bottom * 2 + 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

            # Record attendance if not already recorded
            if name not in recognized_faces and name != "Unknown":
                recognized_faces.add(name)
                roll_number = student_details[name]['Roll_number']
                phone_number = student_details[name]['Phone_number']
                record_attendance(name, roll_number, phone_number, attendance_date, attendance_time, connection)
                attendance_records.append({"Roll_Number": roll_number, "Student_name": name, "Phone_Number": phone_number, "Attendance_date": attendance_date, "Attendance_time": attendance_time})
                print(f"Attendance recorded for {name} with roll number {roll_number}")

        cv2.imshow("Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

video_capture.release()
cv2.destroyAllWindows()

export_to_excel(attendance_records)
