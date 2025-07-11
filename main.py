import sqlite3
import ttkbootstrap as ttk
import os
import webbrowser
from ttkbootstrap.tableview import Tableview
from tkinter import messagebox


# Connect to SQLite database
conn = sqlite3.connect('db/quiz.db')
cursor = conn.cursor()

# Initialize the main window with ttkbootstrap style
style = ttk.Style("flatly")
root = style.master
root.title("Trivia Quiz")
root.geometry("1600x900")

# Custom theme colors
root.configure(bg="#FFDAB9")  # Peach Puff background
style.configure('TLabel', font=('Georgia', 24), foreground="#8B4513", background="#FFDAB9")  # Larger font size
style.configure('TRadiobutton', font=('Georgia', 26), foreground="#8B4513", background="#FFDAB9")  # Increased font size for radiobutton
style.configure('TEntry', font=('Georgia', 20), foreground="#8B4513", fieldbackground="#FFDAB9", background="#FFDAB9")  # Larger font size for entry fields

# Custom Button Style
style.configure('Custom.TButton', font=('Georgia', 20), background="#FF8C00", foreground="white", borderwidth=1)
style.map('Custom.TButton', background=[('active', '#E67E00')])  # Slightly darker orange when hovered

style.configure('Blue.TButton', font=('Georgia', 20), background="#1E90FF", foreground="white", borderwidth=1)
style.map('Blue.TButton', background=[('active', '#1C86EE')])  # Slightly darker blue when hovered

style.configure('Red.TButton', font=('Georgia', 20), background="#FF6347", foreground="white", borderwidth=1)
style.map('Red.TButton', background=[('active', '#FF4500')])  # Slightly darker red when hovered

# Function to create custom buttons
def create_custom_button(text, command):
    return ttk.Button(root, text=text, command=command, style="Custom.TButton")


def open_pdf_externally():
    pdf_path = "D:\Vpy\imgs\che.pdf"  # Replace with the actual file path of your PDF
    if os.path.exists(pdf_path):
        # Use webbrowser to open the PDF in the default viewer externally
        webbrowser.open(f'file:///{os.path.abspath(pdf_path)}', new=2)  # Opens in default PDF viewer
    else:
        messagebox.showerror("Error", "PDF file not found!")

# Create the button to open the PDF externally
def show_pdf_button():
    clear_window()  # Clear the window if necessary

    ttk.Label(root, text="Open PDF Document", font=("Georgia", 32), foreground="#8B4513", background="#FFDAB9").pack(pady=20)
    create_custom_button("Open PDF Externally", open_pdf_externally).pack(pady=20)  # Create the button

# Global variables
current_user_id = None
current_question = 0
score = 0
scor=0
questions = []
timer_label = None
time_left = 15
selected_category = None
selected_difficulty = None
timer_id = None

# Helper functions for UI transitions
def clear_window():
    """Clears all widgets from the window."""
    for widget in root.winfo_children():
        widget.destroy()

def show_intro():
    clear_window()

    # Configure styles
    style.configure("Intro.TLabel", font=("Georgia", 40, "bold"), foreground="#8B4513", background="#FFDAB9")
    style.configure("IntroSub.TLabel", font=("Georgia", 18), foreground="#8B4513", background="#FFDAB9")
    style.configure("Red.TButton", font=("Georgia", 12), background="#FF6347", foreground="white", borderwidth=1)
    style.map("Red.TButton", background=[("active", "#E54B3C")])  # Slightly darker red on hover
    style.configure("TFrame", background="#8B4513")  # Dark line color

    # Intro title
    intro_label = ttk.Label(root, text="Trivia Quiz", style="Intro.TLabel")
    intro_label.pack(pady=50)

    # Subtitle/tagline
    tagline_label = ttk.Label(
        root,
        text="Test your knowledge across categories and levels!",
        style="IntroSub.TLabel",
        wraplength=400,
        anchor="center",
    )
    tagline_label.pack(pady=10)

    # Decorative separator (as a line)
    decorative_line = ttk.Frame(root, height=2, style="TFrame")
    decorative_line.pack(fill="x", padx=50, pady=20)

    # Buttons
    create_custom_button("Start", show_login).pack(pady=20)
    create_custom_button("Leaderboard", show_leaderboard).pack(pady=10)
    ttk.Button(root, text="Exit", command=root.quit, style="Red.TButton").pack(pady=10)

    # Additional space at the bottom
    ttk.Label(root, text="", background="#FFDAB9").pack(pady=20)

# Registration logic
def register_user():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            show_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
    else:
        messagebox.showerror("Error", "All fields are required.")

# Login logic
def login_user():
    global current_user_id
    username = username_entry.get()
    password = password_entry.get()

    cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()


    if user:
        current_user_id = user[0]
        messagebox.showinfo("Success", f"Welcome, {username}!")
        show_rules()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

    


# Show rules screen
def show_rules():
    clear_window()

    # Title of the rules screen
    ttk.Label(root, text="Trivia Quiz - Rules and Objectives", font=("Georgia", 32, "bold"), foreground="#8B4513", background="#FFDAB9").pack(pady=20)

    # Display the rules and features
    rules_text = """
    Welcome to the Trivia Quiz!

    - You will have a selection of categories to choose from: Geography, Literature, Science, History.
    - After selecting a category, you will pick a difficulty level: Beginner, Intermediate, or Advanced.
    - You will be presented with questions, and you can choose the correct answer from multiple options.
    - Each correct answer will earn you points based on the difficulty level:
        - Beginner: +1 point
        - Intermediate: +2 points
        - Advanced: +3 points
    - The quiz will include a timer for each question, and you must answer before time runs out.
    - Your final score will be recorded and added to the leaderboard.

    Good luck, and have fun!
    """
    
    ttk.Label(root, text=rules_text, font=("Georgia", 18), foreground="#8B4513", background="#FFDAB9", justify="left", wraplength=900).pack(pady=30)

    # "Next" button to continue
    create_custom_button("Next", show_category_selection).pack(pady=20)
    
    

# Show registration screen
def show_registration():
    clear_window()

    ttk.Label(root, text="Register", font=("Georgia", 32), foreground="#5bc0de", background="#FFDAB9").pack(pady=20)

    global username_entry, password_entry
    ttk.Label(root, text="Username:").pack()
    username_entry = ttk.Entry(root)
    username_entry.pack(pady=10)

    ttk.Label(root, text="Password:").pack()
    password_entry = ttk.Entry(root, show="*")
    password_entry.pack(pady=10)


    ttk.Button(root, text="Register", command=register_user, style="Blue.TButton").pack(pady=20)  # Blue button
    ttk.Button(root, text="Back to Login", command=show_login, style="Blue.TButton").pack(pady=20)  # Blue button
    

# Show login screen
def show_login():
    clear_window()

    ttk.Label(root, text="Login", font=("Georgia", 32), foreground="#8B4513", background="#FFDAB9").pack(pady=20)

    global username_entry, password_entry
    ttk.Label(root, text="Username:").pack()
    username_entry = ttk.Entry(root)
    username_entry.pack(pady=10)

    ttk.Label(root, text="Password:").pack()
    password_entry = ttk.Entry(root, show="*")
    password_entry.pack(pady=10)

    create_custom_button("Login", login_user).pack(pady=20)
    create_custom_button("Register", show_registration).pack(pady=20)
    ttk.Button(root, text="back", command=show_intro, style="Red.TButton").pack(pady=10)  # Red button for Exit
    

# Category selection screen
# Category selection screen
def show_category_selection():
    clear_window()

    ttk.Label(root, text="Select a Category:", font=("Georgia", 28), foreground="#8B4513", background="#FFDAB9").pack(pady=40)

    # Define category descriptions
    category_overviews = {
        "Geography": "Test your knowledge of countries, capitals, landmarks, and more!",
        "Literature": "Questions about famous authors, novels, poems, and literary terms.",
        "Science": "Explore topics in biology, chemistry, physics, and more.",
        "History": "Dive into historical events, people, and milestones from around the world.",
        "Daily Challenge":"Test out yout proficiency in all things General Knowledge"
    }

    # Get the list of categories from the database
    cursor.execute("SELECT DISTINCT category FROM questions")
    categories = [row[0] for row in cursor.fetchall()]

    for category in categories:
        # Display category name as a button
        button = create_custom_button(category, lambda c=category: show_difficulty_selection(c))
        button.pack(pady=10)

        # Display category overview
        overview = category_overviews.get(category, "No overview available for this category.")
        ttk.Label(root, text=overview, font=("Georgia", 16), foreground="#8B4513", background="#FFDAB9").pack(pady=5)

    ttk.Button(root, text="back", command=show_rules, style="Red.TButton").pack(pady=10)  # Red button for Exit


# Difficulty selection screen

def show_difficulty_selection(category):
    global selected_category
    selected_category = category
    clear_window()
    reset_score()

    ttk.Label(root, text="Select Difficulty Level:", font=("Georgia", 28), foreground="#8B4513", background="#FFDAB9").pack(pady=40)

    # Define difficulty descriptions
    difficulty_overviews = {
        "beginner": "Aimed at those new to the topic, earning 1 point for each correct answer.",
        "intermediate": "For players with some experience, earning 2 points for each correct answer.",
        "advanced": "Challenging questions for experts, earning 3 points for each correct answer."
    }

    difficulties = ["beginner", "intermediate", "advanced"]
    for difficulty in difficulties:
        # Display difficulty button
        button = create_custom_button(difficulty.capitalize(), lambda d=difficulty: start_quiz(d))
        button.pack(pady=10)

        # Display difficulty overview
        overview = difficulty_overviews.get(difficulty, "No overview available for this difficulty.")
        ttk.Label(root, text=overview, font=("Georgia", 16), foreground="#8B4513", background="#FFDAB9").pack(pady=5)

    ttk.Button(root, text="back", command=show_category_selection, style="Red.TButton").pack(pady=10)  # Red button for Exit


# Load questions based on category and difficulty
def load_questions(category, difficulty):
    global questions
    cursor.execute("SELECT * FROM questions WHERE category = ? AND difficulty = ?", (category, difficulty))
    questions = cursor.fetchall()

# Quiz functionality
def start_quiz(difficulty):
    global selected_difficulty, current_question, score
    selected_difficulty = difficulty
    current_question = 0
    score = 0
    scor=0
    load_questions(selected_category, selected_difficulty)
    show_quiz()

# Quiz functionality
def show_quiz():
    global current_question, answer_var, time_left, timer_label, timer_id

    clear_window()

    if current_question < len(questions):
        question_text = questions[current_question][1]
        ttk.Label(root, text=f"Category: {selected_category} | Difficulty: {selected_difficulty}", font=("Georgia", 22), foreground="#8B4513").pack(pady=20, anchor="center")
        ttk.Label(root, text=question_text, wraplength=600, font=("Georgia", 22), anchor="center").pack(pady=30)

        options = questions[current_question][2:6]
        answer_var = ttk.IntVar()

        # Center-align radio buttons
        for idx, option in enumerate(options, start=1):
            ttk.Radiobutton(root, text=option, variable=answer_var, value=idx, bootstyle="primary").pack(anchor="center", pady=10)

        # Timer display
        timer_label = ttk.Label(root, text=f"Time Left: {time_left} seconds", font=("Georgia", 18), foreground="red")
        timer_label.pack(pady=20, anchor="center")
        start_timer()

        create_custom_button("Next", next_question).pack(pady=30, anchor="center")
    else:
        submit_quiz()

def start_timer():
    global time_left, timer_label, timer_id
    time_left = 15  # Reset the timer for each question

    # Cancel any existing timer
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

    update_timer()

def update_timer():
    global time_left, timer_label, timer_id
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time Left: {time_left} seconds")
        timer_id = root.after(1000, update_timer)
    else:
        timer_label.config(text="Time's up!")
        next_question()

def next_question():
    global current_question, score, scor

    selected_option = answer_var.get()
    correct_option = questions[current_question][6]

    if selected_option == correct_option:
        if selected_difficulty == "beginner":
            scor += 1
        elif selected_difficulty == "intermediate":
            scor += 1
        elif selected_difficulty == "advanced":
            scor += 1

    if selected_option == correct_option:
        if selected_difficulty == "beginner":
            score += 1
        elif selected_difficulty == "intermediate":
            score += 2
        elif selected_difficulty == "advanced":
            score += 3

    current_question += 1
    show_quiz()

def reset_score():
    global scor
    scor=0

def submit_quiz():
    save_score()
    show_final_score()

def save_score():
    global current_user_id, score,scor
    cursor.execute("INSERT INTO scores (user_id, score) VALUES (?, ?)", (current_user_id, score))
    conn.commit()

def show_final_score():
    clear_window()
    ttk.Label(root, text=f"Quiz Finished! Your Score: {scor}/{len(questions)}", font=("Georgia", 28), foreground="#8B4513", background="#FFDAB9").pack(pady=40)
    ttk.Button(root, text="Check Leaderboards", command=show_leaderboard, style="Blue.TButton").pack(pady=20)  # Blue button
    create_custom_button("Solutions", open_pdf_externally).pack(pady=20)  # Opens PDF externally
    ttk.Button(root, text="Take Another Quiz", command=show_category_selection, style="Blue.TButton").pack(pady=20)  # Blue button
    ttk.Button(root, text="Back to Main", command=show_intro, style="Blue.TButton").pack(pady=20)  # Blue button
    ttk.Button(root, text="Exit", command=root.quit, style="Red.TButton").pack(pady=10)  # Red button for Exit
    

# Leaderboard functionality
def show_leaderboard():
    clear_window()

    cursor.execute(''' 
        SELECT u.username, SUM(s.score) as total_score
        FROM users u
        JOIN scores s ON u.user_id = s.user_id
        GROUP BY u.user_id
        ORDER BY total_score DESC
        LIMIT 10
    ''')
    leaderboard = cursor.fetchall()

    ttk.Label(root, text="Leaderboard", font=("Georgia", 28), foreground="#8B4513", background="#FFDAB9").pack(pady=20)

    leaderboard_table = Tableview(
        root,
        coldata=["Rank", "Username", "Total Score"],
        rowdata=[(idx + 1, row[0], row[1]) for idx, row in enumerate(leaderboard)],
        bootstyle="info",
        paginated=True,
    )
    leaderboard_table.pack(pady=20)
    ttk.Button(root, text="Back to Main", command=show_intro, style="Blue.TButton").pack(pady=20)  # Blue button
    ttk.Button(root, text="back", command=show_final_score, style="Red.TButton").pack(pady=10)  # Red button for Exit



    

# Start the application with the intro screen
show_intro()
root.mainloop()
