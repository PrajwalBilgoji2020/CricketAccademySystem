import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector

# Function to go back to the main menu
def back_to_menu(window):
    window.destroy()

# Function to add a new team
def add_team():
    def save_team():
        team_name = entry_team_name.get()
        age_group = age_group_combobox.get()
        coach_id = entry_coach_id.get()
        captain_id = entry_captain_id.get()

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
            insert_query = """INSERT INTO teams (team_name, age_group, coach_id, team_captain)
                              VALUES (%s, %s, %s, %s)"""
            team_data = (team_name, age_group, coach_id, captain_id)
            cursor.execute(insert_query, team_data)
            conn.commit()

            messagebox.showinfo("Success", "Team added successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        add_team_window.destroy()

    # Add team window
    add_team_window = tk.Toplevel()
    add_team_window.title("Add New Team")
    add_team_window.geometry("1530x790+0+0")

    # Background Image
    bg_image = Image.open("cric_back.jpg")  # Path to your background image
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(add_team_window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Labels and entry fields for team details
    tk.Label(add_team_window, text="Team Name").pack(pady=5)
    entry_team_name = tk.Entry(add_team_window)
    entry_team_name.pack(pady=5)

    tk.Label(add_team_window, text="Age Group").pack(pady=5)
    age_group_combobox = ttk.Combobox(add_team_window, values=["U-15", "U-19", "Senior"], state="readonly")
    age_group_combobox.pack(pady=5)
    age_group_combobox.current(0)

    tk.Label(add_team_window, text="Coach ID").pack(pady=5)
    entry_coach_id = tk.Entry(add_team_window)
    entry_coach_id.pack(pady=5)

    tk.Label(add_team_window, text="Team Captain (Player ID)").pack(pady=5)
    entry_captain_id = tk.Entry(add_team_window)
    entry_captain_id.pack(pady=5)

    # Save button
    save_button = tk.Button(add_team_window, text="Save Team", command=save_team)
    save_button.pack(pady=20)

    back_button = tk.Button(add_team_window, text="Back", command=add_team_window.destroy)
    back_button.pack(pady=10)

    # Keep reference to background image
    add_team_window.bg_image = bg_image

# Function to view all teams
def view_teams():
    def fetch_teams():
        # Fetch team data from the database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Replace with your MySQL username
                password="Kalpesh@01",  # Replace with your MySQL password
                database="cricket_academy"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM teams")
            teams = cursor.fetchall()

            for row in teams:
                team_list.insert("", tk.END, values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # View teams window
    view_teams_window = tk.Toplevel()
    view_teams_window.title("View Teams")
    view_teams_window.geometry("1530x790+0+0")

    # Background Image
    bg_image = Image.open("cric_back.jpg")  # Path to your background image
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(view_teams_window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    columns = ("Team ID", "Team Name", "Age Group", "Coach ID", "Team Captain")
    team_list = ttk.Treeview(view_teams_window, columns=columns, show="headings")

    for col in columns:
        team_list.heading(col, text=col)

    team_list.pack(fill=tk.BOTH, expand=True)

    # Fetch data
    fetch_teams()

    back_button = tk.Button(view_teams_window, text="Back", command=view_teams_window.destroy)
    back_button.pack(pady=10)

    # Keep reference to background image
    view_teams_window.bg_image = bg_image

# Function to manage teams (including editing and deleting)
def manage_teams():
    def update_team():
        team_id = entry_team_id.get()
        team_name = entry_team_name.get()
        age_group = age_group_combobox.get()
        coach_id = entry_coach_id.get()
        captain_id = entry_captain_id.get()

        # Check if any field is empty
        if not team_id or not team_name or not age_group or not coach_id or not captain_id:
            messagebox.showerror("Input Error", "All fields must be filled!")
            return

        # Update database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Replace with your MySQL username
                password="Kalpesh@01",  # Replace with your MySQL password
                database="cricket_academy"
            )
            cursor = conn.cursor()

            # Update query
            update_query = """UPDATE teams
                              SET team_name = %s, age_group = %s, coach_id = %s, team_captain = %s
                              WHERE team_id = %s"""
            team_data = (team_name, age_group, coach_id, captain_id, team_id)
            cursor.execute(update_query, team_data)
            conn.commit()

            messagebox.showinfo("Success", "Team updated successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        manage_teams_window.destroy()

    def delete_team():
        team_id = entry_team_id.get()

        # Check if team ID is empty
        if not team_id:
            messagebox.showerror("Input Error", "Team ID must be filled!")
            return

        # Delete from database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Replace with your MySQL username
                password="Kalpesh@01",  # Replace with your MySQL password
                database="cricket_academy"
            )
            cursor = conn.cursor()

            # Delete query
            delete_query = "DELETE FROM teams WHERE team_id = %s"
            cursor.execute(delete_query, (team_id,))
            conn.commit()

            messagebox.showinfo("Success", "Team deleted successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        manage_teams_window.destroy()

    # Manage teams window
    manage_teams_window = tk.Toplevel()
    manage_teams_window.title("Manage Teams")
    manage_teams_window.geometry("1530x790+0+0")

    # Background Image
    bg_image = Image.open("cric_back.jpg")  # Path to your background image
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(manage_teams_window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(manage_teams_window, text="Team ID").pack(pady=5)
    entry_team_id = tk.Entry(manage_teams_window)
    entry_team_id.pack(pady=5)

    tk.Label(manage_teams_window, text="Team Name").pack(pady=5)
    entry_team_name = tk.Entry(manage_teams_window)
    entry_team_name.pack(pady=5)

    tk.Label(manage_teams_window, text="Age Group").pack(pady=5)
    age_group_combobox = ttk.Combobox(manage_teams_window, values=["U-15", "U-19", "Senior"], state="readonly")
    age_group_combobox.pack(pady=5)
    age_group_combobox.current(0)

    tk.Label(manage_teams_window, text="Coach ID").pack(pady=5)
    entry_coach_id = tk.Entry(manage_teams_window)
    entry_coach_id.pack(pady=5)

    tk.Label(manage_teams_window, text="Team Captain (Player ID)").pack(pady=5)
    entry_captain_id = tk.Entry(manage_teams_window)
    entry_captain_id.pack(pady=5)

    # Update and Delete buttons
    update_button = tk.Button(manage_teams_window, text="Update Team", command=update_team)
    update_button.pack(pady=10)

    delete_button = tk.Button(manage_teams_window, text="Delete Team", command=delete_team)
    delete_button.pack(pady=10)

    back_button = tk.Button(manage_teams_window, text="Back", command=manage_teams_window.destroy)
    back_button.pack(pady=10)

    # Keep reference to background image
    manage_teams_window.bg_image = bg_image

# Function to open the team management window
def open_team_management():
    team_management_window = tk.Toplevel()
    team_management_window.title("Team Management")
    team_management_window.geometry("1530x790+0+0")

    # Background Image
    bg_image = Image.open("cric_back.jpg")  # Path to your background image
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(team_management_window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    title_label = tk.Label(team_management_window, text="Team Management", font=("Arial", 24, "bold"))
    title_label.pack(pady=20)

    # Buttons for team management
    tk.Button(team_management_window, text="Add Team", command=add_team, width=20).pack(pady=10)
    tk.Button(team_management_window, text="View Teams", command=view_teams, width=20).pack(pady=10)
    tk.Button(team_management_window, text="Manage Teams", command=manage_teams, width=20).pack(pady=10)
    tk.Button(team_management_window, text="Back", command=lambda: back_to_menu(team_management_window), width=20).pack(pady=10)

    # Keep reference to background image
    team_management_window.bg_image = bg_image
