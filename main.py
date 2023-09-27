import tkinter as tk
import random

# Define the card values
card_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0, '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

# Initialize the running count
running_count = 0

# Initialize the number of players (including the dealer)
num_players = 0

# Initialize the decks of cards
decks = []

# Initialize hands for the dealer and players
dealer_hand = []
player_hands = []

# Initialize labels
count_label = None
card_entry = None
players_entry = None
start_button = None
dealer_label = None
player_labels = []

# Initialize buttons for player actions
hit_button = None
stand_button = None

# Initialize the dealer's turn state
dealer_turn = False

cards_dealt = 0  # Track the number of cards dealt

# Function to create the blackjack game display
def create_game_display(num_players):
    global dealer_label, player_labels, hit_button, stand_button, count_label  # Add count_label

    # Destroy the existing widgets
    count_label.pack_forget()
    card_entry.pack_forget()
    card_button.pack_forget()
    players_label.pack_forget()
    players_entry.pack_forget()
    start_button.pack_forget()

    # Initialize the decks of cards
    decks.extend(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4)

    # Shuffle the decks of cards
    random.shuffle(decks)

    # Create a label for the game simulation
    game_label = tk.Label(root, text="Blackjack Game Simulation")
    game_label.pack()

    # Create a label to display the number of players
    player_count_label = tk.Label(root, text=f"Number of Players: {num_players}")
    player_count_label.pack()

    # Create a label for the running count
    count_label = tk.Label(root, text=f"Running Count: {running_count}")
    count_label.pack()

    # Deal two cards to each player and the dealer
    for _ in range(2):
        dealer_hand.append(deal_card())
        player_hands.append([deal_card() for _ in range(num_players)])

    # Create labels for the dealer's hand and players' hands
    dealer_label = tk.Label(root, text="Dealer's Hand: " + dealer_hand[0] + " ?")
    dealer_label.pack()

    player_labels = [tk.Label(root, text=f"Player {i + 1}'s Hand: {', '.join(player_hands[i])}") for i in range(num_players)]
    for label in player_labels:
        label.pack()

    # Create buttons for player actions
    hit_button = tk.Button(root, text="Hit", command=player_hit)
    stand_button = tk.Button(root, text="Stand", command=player_stand)
    hit_button.pack()
    stand_button.pack()

    # Disable hit and stand buttons initially
    hit_button.config(state=tk.DISABLED)
    stand_button.config(state=tk.DISABLED)

def input_card():
    card = card_entry.get().upper()
    update_count(card)
    card_entry.delete(0, tk.END)

# Function to start the blackjack simulation
def start_simulation():
    global num_players, players_entry, start_button, hit_button, stand_button, dealer_turn
    num_players = int(players_entry.get())
    if num_players >= 1:
        players_entry.config(state=tk.DISABLED)
        start_button.config(state=tk.DISABLED)
        create_game_display(num_players)
        dealer_turn = False
        hit_button.config(state=tk.DISABLED)
        stand_button.config(state=tk.DISABLED)
        player_turn()

# Function for player's turn
def player_turn():
    global dealer_turn
    dealer_label.config(text="Dealer's Hand: " + dealer_hand[0] + " ?")
    if not dealer_turn:
        player_labels[0].config(text=f"Player 1's Hand: {', '.join(player_hands[0])}")
        hit_button.config(state=tk.NORMAL)
        stand_button.config(state=tk.NORMAL)
    else:
        dealer_turn = True
        dealer_play()
        update_count(dealer_hand[1])

# Function for player to hit
def player_hit():
    global player_labels
    # Deal a card to the current player
    new_card = deal_card()
    player_hands[0].append(new_card)

    # Update the display for the current player
    player_labels[0].config(text=f"Player 1's Hand: {', '.join(player_hands[0])}")

    # Check for bust
    if get_hand_value(player_hands[0]) > 21:
        end_game("Player 1 busts!")
    else:
        update_count(new_card)  # Update count after hitting

# Function for player to stand
def player_stand():
    global dealer_turn
    hit_button.config(state=tk.DISABLED)
    stand_button.config(state=tk.DISABLED)
    dealer_turn = True
    dealer_play()

# Function for dealer's turn
def dealer_play():
    global dealer_turn
    dealer_label.config(text="Dealer's Hand: " + ', '.join(dealer_hand))
    while get_hand_value(dealer_hand) < 17:
        new_card = deal_card()
        dealer_hand.append(new_card)
        update_count(new_card)  # Update count after dealer draws a card
    determine_winner()

# Function to simulate dealing a card
def deal_card():
    global cards_dealt
    if cards_dealt >= len(decks) * 0.75:
        # If more than 75% of the cards have been dealt, reshuffle
        random.shuffle(decks)
        cards_dealt = 0
    card = decks.pop()
    cards_dealt += 1
    return card

# Function to update the running count and display it
def update_count(card):
    global running_count, count_label  # Ensure count_label is global
    if card in card_values:
        running_count += card_values[card]
        count_label.config(text=f"Running Count: {running_count}")

# Function to determine the winner
# Function to determine the winner
# Function to determine the winner
def determine_winner():
    dealer_value = get_hand_value(dealer_hand)
    player_values = [get_hand_value(hand) for hand in player_hands]

    winners = []

    for i, value in enumerate(player_values):
        if value > 21:
            continue  # Player has busted
        if value <= 21 and (dealer_value > 21 or value > dealer_value):
            winners.append(f"Player {i + 1}")
        elif value <= 21 and dealer_value == value:
            winners.append(f"Player {i + 1}")

    if dealer_value > 21:
        winners.append("Dealer")
    elif all(value > 21 for value in player_values):
        winners.append("Dealer")

    if winners:
        end_game(f"{', '.join(winners)} win{'s' if len(winners) > 1 else ''}!")
    else:
        end_game("It's a tie!")


# Function to get the value of a hand
def get_hand_value(hand):
    value = sum(card_values[card] for card in hand)
    num_aces = hand.count('A')

    # Handle aces as 11 if it doesn't bust the hand
    while num_aces > 0 and value <= 11:
        value += 10
        num_aces -= 1

    return value

# Function to end the game
def end_game(message):
    end_label = tk.Label(root, text=message)
    end_label.pack()
    restart_button = tk.Button(root, text="Restart", command=restart_simulation)
    restart_button.pack()

# Function to restart the simulation
def restart_simulation():
    global running_count, num_players, decks, dealer_hand, player_hands, count_label, card_entry, players_entry, start_button, dealer_label, player_labels
    running_count = 0
    num_players = 0
    decks = []
    dealer_hand = []
    player_hands = []
    count_label.config(text=f"Running Count: {running_count}")
    count_label.pack()
    card_entry.pack()
    card_button.pack()
    players_label.pack()
    players_entry.delete(0, tk.END)
    players_entry.config(state=tk.NORMAL)
    players_entry.pack()
    start_button.config(state=tk.NORMAL)
    start_button.pack()
    dealer_label = None
    player_labels = []
    root.quit()

# Create the main GUI window
root = tk.Tk()
root.title("Blackjack Card Counting Simulator")

# Create an entry field for user input of a card
card_entry = tk.Entry(root, width=10)
card_entry.pack()

# Create a button to submit user input of a card
card_button = tk.Button(root, text="Submit Card", command=input_card)
card_button.pack()

# Create a label for the number of players
players_label = tk.Label(root, text="Enter the number of players (including the dealer):")
players_label.pack()

# Create an entry field for user input of the number of players
players_entry = tk.Entry(root, width=5)
players_entry.pack()

# Create a button to start the blackjack simulation
start_button = tk.Button(root, text="Start Simulation", command=start_simulation)
start_button.pack()

# Create a label to display the running count
count_label = tk.Label(root, text=f"Running Count: {running_count}")
count_label.pack()

# Start the GUI main loop
root.mainloop()
