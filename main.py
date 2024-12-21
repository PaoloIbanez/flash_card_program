BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
from tkinter import messagebox
import pandas
import random

# ---------------------------- Flash Cards ------------------------------- #

# data = pandas.read_csv("data/french_words.csv")
# to_learn = data.to_dict(orient="records")
# Global variables
to_learn = []
current_card = {}
flip_timer = None
# Load Data
try:
    data = pandas.read_csv("data/words_to_learn.csv")
    to_learn = data.to_dict(orient="records")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    # If there was no FileNotFoundError, then we successfully read from words_to_learn.csv
    to_learn = data.to_dict(orient="records")

def load_data():
    global to_learn
    data = pandas.read_csv("data/french_words.csv")
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer

    # Cancel the previous timer if it exists
    window.after_cancel(flip_timer)

    # 1. Pick a random pair from the list
    current_card = random.choice(to_learn)

    # 2. Update the canvas text
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    # Also switch the card image if needed (front card)
    canvas.itemconfig(card_background, image=card_front_img)

    # Schedule the flip in 3 seconds
    flip_timer = window.after(3000, flip_card)
def is_known():
    global to_learn
    # Remove the known card from the list so it won't repeat
    to_learn.remove(current_card)
    # Save the updated list to words_to_learn.csv
    data_to_save = pandas.DataFrame(to_learn)
    data_to_save.to_csv("data/words_to_learn.csv", index=False)

    next_card()


# flip the cards

def flip_card():
    # Switch to back image
    canvas.itemconfig(card_background, image=card_back_img)
    # Change the title to "English" and text color to white
    canvas.itemconfig(card_title, text="English", fill="white")
    # Change the word to the English version
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")





# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Learning Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=lambda: None)  # Placeholder

canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)

# Text for the language (smaller font, near the top of the card)
card_title = canvas.create_text(
    400,
    150,
    text="French",
    font=("Ariel", 40, "italic")
)

# Text for the actual word (larger font, in the center)
card_word = canvas.create_text(
    400,
    263,
    text="trouve",
    font=("Ariel", 60, "bold")
)
canvas.grid(row=0, column=0, columnspan=2)

# buttons

right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")

known_button = Button(
    image=right_image,
    highlightthickness=0,
    command=is_known
)
unknown_button = Button(
    image=wrong_image,
    highlightthickness=0,
    command=next_card
)
unknown_button.grid(row=1, column=0)
known_button.grid(row=1, column=1)

next_card()







window.mainloop()