# Import necessary modules
import tkinter as tk                      # GUI toolkit
from tkinter import messagebox            # For showing popup dialogs
import random                             # For shuffling questions

# --------------------- QUIZ QUESTIONS DATA ---------------------
# List of dictionaries, each representing a quiz question
questions_data = [
    {
        "question": "What is the correct file extension for Python files?",
        "options": [".pyt", ".pt", ".py", ".python"],
        "answer": 2
    },
    {
        "question": "Which of the following is a valid variable name in Python?",
        "options": ["2value", "value_2", "value-2", "value 2"],
        "answer": 1
    },
    {
        "question": "What is the output of print(2 ** 3)?",
        "options": ["6", "8", "9", "5"],
        "answer": 1
    },
    {
        "question": "Which of the following data types is immutable in Python?",
        "options": ["List", "Dictionary", "Set", "Tuple"],
        "answer": 3
    },
    {
        "question": "What does len(\"Hello\") return?",
        "options": ["4", "5", "6", "Error"],
        "answer": 1
    },
    {
        "question": "What is the keyword used to define a function in Python?",
        "options": ["func", "define", "def", "function"],
        "answer": 2
    },
    {
        "question": "Which of the following is used to take input from the user?",
        "options": ["read()", "input()", "scan()", "get()"],
        "answer": 1
    },
    {
        "question": "Which loop is used when the number of iterations is known?",
        "options": ["while loop", "repeat loop", "for loop", "do-while loop"],
        "answer": 2
    },
    {
        "question": "What is the output of print(type(5.0))?",
        "options": ["<class 'int'>", "<class 'float'>", "<class 'double'>", "<class 'str'>"],
        "answer": 1
    },
    {
        "question": "Which of the following is used to handle exceptions in Python?",
        "options": ["catch", "try-except", "error-check", "raise"],
        "answer": 1
    },
    {
        "question": "Which keyword is used to start a class definition in Python?",
        "options": ["define", "function", "class", "object"],
        "answer": 2
    },
    {
        "question": "What is the default value of a variable that is not initialized in Python?",
        "options": ["0", "null", "undefined", "It causes an error"],
        "answer": 3
    },
    {
        "question": "Which of the following operators is used for floor division in Python?",
        "options": ["/", "//", "%", "**"],
        "answer": 1
    },
    {
        "question": "What is the correct way to import a module in Python?",
        "options": ["use math", "include math", "import math", "require math"],
        "answer": 2
    },
    {
        "question": "Which function is used to get the length of a list?",
        "options": ["length()", "size()", "count()", "len()"],
        "answer": 3
    },
    {
        "question": "How do you start a comment in Python?",
        "options": ["//", "#", "/*", "--"],
        "answer": 1
    },
    {
        "question": "Which data structure allows duplicate values in Python?",
        "options": ["Set", "Tuple", "Dictionary keys", "List"],
        "answer": 3
    },
    {
        "question": "Which method can be used to convert a string to lowercase?",
        "options": ["lowercase()", "toLower()", "lower()", "convertLower()"],
        "answer": 2
    },
    {
        "question": "What does the 'break' statement do in a loop?",
        "options": ["Skips to next iteration", "Stops the loop", "Restarts the loop", "Continues indefinitely"],
        "answer": 1
    },
    {
        "question": "Which function can be used to generate a range of numbers?",
        "options": ["numbers()", "range()", "list()", "generate()"],
        "answer": 1
    }
]


# --------------------- GLOBAL VARIABLES ---------------------
questions = []          # Will hold shuffled questions
current_q = 0           # Current question index
score = 0               # Tracks correct answers
time_left = 30          # Time remaining for current question
timer_id = None         # Used to cancel/reset the timer

# --------------------- TKINTER GUI SETUP ---------------------
root = tk.Tk()                           # Create main window
root.title("Python Quiz Game")          # Set window title
root.geometry("500x450")                # Set window size

# Label to show the current question
question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=450, justify="left")
question_label.pack(pady=20)

# Label to show the countdown timer
timer_label = tk.Label(root, text="Time left: 30", font=("Arial", 12), fg="red")
timer_label.pack()

# Tkinter variable to hold selected radio button (option)
selected_option = tk.IntVar()

# Create and place 4 radio buttons for answer options
option_buttons = []
for i in range(4):
    btn = tk.Radiobutton(
        root,
        text="",                       # Will be filled dynamically
        variable=selected_option,     # Connected to `selected_option`
        value=i,                      # Value = option index
        font=("Arial", 12),
        anchor="w",
        justify="left"
    )
    btn.pack(fill="x", padx=50, pady=2)
    option_buttons.append(btn)

# --------------------- FUNCTION TO LOAD QUESTIONS ---------------------
def load_question():
    """
    Load the current question and options onto the screen.
    Also reset timer and start countdown.
    """
    global time_left, timer_id
    time_left = 30                      # Reset timer to 30 seconds
    update_timer_label()               # Update label text
    if timer_id:                       # Cancel any existing timer
        root.after_cancel(timer_id)
    start_timer()                      # Start countdown again

    question = questions[current_q]    # Get current question dictionary
    question_label.config(text=f"Q{current_q + 1}: {question['question']}")
    selected_option.set(-1)            # Deselect any previously selected option

    # Load options text into radio buttons
    for i, option in enumerate(question["options"]):
        option_buttons[i].config(text=option)

# --------------------- FUNCTION TO UPDATE TIMER DISPLAY ---------------------
def update_timer_label():
    timer_label.config(text=f"Time left: {time_left}")

# --------------------- FUNCTION TO START/UPDATE TIMER ---------------------
def start_timer():
    """
    Decrease time every second and auto-move to next question when time runs out.
    """
    global time_left, timer_id
    if time_left > 0:
        time_left -= 1
        update_timer_label()
        timer_id = root.after(1000, start_timer)  # Call this function again in 1 second
    else:
        messagebox.showinfo("Time's up!", "You ran out of time for this question.")
        next_question(timed_out=True)  # Skip to next question if time is up

# --------------------- FUNCTION TO MOVE TO NEXT QUESTION ---------------------
def next_question(timed_out=False):
    """
    Handle answer validation and move to next question.
    If timed_out=True, skip score check.
    """
    global current_q, score, timer_id

    if timer_id:
        root.after_cancel(timer_id)    # Stop the countdown

    # Only validate answer if user clicked Next (not if time ran out)
    if not timed_out:
        if selected_option.get() == -1:
            messagebox.showwarning("No Selection", "Please select an option before proceeding.")
            return
        if selected_option.get() == questions[current_q]["answer"]:
            score += 1

    current_q += 1                     # Go to next question

    if current_q < len(questions):
        load_question()               # Load next question
    else:
        # Quiz complete: show score and restart button
        messagebox.showinfo("Quiz Completed", f"You scored {score} out of {len(questions)}.")
        restart_btn.pack(pady=10)
        next_btn.config(state="disabled")  # Disable next button

# --------------------- FUNCTION TO RESTART QUIZ ---------------------
def restart_quiz():
    """
    Reset everything and start the quiz again.
    """
    global current_q, score, questions, timer_id
    current_q = 0                     # Reset question index
    score = 0                         # Reset score
    questions = random.sample(questions_data, len(questions_data))  # Shuffle questions
    next_btn.config(state="normal")  # Re-enable Next button
    restart_btn.pack_forget()        # Hide Restart button
    load_question()                  # Load first question

# --------------------- BUTTONS ---------------------

# "Next" button to go to the next question
next_btn = tk.Button(root, text="Next", command=next_question,
                     font=("Arial", 12), bg="#4CAF50", fg="white")
next_btn.pack(pady=20)

# "Restart" button to restart the quiz (initially hidden)
restart_btn = tk.Button(root, text="Restart", command=restart_quiz,
                        font=("Arial", 12), bg="#2196F3", fg="white")

# --------------------- START THE QUIZ ---------------------
restart_quiz()        # Begin the quiz for the first time

# Start Tkinter event loop (keeps window open)
root.mainloop()
