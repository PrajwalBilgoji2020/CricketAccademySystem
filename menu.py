import tkinter as tk
from PIL import Image, ImageTk
from player_management import player_menu
from coach_management import open_coach_management
from training_sessions import training_menu
from team_management import open_team_management
from facility_management import facility_menu
from fees_payments import open_fees_management
from attendance_records import attendance_menu

def main_menu():
    root = tk.Tk()
    root.title("Cricket Academy Management System")
    root.geometry("1530x790+0+0")

    # Load and set the background image
    background_image = Image.open("cric_back.jpg")
    background_image = background_image.resize((1530, 790), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # Title Label
    title_label = tk.Label(root, text="Cricket Academy Management System", font=("Arial", 30, "bold"), bg="lightblue")
    title_label.pack(pady=20)

    # Create buttons for each module
    player_button = tk.Button(root, text="Player Management", font=("Arial", 18), command=player_menu, width=20)
    player_button.pack(pady=10)

    coach_button = tk.Button(root, text="Coach Management", font=("Arial", 18), command=open_coach_management, width=20)
    coach_button.pack(pady=10)

    training_button = tk.Button(root, text="Training Sessions", font=("Arial", 18), command=training_menu, width=20)
    training_button.pack(pady=10)

    team_button = tk.Button(root, text="Team Management", font=("Arial", 18), command=open_team_management, width=20)
    team_button.pack(pady=10)

    facility_button = tk.Button(root, text="Facility Management", font=("Arial", 18), command=facility_menu, width=20)
    facility_button.pack(pady=10)

    fees_button = tk.Button(root, text="Fees and Payments", font=("Arial", 18), command=open_fees_management, width=20)
    fees_button.pack(pady=10)

    attendance_button = tk.Button(root, text="Attendance Records", font=("Arial", 18), command=attendance_menu, width=20)
    attendance_button.pack(pady=10)

    # Start the Tkinter loop
    root.mainloop()

# Ensure that the main menu is launched if this file is run directly
if __name__ == "__main__":
    main_menu()
