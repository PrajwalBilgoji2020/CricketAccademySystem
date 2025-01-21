import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kalpesh@01",
        database="cricket_academy"
    )
# Add Player to the database with Validation
def add_player():
    # Validate all felds
    if not entry_name.get() or not entry_dob.get() or not entry_gender.get() or not entry_address.get() or \
            not entry_contact.get() or not entry_email.get() or not entry_role.get() or \
            not entry_batting_style.get() or not entry_bowling_style.get() or not entry_parent_name.get() or \
            not entry_parent_number.get():
        messagebox.showwarning("Input Error", "Please fll in all the player details.")
        return
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = """INSERT INTO players 
             (player_name, date_of_birth, gender, address, contact_number, email, 
             role, batting_style, bowling_style, parent_name, parent_number) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (entry_name.get(), entry_dob.get(), entry_gender.get(), entry_address.get(),
              entry_contact.get(), entry_email.get(), entry_role.get(),
              entry_batting_style.get(), entry_bowling_style.get(),
              entry_parent_name.get(), entry_parent_number.get())
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Success", "Player added successfully")
    refresh_player_list() # Refresh the list after adding a player
    clear_entries() # Clear form felds after successful submission
# Clear form entries
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_dob.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_contact.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_role.delete(0, tk.END)
    entry_batting_style.delete(0, tk.END)
    entry_bowling_style.delete(0, tk.END)
    entry_parent_name.delete(0, tk.END)
    entry_parent_number.delete(0, tk.END)
# Refresh Player List
def refresh_player_list():
    for row in tree.get_children():
        tree.delete(row)
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    for player in players:
        tree.insert('', tk.END, values=player)
    cursor.close()
    conn.close()
# Delete Player
def delete_player():
    selected_item = tree.selection()[0]
    player_id = tree.item(selected_item)['values'][0]
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players WHERE player_id = %s", (player_id,))
    conn.commit()
    cursor.close()
    conn.close()
    refresh_player_list()
    messagebox.showinfo("Success", "Player deleted successfully")
# Home Page
def home_page():
    for widget in root.winfo_children():
        widget.destroy()
    home_frame = tk.Frame(root)
    home_frame.pack(fill='both', expand=True)
    bg_image = tk.PhotoImage(file=r"C:\Users\KALPESH\Downloads\bng.png")
    bg_label = tk.Label(home_frame, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(relwidth=1, relheight=1)
    btn_player_mgmt = tk.Button(home_frame, text="Player Management", command=player_management_page)
    btn_player_mgmt.pack(pady=10)
    # Additional buttons for other sections can be added here
# Player Management Page
def player_management_page():
    for widget in root.winfo_children():
        widget.destroy()
    pm_frame = tk.Frame(root)
    pm_frame.pack(fill='both', expand=True)
    bg_image = tk.PhotoImage(file=r"C:\Users\KALPESH\Downloads\bng.png")
    bg_label = tk.Label(pm_frame, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(relwidth=1, relheight=1)
    btn_add_player = tk.Button(pm_frame, text="Add Player", command=add_player_page)
    btn_add_player.pack(pady=10)
    btn_player_list = tk.Button(pm_frame, text="Player List", command=player_list_page)
    btn_player_list.pack(pady=10)
    btn_back = tk.Button(pm_frame, text="Back", command=home_page)
    btn_back.pack(pady=10)
# Add Player Page
def add_player_page():
    for widget in root.winfo_children():
        widget.destroy()
    ap_frame = tk.Frame(root)
    ap_frame.pack(fill='both', expand=True)
    bg_image = tk.PhotoImage(file=r"C:\Users\KALPESH\Downloads\bng.png")
    bg_label = tk.Label(ap_frame, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(relwidth=1, relheight=1)
    felds = ['Player Name', 'Date of Birth', 'Gender', 'Address', 'Contact Number',
              'Email', 'Role', 'Batting Style', 'Bowling Style', 'Parent Name', 'Parent Number']
    global entry_name, entry_dob, entry_gender, entry_address, entry_contact, entry_email
    global entry_role, entry_batting_style, entry_bowling_style, entry_parent_name, entry_parent_number
    for i, feld in enumerate(felds):
        label = tk.Label(ap_frame, text=feld)
        label.grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(ap_frame)
        entry.grid(row=i, column=1, padx=10, pady=5)
        if feld == 'Player Name':
            entry_name = entry
        elif feld == 'Date of Birth':
            entry_dob = entry
        elif feld == 'Gender':
            entry_gender = entry
        elif feld == 'Address':
            entry_address = entry
        elif feld == 'Contact Number':
            entry_contact = entry
        elif feld == 'Email':
            entry_email = entry
        elif feld == 'Role':
            entry_role = entry
        elif feld == 'Batting Style':
            entry_batting_style = entry
        elif feld == 'Bowling Style':
            entry_bowling_style = entry
        elif feld == 'Parent Name':
            entry_parent_name = entry
        elif feld == 'Parent Number':
            entry_parent_number = entry
    btn_add = tk.Button(ap_frame, text="Add Player", command=add_player)
    btn_add.grid(row=len(felds), column=1, pady=10)
    btn_back = tk.Button(ap_frame, text="Back", command=player_management_page)
    btn_back.grid(row=len(felds), column=0, pady=10)
# Player List Page
def player_list_page():
    for widget in root.winfo_children():
        widget.destroy()
    pl_frame = tk.Frame(root)
    pl_frame.pack(fill='both', expand=True)
    bg_image = tk.PhotoImage(file=r"C:\Users\KALPESH\Downloads\bng.png")
    bg_label = tk.Label(pl_frame, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(relwidth=1, relheight=1)
    columns = ('player_id', 'player_name', 'date_of_birth', 'gender', 'address', 'contact_number',
               'email', 'role', 'batting_style', 'bowling_style', 'parent_name', 'parent_number')
    global tree
    tree = ttk.Treeview(pl_frame, columns=columns, show='headings')
    tree.heading('player_id', text='Player ID')
    tree.heading('player_name', text='Player Name')
    tree.heading('date_of_birth', text='Date of Birth')
    tree.heading('gender', text='Gender')
    tree.heading('address', text='Address')
    tree.heading('contact_number', text='Contact Number')
    tree.heading('email', text='Email')
    tree.heading('role', text='Role')
    tree.heading('batting_style', text='Batting Style')
    tree.heading('bowling_style', text='Bowling Style')
    tree.heading('parent_name', text='Parent Name')
    tree.heading('parent_number', text='Parent Number')
    tree.pack(fill='both', expand=True)
    refresh_player_list()
    btn_delete = tk.Button(pl_frame, text="Delete Player", command=delete_player)
    btn_delete.pack(pady=10)
    btn_back = tk.Button(pl_frame, text="Back", command=player_management_page)
    btn_back.pack(pady=10)
# Main Tkinter setup
root = tk.Tk()
root.title("Cricket Management System")
root.geometry("800x600")
home_page()
root.mainloop()