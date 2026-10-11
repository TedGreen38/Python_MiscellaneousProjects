import random
import tkinter as tk

# Constants for the game of rock, paper, scissors
CHOICES = ("Rock", "Paper", "Scissors")

# game rules of what beats what in rock, paper, scissors
BEATS = {
	"Rock": "Scissors",
	"Paper": "Rock",
	"Scissors": "Paper",
}

# main class for the Rock, Paper, Scissors game app
class RockPaperScissorsApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Rock, Paper, Scissors")
		self.root.resizable(False, False)

        # stores the scores of the players wins and losses for this session.
		self.scores = {"Wins": 0, "Losses": 0, "Ties": 0}
		self.score_values = {}

        # displays the label "Choose your move"
		tk.Label(root, text="Choose your move", font=("Arial", 16, "bold")).pack(pady=(16, 8))

        # displays each choice as a button, when any are pressed, calls the play method.
		button_frame = tk.Frame(root)
		button_frame.pack(padx=12)
		for choice in CHOICES:
			tk.Button(
				button_frame,
				text=choice,
				width=10,
				command=lambda selected=choice: self.play(selected),
			).pack(side=tk.LEFT, padx=4)

        # initial result label when the app is initialized.
		self.result = tk.Label(root, text="Make a choice to start playing.", font=("Arial", 11), height=2)
		self.result.pack(padx=12, pady=12)

        # ui elements that display the wins, losses, and ties of the current session.
		score_frame = tk.Frame(root)
		score_frame.pack(padx=12, pady=(0, 16))
		for column, name in enumerate(self.scores):
			tk.Label(score_frame, text=name, font=("Arial", 10)).grid(row=0, column=column, padx=16)
			value = tk.Label(score_frame, text="0", font=("Arial", 16, "bold"))
			value.grid(row=1, column=column, padx=16)
			self.score_values[name] = value

    # gameplay loop for a round of Rock, Paper, Scissors.
	def play(self, user_choice):
		computer_choice = random.choice(CHOICES)

        # determine the outcome of the round and modify the outcome and score_name values to reflect the result.
		if user_choice == computer_choice:
			outcome, score_name = "It's a tie!", "Ties"
		elif BEATS[user_choice] == computer_choice:
			outcome, score_name = "You win!", "Wins"
		else:
			outcome, score_name = "Computer wins!", "Losses"

        # updates the values displayed for each score category and display the result message for the round.
		self.scores[score_name] += 1
		self.score_values[score_name].config(text=str(self.scores[score_name]))
		self.result.config(
			text=f"You chose {user_choice}; computer chose {computer_choice}.\n{outcome}"
		)

# main function that initializes the game window and starts the main loop.
if __name__ == "__main__":
	window = tk.Tk()
	RockPaperScissorsApp(window)
	window.mainloop()
