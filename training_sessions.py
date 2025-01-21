import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk

def training_menu():
    # Create a new window for Training Sessions Management
    training_window = tk.Toplevel()
    training_window.title("Training Sessions Management")
    training_window.geometry("1530x790+0+0")

    # Background Image
    global background_image
    background_image = Image.open("cric_back.jpg")
    background_image = background_image.resize((1530, 790), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(training_window, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    title_label = tk.Label(training_window, text="Training Sessions", font=("Arial", 24, "bold"))
    title_label.pack(pady=20)
    # Add Session Button
    add_button = tk.Button(training_window, text="Add Training Session", command=add_session, font=("Arial", 16), bg="lightblue", fg="black")
    add_button.pack(pady=20)

    # View Sessions Button
    view_button = tk.Button(training_window, text="View Training Sessions", command=view_sessions, font=("Arial", 16), bg="lightblue", fg="black")
    view_button.pack(pady=20)

    # Back Button
    back_button = tk.Button(training_window, text="Back", command=training_window.destroy, font=("Arial", 16), bg="lightblue", fg="black")
    back_button.pack(pady=20)

    training_window.mainloop()


def add_session():
    add_session_window = tk.Toplevel()
    add_session_window.title("Add Training Session")
    add_session_window.geometry("1530x790+0+0")

    bg_image = Image.open("cric_back.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(add_session_window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Labels and Entry Fields
    label_date = tk.Label(add_session_window, text="Date (YYYY-MM-DD):", font=("Arial", 12))
    label_date.pack(pady=5)
    entry_date = tk.Entry(add_session_window, font=("Arial", 12))
    entry_date.pack(pady=5)

    label_time = tk.Label(add_session_window, text="Time (HH:MM:SS):", font=("Arial", 12))
    label_time.pack(pady=5)
    entry_time = tk.Entry(add_session_window, font=("Arial", 12))
    entry_time.pack(pady=5)

    label_location = tk.Label(add_session_window, text="Location:", font=("Arial", 12))
    label_location.pack(pady=5)
    entry_location = tk.Entry(add_session_window, font=("Arial", 12))
    entry_location.pack(pady=5)

    label_coach_id = tk.Label(add_session_window, text="Coach ID:", font=("Arial", 12))
    label_coach_id.pack(pady=5)
    entry_coach_id = tk.Entry(add_session_window, font=("Arial", 12))
    entry_coach_id.pack(pady=5)

    label_session_type = tk.Label(add_session_window, text="Session Type:", font=("Arial", 12))
    label_session_type.pack(pady=5)
    session_type_combobox = ttk.Combobox(add_session_window, font=("Arial", 12), values=["Individual", "Group", "Special Clinic"])
    session_type_combobox.pack(pady=5)

    # Save Button
    save_button = tk.Button(add_session_window, text="Save Session", command=lambda: save_session(entry_date, entry_time, entry_location, entry_coach_id, session_type_combobox, add_session_window), font=("Arial", 12), bg="green", fg="white")
    save_button.pack(pady=20)

    back_button = tk.Button(add_session_window, text="Back", command=add_session_window.destroy)
    back_button.pack(pady=10)


def save_session(entry_date, entry_time, entry_location, entry_coach_id, session_type_combobox, window):
    session_date = entry_date.get()
    session_time = entry_time.get()
    location = entry_location.get()
    coach_id = entry_coach_id.get()
    session_type = session_type_combobox.get()

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="Kalpesh@01",  # Replace with your MySQL password
            database="cricket_academy"
        )
        cursor = conn.cursor()

        # Insert into database
        insert_query = """INSERT INTO training_sessions (date, time, location, coach_id, session_type)
                          VALUES (%s, %s, %s, %s, %s)"""
        session_data = (session_date, session_time, location, coach_id, session_type)
        cursor.execute(insert_query, session_data)
        conn.commit()

        messagebox.showinfo("Success", "Training session added successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    window.destroy()


def view_sessions():
    view_sessions_window = tk.Toplevel()
    view_sessions_window.title("View Training Sessions")
    view_sessions_window.geometry("1530x790+0+0")

    bg_image = Image.open("cric_back.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(view_sessions_window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Table for displaying sessions
    session_list = ttk.Treeview(view_sessions_window, columns=("Session ID", "Date", "Time", "Location", "Coach ID", "Session Type"), show="headings", height=30)
    session_list.heading("Session ID", text="Session ID")
    session_list.heading("Date", text="Date")
    session_list.heading("Time", text="Time")
    session_list.heading("Location", text="Location")
    session_list.heading("Coach ID", text="Coach ID")
    session_list.heading("Session Type", text="Session Type")
    session_list.pack(pady=20)

    fetch_sessions(session_list)

    back_button = tk.Button(view_sessions_window, text="Back", command=view_sessions_window.destroy)
    back_button.pack(pady=10)
def fetch_sessions(session_list):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="Kalpesh@01",  # Replace with your MySQL password
            database="cricket_academy"
        )
        cursor = conn.cursor()

        # Select all sessions
        cursor.execute("SELECT * FROM training_sessions")
        sessions = cursor.fetchall()

        for row in sessions:
            session_list.insert("", tk.END, values=row)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

