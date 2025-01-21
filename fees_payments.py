import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox

# MySQL connection
def connect_database():
    return mysql.connector.connect(
        host="localhost",  # Replace with your MySQL host
        user="root",       # Replace with your MySQL username
        password="Kalpesh@01",       # Replace with your MySQL password
        database="cricket_academy"  # Replace with your database name
    )

# Function to add fees
def add_fees():
    def save_fee():
        conn = connect_database()
        cursor = conn.cursor()

        player_id = entry_player_id.get()
        fee_amount = entry_fee_amount.get()
        payment_date = entry_payment_date.get()
        payment_type = payment_type_combobox.get()
        fee_type = fee_type_combobox.get()
        status = status_combobox.get()

        query = "INSERT INTO fees_payments (player_id, amount, payment_date, payment_type, fee_type, status) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (player_id, fee_amount, payment_date, payment_type, fee_type, status)

        try:
            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Success", "Fee added successfully!")
            add_fees_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding fee: {e}")
        finally:
            cursor.close()
            conn.close()

    add_fees_window = tk.Toplevel()
    add_fees_window.title("Add Fees")
    add_fees_window.geometry("1530x790+0+0")

    bg_image = Image.open("cric_back.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(add_fees_window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(add_fees_window, text="Player ID").pack(pady=5)
    entry_player_id = tk.Entry(add_fees_window)
    entry_player_id.pack(pady=5)

    tk.Label(add_fees_window, text="Fee Amount").pack(pady=5)
    entry_fee_amount = tk.Entry(add_fees_window)
    entry_fee_amount.pack(pady=5)

    tk.Label(add_fees_window, text="Payment Date (YYYY-MM-DD)").pack(pady=5)
    entry_payment_date = tk.Entry(add_fees_window)
    entry_payment_date.pack(pady=5)

    tk.Label(add_fees_window, text="Payment Type").pack(pady=5)
    payment_type_combobox = ttk.Combobox(add_fees_window, values=["Cash", "Card", "Online"], state="readonly")
    payment_type_combobox.pack(pady=5)
    payment_type_combobox.current(0)

    tk.Label(add_fees_window, text="Fee Type").pack(pady=5)
    fee_type_combobox = ttk.Combobox(add_fees_window, values=["Registration", "Monthly Fee", "Training Camp Fee"], state="readonly")
    fee_type_combobox.pack(pady=5)
    fee_type_combobox.current(0)

    tk.Label(add_fees_window, text="Status").pack(pady=5)
    status_combobox = ttk.Combobox(add_fees_window, values=["Paid", "Pending"], state="readonly")
    status_combobox.pack(pady=5)
    status_combobox.current(0)

    save_button = tk.Button(add_fees_window, text="Save Fee", command=save_fee)
    save_button.pack(pady=20)

    back_button = tk.Button(add_fees_window, text="Back", command=add_fees_window.destroy)
    back_button.pack(pady=10)

# Function to view fees
def view_fees():
    view_fees_window = tk.Toplevel()
    view_fees_window.title("View Fees")
    view_fees_window.geometry("1530x790+0+0")

    background_image = Image.open("cric_back.jpg")
    background_image = background_image.resize((1530, 790), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(view_fees_window, image=background_photo)
    background_label.image = background_photo  # Keep a reference to avoid garbage collection
    background_label.place(relwidth=1, relheight=1)

    columns = ("Player ID", "Amount", "Payment Date", "Payment Type", "Fee Type", "Status")
    tree = ttk.Treeview(view_fees_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)

    tree.pack(fill=tk.BOTH, expand=True)

    conn = connect_database()
    cursor = conn.cursor()
    query = "SELECT player_id, amount, payment_date, payment_type, fee_type, status FROM fees_payments"
    cursor.execute(query)

    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

    cursor.close()
    conn.close()

    back_button = tk.Button(view_fees_window, text="Back", command=view_fees_window.destroy)
    back_button.pack(pady=10)

# Function to manage (update or delete) fees
def manage_fees():
    def update_fees():
        conn = connect_database()
        cursor = conn.cursor()

        payment_id = entry_payment_id.get()
        player_id = entry_player_id.get()
        fee_amount = entry_fee_amount.get()
        payment_date = entry_payment_date.get()
        payment_type = payment_type_combobox.get()
        fee_type = fee_type_combobox.get()
        status = status_combobox.get()

        query = "UPDATE fees_payments SET player_id=%s, amount=%s, payment_date=%s, payment_type=%s, fee_type=%s, status=%s WHERE payment_id=%s"
        values = (player_id, fee_amount, payment_date, payment_type, fee_type, status, payment_id)

        try:
            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Success", "Fee updated successfully!")
            manage_fees_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating fee: {e}")
        finally:
            cursor.close()
            conn.close()

    def delete_fees():
        conn = connect_database()
        cursor = conn.cursor()

        payment_id = entry_payment_id.get()

        query = "DELETE FROM fees_payments WHERE payment_id=%s"
        try:
            cursor.execute(query, (payment_id,))
            conn.commit()
            messagebox.showinfo("Success", "Fee deleted successfully!")
            manage_fees_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting fee: {e}")
        finally:
            cursor.close()
            conn.close()

    manage_fees_window = tk.Toplevel()
    manage_fees_window.title("Manage Fees")
    manage_fees_window.geometry("1530x790+0+0")

    bg_image = Image.open("cric_back.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(manage_fees_window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(manage_fees_window, text="Payment ID").pack(pady=5)
    entry_payment_id = tk.Entry(manage_fees_window)
    entry_payment_id.pack(pady=5)

    tk.Label(manage_fees_window, text="Player ID").pack(pady=5)
    entry_player_id = tk.Entry(manage_fees_window)
    entry_player_id.pack(pady=5)

    tk.Label(manage_fees_window, text="Fee Amount").pack(pady=5)
    entry_fee_amount = tk.Entry(manage_fees_window)
    entry_fee_amount.pack(pady=5)

    tk.Label(manage_fees_window, text="Payment Date (YYYY-MM-DD)").pack(pady=5)
    entry_payment_date = tk.Entry(manage_fees_window)
    entry_payment_date.pack(pady=5)

    tk.Label(manage_fees_window, text="Payment Type").pack(pady=5)
    payment_type_combobox = ttk.Combobox(manage_fees_window, values=["Cash", "Card", "Online"], state="readonly")
    payment_type_combobox.pack(pady=5)
    payment_type_combobox.current(0)

    tk.Label(manage_fees_window, text="Fee Type").pack(pady=5)
    fee_type_combobox = ttk.Combobox(manage_fees_window, values=["Registration", "Monthly Fee", "Training Camp Fee"], state="readonly")
    fee_type_combobox.pack(pady=5)
    fee_type_combobox.current(0)

    tk.Label(manage_fees_window, text="Status").pack(pady=5)
    status_combobox = ttk.Combobox(manage_fees_window, values=["Paid", "Pending"], state="readonly")
    status_combobox.pack(pady=5)
    status_combobox.current(0)

    update_button = tk.Button(manage_fees_window, text="Update Fee", command=update_fees)
    update_button.pack(pady=20)

    delete_button = tk.Button(manage_fees_window, text="Delete Fee", command=delete_fees)
    delete_button.pack(pady=10)

    back_button = tk.Button(manage_fees_window, text="Back", command=manage_fees_window.destroy)
    back_button.pack(pady=10)

# Main function for fees management
def open_fees_management():
    fees_window = tk.Toplevel()
    fees_window.title("Fees Management")
    fees_window.geometry("1530x790+0+0")

    # Load and set the background image
    background_image = Image.open("cric_back.jpg")
    background_image = background_image.resize((1530, 790), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(fees_window, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    tk.Label(fees_window, text="Fees Management", font=("Arial", 24), bg="lightblue").pack(pady=20)

    add_fees_button = tk.Button(fees_window, text="Add Fees", command=add_fees, width=20)
    add_fees_button.pack(pady=10)

    view_fees_button = tk.Button(fees_window, text="View Fees", command=view_fees, width=20)
    view_fees_button.pack(pady=10)

    manage_fees_button = tk.Button(fees_window, text="Manage Fees", command=manage_fees, width=20)
    manage_fees_button.pack(pady=10)

    back_button = tk.Button(fees_window, text="Back", command=fees_window.destroy)
    back_button.pack(pady=20)

    fees_window.mainloop()
