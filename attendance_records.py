import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox
import csv

# Database connection function
def connect_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kalpesh@01",  # Replace with your MySQL password
        database="cricket_academy"
    )

# Function to add attendance
def add_attendance():
    def save_attendance():
        conn = connect_database()
        cursor = conn.cursor()

        player_id = entry_player_id.get()
        session_id = entry_session_id.get()
        attendance_status = status_combobox.get()

        query = "INSERT INTO attendance_records (player_id, session_id, attendance_status) VALUES (%s, %s, %s)"
        values = (player_id, session_id, attendance_status)

        try:
            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Success", "Attendance added successfully!")
            add_attendance_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding attendance: {e}")
        finally:
            cursor.close()
            conn.close()

    add_attendance_window = tk.Toplevel()
    add_attendance_window.title("Add Attendance")
    add_attendance_window.geometry("1530x790+0+0")

    bg_image = Image.open("cric_back.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(add_attendance_window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(add_attendance_window, text="Player ID").pack(pady=5)
    entry_player_id = tk.Entry(add_attendance_window)
    entry_player_id.pack(pady=5)

    tk.Label(add_attendance_window, text="Session ID").pack(pady=5)
    entry_session_id = tk.Entry(add_attendance_window)
    entry_session_id.pack(pady=5)

    tk.Label(add_attendance_window, text="Attendance Status").pack(pady=5)
    status_combobox = ttk.Combobox(add_attendance_window, values=["Present", "Absent", "Late"], state="readonly")
    status_combobox.pack(pady=5)
    status_combobox.current(0)

    save_button = tk.Button(add_attendance_window, text="Save Attendance", command=save_attendance)
    save_button.pack(pady=20)

    back_button = tk.Button(add_attendance_window, text="Back", command=add_attendance_window.destroy)
    back_button.pack(pady=10)

# Function to view attendance
def view_attendance():
    view_attendance_window = tk.Toplevel()
    view_attendance_window.title("View Attendance")
    view_attendance_window.geometry("1530x790+0+0")

    background_image = Image.open("cric_back.jpg")
    background_image = background_image.resize((1530, 790), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(view_attendance_window, image=background_photo)
    background_label.image = background_photo  # Keep a reference to avoid garbage collection
    background_label.place(relwidth=1, relheight=1)

    columns = ("Record ID", "Player ID", "Session ID", "Status")
    tree = ttk.Treeview(view_attendance_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)

    tree.pack(fill=tk.BOTH, expand=True)

    conn = connect_database()
    cursor = conn.cursor()
    query = "SELECT record_id, player_id, session_id, attendance_status FROM attendance_records"
    cursor.execute(query)

    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

    cursor.close()
    conn.close()

    back_button = tk.Button(view_attendance_window, text="Back", command=view_attendance_window.destroy)
    back_button.pack(pady=10)

# Function to export attendance to CSV
def export_attendance_csv():
    conn = connect_database()
    cursor = conn.cursor()

    query = "SELECT record_id, player_id, session_id, attendance_status FROM attendance_records"
    cursor.execute(query)

    rows = cursor.fetchall()

    # Save the results in a CSV file
    with open('attendance_records.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # Writing headers
        writer.writerow(["Record ID", "Player ID", "Session ID", "Attendance Status"])
        # Writing the rows
        writer.writerows(rows)

    messagebox.showinfo("Success", "Attendance records exported to CSV successfully!")

    cursor.close()
    conn.close()

# Function to manage (update or delete) attendance
def manage_attendance():
    def update_attendance():
        conn = connect_database()
        cursor = conn.cursor()

        record_id = entry_record_id.get()
        player_id = entry_player_id.get()
        session_id = entry_session_id.get()
        attendance_status = status_combobox.get()

        query = "UPDATE attendance_records SET player_id=%s, session_id=%s, attendance_status=%s WHERE record_id=%s"
        values = (player_id, session_id, attendance_status, record_id)

        try:
            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Success", "Attendance updated successfully!")
            manage_attendance_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating attendance: {e}")
        finally:
            cursor.close()
            conn.close()

    def delete_attendance():
        conn = connect_database()
        cursor = conn.cursor()

        record_id = entry_record_id.get()

        query = "DELETE FROM attendance_records WHERE record_id=%s"
        try:
            cursor.execute(query, (record_id,))
            conn.commit()
            messagebox.showinfo("Success", "Attendance deleted successfully!")
            manage_attendance_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting attendance: {e}")
        finally:
            cursor.close()
            conn.close()

    manage_attendance_window = tk.Toplevel()
    manage_attendance_window.title("Manage Attendance")
    manage_attendance_window.geometry("1530x790+0+0")

    bg_image = Image.open("cric_back.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(manage_attendance_window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(manage_attendance_window, text="Record ID").pack(pady=5)
    entry_record_id = tk.Entry(manage_attendance_window)
    entry_record_id.pack(pady=5)

    tk.Label(manage_attendance_window, text="Player ID").pack(pady=5)
    entry_player_id = tk.Entry(manage_attendance_window)
    entry_player_id.pack(pady=5)

    tk.Label(manage_attendance_window, text="Session ID").pack(pady=5)
    entry_session_id = tk.Entry(manage_attendance_window)
    entry_session_id.pack(pady=5)

    tk.Label(manage_attendance_window, text="Attendance Status").pack(pady=5)
    status_combobox = ttk.Combobox(manage_attendance_window, values=["Present", "Absent", "Late"], state="readonly")
    status_combobox.pack(pady=5)
    status_combobox.current(0)

    update_button = tk.Button(manage_attendance_window, text="Update Attendance", command=update_attendance)
    update_button.pack(pady=20)

    delete_button = tk.Button(manage_attendance_window, text="Delete Attendance", command=delete_attendance)
    delete_button.pack(pady=10)

    back_button = tk.Button(manage_attendance_window, text="Back", command=manage_attendance_window.destroy)
    back_button.pack(pady=10)

# Main function for attendance management
def attendance_menu():
    attendance_window = tk.Toplevel()
    attendance_window.title("Attendance Management")
    attendance_window.geometry("1530x790+0+0")

    bg_image = Image.open("cric_back.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(attendance_window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Title Label
    title_label = tk.Label(attendance_window, text="Attendance Management", font=("Arial", 24), bg="lightblue")
    title_label.pack(pady=20)

    add_attendance_button = tk.Button(attendance_window, text="Add Attendance", font=("Arial", 18), command=add_attendance)
    add_attendance_button.pack(pady=10)

    view_attendance_button = tk.Button(attendance_window, text="View Attendance", font=("Arial", 18), command=view_attendance)
    view_attendance_button.pack(pady=10)

    manage_attendance_button = tk.Button(attendance_window, text="Manage Attendance", font=("Arial", 18), command=manage_attendance)
    manage_attendance_button.pack(pady=10)

    export_csv_button = tk.Button(attendance_window, text="Export to CSV", font=("Arial", 18), command=export_attendance_csv)
    export_csv_button.pack(pady=10)

    back_button = tk.Button(attendance_window, text="Back", font=("Arial", 18), command=attendance_window.destroy)
    back_button.pack(pady=20)
