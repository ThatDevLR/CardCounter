import tkinter as tk

# Define the card values
card_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0, '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

# Initialize the running count
running_count = 0

# Function to update the running count and display it
def update_count(card):
    global running_count
    if card in card_values:
        running_count += card_values[card]
        count_label.config(text=f"Running Count: {running_count}")

# Function to handle user input
def input_card():
    card = entry.get().upper()
    update_count(card)
    entry.delete(0, tk.END)

# Create the main GUI window
root = tk.Tk()
root.title("Blackjack Card Counting Simulator")

# Create a label to display the running count
count_label = tk.Label(root, text=f"Running Count: {running_count}")
count_label.pack()

# Create an entry field for user input
entry = tk.Entry(root, width=10)
entry.pack()

# Create a button to submit user input
submit_button = tk.Button(root, text="Submit", command=input_card)
submit_button.pack()

# Start the GUI main loop
root.mainloop()
