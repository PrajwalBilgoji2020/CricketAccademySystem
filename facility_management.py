import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector

# Function to connect to the database
def back_to_menu(window):
    window.destroy()
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="Kalpesh@01",  # Replace with your MySQL password
            database="cricket_academy"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection Error", f"Error: {err}")
        return None

# Function to add a new facility
def add_facility():
    def save_facility():
        facility_name = entry_facility_name.get()
        facility_type = combo_facility_type.get()

        # Database connection
        conn = create_connection()
        if conn:
            cursor = conn.cursor()

            try:
                # Insert query
                insert_query = """INSERT INTO facilities (facility_name, type)
                                  VALUES (%s, %s)"""
                facility_data = (facility_name, facility_type)
                cursor.execute(insert_query, facility_data)
                conn.commit()
                messagebox.showinfo("Success", "Facility added successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
                add_facility_window.destroy()

    # Add facility window
    add_facility_window = tk.Toplevel()
    add_facility_window.title("Add New Facility")
    add_facility_window.geometry("1530x790+0+0")

    # Background Image
    bg_image = Image.open("cric_back.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(add_facility_window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Labels and entry fields for facility details
    tk.Label(add_facility_window, text="Facility Name").pack(pady=5)
    entry_facility_name = tk.Entry(add_facility_window)
    entry_facility_name.pack(pady=5)

    tk.Label(add_facility_window, text="Facility Type").pack(pady=5)
    combo_facility_type = ttk.Combobox(add_facility_window, values=["Ground", "Indoor Net", "Gym"])
    combo_facility_type.pack(pady=5)

    # Save button
    save_button = tk.Button(add_facility_window, text="Save Facility", command=save_facility)
    save_button.pack(pady=20)

    back_button = tk.Button(add_facility_window, text="Back", command=add_facility_window.destroy)
    back_button.pack(pady=10)

    # Keep reference to background image
    add_facility_window.bg_image = bg_image

# Function to view all facilities
def view_facilities():
    def load_facilities():
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM facilities")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)
            cursor.close()
            conn.close()

    # View facilities window
    view_window = tk.Toplevel()
    view_window.title("View Facilities")
    view_window.geometry("1530x790+0+0")

    background_image = Image.open("cric_back.jpg")
    background_image = background_image.resize((1530, 790), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(view_window, image=background_photo)
    background_label.image = background_photo  # Keep a reference to avoid garbage collection
    background_label.place(relwidth=1, relheight=1)
    # Treeview to display facilities
    columns = ("Facility ID", "Facility Name", "Type")
    tree = ttk.Treeview(view_window, columns=columns, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

    load_facilities()

    back_button = tk.Button(view_window, text="Back", command=view_window.destroy)
    back_button.pack(pady=10)

# Function to delete a facility
def delete_facility():
    def remove_facility():
        facility_id = entry_facility_id.get()

        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                delete_query = "DELETE FROM facilities WHERE facility_id = %s"
                cursor.execute(delete_query, (facility_id,))
                conn.commit()
                messagebox.showinfo("Success", "Facility deleted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
                delete_window.destroy()

    # Delete facility window
    delete_window = tk.Toplevel()
    delete_window.title("Delete Facility")
    delete_window.geometry("1530x790+0+0")

    background_image = Image.open("cric_back.jpg")
    background_image = background_image.resize((1530, 790), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(delete_window, image=background_photo)
    background_label.image = background_photo  # Keep a reference to avoid garbage collection
    background_label.place(relwidth=1, relheight=1)

    tk.Label(delete_window, text="Facility ID to Delete").pack(pady=5)
    entry_facility_id = tk.Entry(delete_window)
    entry_facility_id.pack(pady=5)

    delete_button = tk.Button(delete_window, text="Delete Facility", command=remove_facility)
    delete_button.pack(pady=20)

    back_button = tk.Button(delete_window, text="Back", command=delete_window.destroy)
    back_button.pack(pady=10)

# Main function to run the application
def facility_menu():
    facility_window = tk.Toplevel()
    facility_window.title("Facility Management")
    facility_window.geometry("1530x790+0+0")

    bg_image = Image.open("cric_back.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(facility_window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    title_label = tk.Label(facility_window, text="Facility Management", font=("Arial", 24, "bold"))
    title_label.pack(pady=20)

    add_button = tk.Button(facility_window, text="Add Facility", command=add_facility)
    add_button.pack(pady=10)

    view_button = tk.Button(facility_window, text="View Facilities", command=view_facilities)
    view_button.pack(pady=10)

    delete_button = tk.Button(facility_window, text="Delete Facility", command=delete_facility)
    delete_button.pack(pady=10)

    back_button = tk.Button(facility_window, text="Back", command=facility_window.destroy)
    back_button.pack(pady=10)

    facility_window.mainloop()


