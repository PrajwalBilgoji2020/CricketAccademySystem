import tkinter as tk
import mysql.connector
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
# Function to add a new player
def back_to_menu(window):
    window.destroy()
def add_player():
    def save_player():
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        dob = entry_dob.get()
        gender = gender_combobox.get()
        address = entry_address.get()
        phone = entry_phone.get()
        join_date = entry_join_date.get()
        skill_level = skill_level_combobox.get()
        position = position_combobox.get()

        # Database connection
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Kalpesh@01",
                database="cricket_academy"
            )
            cursor = conn.cursor()

            # Insert query
            insert_query = """INSERT INTO players (first_name, last_name, date_of_birth, gender, address, phone_number, joining_date, skill_level, position)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            player_data = (first_name, last_name, dob, gender, address, phone, join_date, skill_level, position)
            cursor.execute(insert_query, player_data)
            conn.commit()

            messagebox.showinfo("Success", "Player added successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        add_player_window.destroy()

    # Add player window
    add_player_window = tk.Toplevel()
    add_player_window.title("Add New Player")
    add_player_window.geometry("1530x790+0+0")

    bg_image = Image.open("cric_back.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(add_player_window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Labels and entry fields for player details
    tk.Label(add_player_window, text="First Name").pack(pady=5)
    entry_first_name = tk.Entry(add_player_window)
    entry_first_name.pack(pady=5)

    tk.Label(add_player_window, text="Last Name").pack(pady=5)
    entry_last_name = tk.Entry(add_player_window)
    entry_last_name.pack(pady=5)

    tk.Label(add_player_window, text="Date of Birth (YYYY-MM-DD)").pack(pady=5)
    entry_dob = tk.Entry(add_player_window)
    entry_dob.pack(pady=5)

    tk.Label(add_player_window, text="Gender").pack(pady=5)
    gender_combobox = ttk.Combobox(add_player_window, values=["Male", "Female"], state="readonly")
    gender_combobox.pack(pady=5)
    gender_combobox.current(0)

    tk.Label(add_player_window, text="Address").pack(pady=5)
    entry_address = tk.Entry(add_player_window)
    entry_address.pack(pady=5)

    tk.Label(add_player_window, text="Phone Number").pack(pady=5)
    entry_phone = tk.Entry(add_player_window)
    entry_phone.pack(pady=5)

    tk.Label(add_player_window, text="Joining Date (YYYY-MM-DD)").pack(pady=5)
    entry_join_date = tk.Entry(add_player_window)
    entry_join_date.pack(pady=5)

    tk.Label(add_player_window, text="Skill Level").pack(pady=5)
    skill_level_combobox= ttk.Combobox(add_player_window, values=["Beginner", "Intermediate","Advanced"], state="readonly")
    skill_level_combobox.pack(pady=5)
    skill_level_combobox.current(0)

    tk.Label(add_player_window, text="Position").pack(pady=5)
    position_combobox = ttk.Combobox(add_player_window, values=["Batsman", "Bowler", "All-rounder"],state="readonly")
    position_combobox.pack(pady=5)
    position_combobox.current(0)

    # Save button
    save_button = tk.Button(add_player_window, text="Save Player", command=save_player)
    save_button.pack(pady=20)

    back_button = tk.Button(add_player_window, text="Back", command=add_player_window.destroy)
    back_button.pack(pady=10)
# Function to view all players
def view_players():
    # View players window
    view_window = tk.Toplevel()
    view_window.title("View Players")
    view_window.geometry("1530x790+0+0")

    # Background image for window
    background_image = Image.open("cric_back.jpg")
    background_image = background_image.resize((1530, 790), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(view_window, image=background_photo)
    background_label.image = background_photo  # Keep a reference to avoid garbage collection
    background_label.place(relwidth=1, relheight=1)

    # Connect to database and fetch player data
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kalpesh@01",
            database="cricket_academy"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT player_id, first_name, last_name, date_of_birth, gender, address, phone_number, joining_date, skill_level, position FROM players")
        players = cursor.fetchall()

        if not players:
            messagebox.showinfo("No Data", "No players found in the database")
            return

        # Create a Listbox to display players
        listbox = tk.Listbox(view_window, width=250, height=40)
        listbox.pack(pady=20)

        # Insert player details into Listbox
        for player in players:
            listbox.insert(tk.END, f"ID: {player[0]}, Name: {player[1]} {player[2]}, DOB: {player[3]}, Gender: {player[4]}, "
                                   f"Address: {player[5]}, Phone: {player[6]}, Joining Date: {player[7]}, "
                                   f"Skill Level: {player[8]}, Position: {player[9]}")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    # Back button to close the window
    back_button = tk.Button(view_window, text="Back", command=view_window.destroy)
    back_button.pack(pady=10)
def manage_players():
    def update_player():
        player_id = entry_player_id.get()
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        dob = entry_dob.get()
        gender = entry_gender.get()
        address = entry_address.get()
        phone = entry_phone.get()
        join_date = entry_join_date.get()
        skill_level = entry_skill_level.get()
        position = entry_position.get()

        # Validate inputs
        if not all([player_id, first_name, last_name, dob, gender, address, phone, join_date, skill_level, position]):
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        # Database connection
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Kalpesh@01",
                database="cricket_academy"
            )
            cursor = conn.cursor()

            # Update query
            update_query = """UPDATE players
                              SET first_name = %s, last_name = %s, date_of_birth = %s, gender = %s,
                                  address = %s, phone_number = %s, joining_date = %s, skill_level = %s, position = %s
                              WHERE player_id = %s"""
            player_data = (first_name, last_name, dob, gender, address, phone, join_date, skill_level, position, player_id)
            cursor.execute(update_query, player_data)
            conn.commit()

            messagebox.showinfo("Success", "Player updated successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        manage_players_window.destroy()

    def delete_player():
        player_id = entry_player_id.get()

        # Validate player ID
        if not player_id:
            messagebox.showwarning("Input Error", "Please enter Player ID to delete.")
            return

        # Delete from database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Kalpesh@01",
                database="cricket_academy"
            )
            cursor = conn.cursor()

            # Delete query
            delete_query = "DELETE FROM players WHERE player_id = %s"
            cursor.execute(delete_query, (player_id,))
            conn.commit()

            messagebox.showinfo("Success", "Player deleted successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        manage_players_window.destroy()

    # Manage players window
    manage_players_window = tk.Toplevel()
    manage_players_window.title("Manage Players")
    manage_players_window.geometry("1530x790+0+0")

    bg_image = Image.open("cric_back.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(manage_players_window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Labels and entry fields for player management
    tk.Label(manage_players_window, text="Player ID (for Update/Delete)").pack(pady=5)
    entry_player_id = tk.Entry(manage_players_window)
    entry_player_id.pack(pady=5)

    tk.Label(manage_players_window, text="First Name").pack(pady=5)
    entry_first_name = tk.Entry(manage_players_window)
    entry_first_name.pack(pady=5)

    tk.Label(manage_players_window, text="Last Name").pack(pady=5)
    entry_last_name = tk.Entry(manage_players_window)
    entry_last_name.pack(pady=5)

    tk.Label(manage_players_window, text="Date of Birth (YYYY-MM-DD)").pack(pady=5)
    entry_dob = tk.Entry(manage_players_window)
    entry_dob.pack(pady=5)

    tk.Label(manage_players_window, text="Gender").pack(pady=5)
    entry_gender = tk.Entry(manage_players_window)
    entry_gender.pack(pady=5)

    tk.Label(manage_players_window, text="Address").pack(pady=5)
    entry_address = tk.Entry(manage_players_window)
    entry_address.pack(pady=5)

    tk.Label(manage_players_window, text="Phone Number").pack(pady=5)
    entry_phone = tk.Entry(manage_players_window)
    entry_phone.pack(pady=5)

    tk.Label(manage_players_window, text="Joining Date (YYYY-MM-DD)").pack(pady=5)
    entry_join_date = tk.Entry(manage_players_window)
    entry_join_date.pack(pady=5)

    tk.Label(manage_players_window, text="Skill Level").pack(pady=5)
    entry_skill_level = tk.Entry(manage_players_window)
    entry_skill_level.pack(pady=5)

    tk.Label(manage_players_window, text="Position").pack(pady=5)
    entry_position = tk.Entry(manage_players_window)
    entry_position.pack(pady=5)

    # Update and Delete buttons
    update_button = tk.Button(manage_players_window, text="Update Player", command=update_player)
    update_button.pack(pady=20)

    delete_button = tk.Button(manage_players_window, text="Delete Player", command=delete_player)
    delete_button.pack(pady=20)

    # Back button
    back_button = tk.Button(manage_players_window, text="Back", command=manage_players_window.destroy)
    back_button.pack(pady=10)

# Player management menu
def player_menu():
    player_window = tk.Toplevel()
    player_window.title("Player Management")
    player_window.geometry("1530x790+0+0")

    # Load the image using Pillow
    bg_image = Image.open("cric_back.jpg")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(player_window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    title_label = tk.Label(player_window, text="Player Management", font=("Arial", 24, "bold"))
    title_label.pack(pady=20)

    # Button to add a new player
    add_player_button = tk.Button(player_window, text="Add Player", font=("Arial", 16), command=add_player, width=20)
    add_player_button.pack(pady=10)

    # Button to view all added players
    view_players_button = tk.Button(player_window, text="View Players", font=("Arial", 16), command=view_players, width=20)
    view_players_button.pack(pady=10)

    # Button to view all added players
    view_players_button = tk.Button(player_window, text="Manage Players", font=("Arial", 16), command=manage_players, width=20)
    view_players_button.pack(pady=10)

    # Back button to close the player management window
    back_button = tk.Button(player_window, text="Back", font=("Arial", 16), command=player_window.destroy, width=20)
    back_button.pack(pady=10)

    player_window.mainloop()

# Ensure that the player menu is launched when this file is run
