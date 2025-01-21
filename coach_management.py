import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from PIL import Image, ImageTk

# Function to go back to the main menu
def back_to_menu(window):
    window.destroy()  # Close the current window

# Function to add a new coach
def add_coach():
    def save_coach():
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        dob = entry_dob.get()
        gender = gender_combobox.get()  # Get selected value from combobox
        address = entry_address.get()
        phone = entry_phone.get()

        # Database connection
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Replace with your MySQL username
                password="Kalpesh@01",  # Replace with your MySQL password
                database="cricket_academy"
            )
            cursor = conn.cursor()

            # Insert query
            insert_query = """INSERT INTO coaches (first_name, last_name, date_of_birth, gender, address, phone_number)
                              VALUES (%s, %s, %s, %s, %s, %s)"""
            coach_data = (first_name, last_name, dob, gender, address, phone)
            cursor.execute(insert_query, coach_data)
            conn.commit()

            messagebox.showinfo("Success", "Coach added successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        add_coach_window.destroy()

    # Add coach window
    add_coach_window = tk.Toplevel()
    add_coach_window.title("Add New Coach")
    add_coach_window.geometry("1530x790+0+0")

    bg_image = Image.open("cric_back.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(add_coach_window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Labels and entry fields for coach details
    tk.Label(add_coach_window, text="First Name").pack(pady=5)
    entry_first_name = tk.Entry(add_coach_window)
    entry_first_name.pack(pady=5)

    tk.Label(add_coach_window, text="Last Name").pack(pady=5)
    entry_last_name = tk.Entry(add_coach_window)
    entry_last_name.pack(pady=5)

    tk.Label(add_coach_window, text="Date of Birth (YYYY-MM-DD)").pack(pady=5)
    entry_dob = tk.Entry(add_coach_window)
    entry_dob.pack(pady=5)

    tk.Label(add_coach_window, text="Gender").pack(pady=5)
    gender_combobox = ttk.Combobox(add_coach_window, values=["Male", "Female"], state="readonly")
    gender_combobox.pack(pady=5)
    gender_combobox.current(0)  # Default selection to "Male"

    tk.Label(add_coach_window, text="Address").pack(pady=5)
    entry_address = tk.Entry(add_coach_window)
    entry_address.pack(pady=5)

    tk.Label(add_coach_window, text="Phone Number").pack(pady=5)
    entry_phone = tk.Entry(add_coach_window)
    entry_phone.pack(pady=5)

    # Save button
    save_button = tk.Button(add_coach_window, text="Save Coach", command=save_coach)
    save_button.pack(pady=20)

    back_button = tk.Button(add_coach_window, text="Back", command=add_coach_window.destroy)
    back_button.pack(pady=10)

# Function to view all coaches
def view_coaches():
    def fetch_coaches():
        # Fetch coach data from the database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Replace with your MySQL username
                password="Kalpesh@01",  # Replace with your MySQL password
                database="cricket_academy"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM coaches")
            coaches = cursor.fetchall()

            for row in coaches:
                coach_list.insert("", tk.END, values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # View coaches window
    view_coaches_window = tk.Toplevel()
    view_coaches_window.title("View Coaches")
    view_coaches_window.geometry("1530x790+0+0")

    bg_image = Image.open("cric_back.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(view_coaches_window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    columns = ("Coach ID", "First Name", "Last Name", "Date of Birth", "Gender", "Address", "Phone Number")
    coach_list = ttk.Treeview(view_coaches_window, columns=columns, show="headings")

    for col in columns:
        coach_list.heading(col, text=col)

    coach_list.pack(fill=tk.BOTH, expand=True)

    # Fetch data
    fetch_coaches()

    back_button = tk.Button(view_coaches_window, text="Back", command=view_coaches_window.destroy)
    back_button.pack(pady=10)
# Main Coach Management window
def open_coach_management():
    coach_management_window = tk.Toplevel()
    coach_management_window.title("Coach Management")
    coach_management_window.geometry("1530x790+0+0")

    background_image = Image.open("cric_back.jpg")
    background_image = background_image.resize((1530, 790), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(coach_management_window, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    title_label = tk.Label(coach_management_window, text="Coach Management", font=("Arial", 24, "bold"))
    title_label.pack(pady=20)
    # Buttons for coach management
    tk.Button(coach_management_window, text="Add Coach", command=add_coach, width=20).pack(pady=10)
    tk.Button(coach_management_window, text="View Coaches", command=view_coaches, width=20).pack(pady=10)
    tk.Button(coach_management_window, text="Back", command=lambda: back_to_menu(coach_management_window), width=20).pack(pady=10)
    coach_management_window.mainloop()
