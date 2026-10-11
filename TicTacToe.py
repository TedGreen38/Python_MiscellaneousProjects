import random
import tkinter as tk


# Create the game window, draw the board, and coordinate each round.
class TicTacToe:
	# Colors used to distinguish the players and computer.
	BLUE = "#1565c0"
	RED = "#d32f2f"
	# Every possible row, column, or diagonal that can win a round.
	WINNING_LINES = (
		(0, 1, 2), (3, 4, 5), (6, 7, 8),
		(0, 3, 6), (1, 4, 7), (2, 5, 8),
		(0, 4, 8), (2, 4, 6),
	)

	def __init__(self, root):
		# Configure the main window and initialize the game and score state.
		self.root = root
		root.title("Tic-Tac-Toe")
		root.resizable(False, False)
		root.configure(bg="#f3f5f7")

		self.board = [""] * 9
		self.wins = 0
		self.losses = 0
		self.ties = 0
		self.game_over = False

		# Add the title and a status message above the playing grid.
		tk.Label(root, text="Tic-Tac-Toe", font=("Arial", 24, "bold"),
				 bg="#f3f5f7", fg="#263238").pack(pady=(16, 4))
		self.status = tk.Label(root, text="Your turn (O)", font=("Arial", 12),
							   bg="#f3f5f7", fg="#37474f")
		self.status.pack(pady=(0, 12))

		# Build nine buttons; each button calls user_move for its board position.
		grid = tk.Frame(root, bg="#263238", padx=3, pady=3)
		grid.pack(padx=18)
		self.buttons = []
		for index in range(9):
			button = tk.Button(
				grid, text="", font=("Arial", 32, "bold"), width=3, height=1,
				bg="white", activebackground="#e8eef3", relief="flat",
				command=lambda spot=index: self.user_move(spot),
			)
			button.grid(row=index // 3, column=index % 3, padx=2, pady=2)
			self.buttons.append(button)

		# Display the round totals and provide a control to start another round.
		self.score = tk.Label(
			root, text="Wins: 0    Losses: 0    Ties: 0",
			font=("Arial", 11, "bold"), bg="#f3f5f7", fg="#37474f",
		)
		self.score.pack(pady=(14, 8))
		tk.Button(root, text="New round", command=self.new_round).pack(pady=(0, 14))

	def user_move(self, index):
		# Ignore invalid turns, place the user's mark, then check for an end state.
		if self.game_over or self.board[index]:
			return
		self.place_mark(index, "O")
		if self.check_round_end():
			return
		self.status.config(text="Computer's turn (X)")
		self.root.after(250, self.computer_move)

	def computer_move(self):
		# Select and play the computer's move unless the round already ended.
		if self.game_over:
			return
		index = self.best_move()
		self.place_mark(index, "X")
		if not self.check_round_end():
			self.status.config(text="Your turn (O)")

	def place_mark(self, index, mark):
		# Update the board data and disable/color the button for this position.
		self.board[index] = mark
		color = self.BLUE if mark == "O" else self.RED
		self.buttons[index].config(text=mark, fg=color, disabledforeground=color,
								   state="disabled")

	def has_won(self, mark):
					# Return whether this mark occupies all three cells in any winning line.
		return any(all(self.board[i] == mark for i in line)
				   for line in self.WINNING_LINES)

	def best_move(self):
		# Try every available square and use minimax to choose the best outcome.
		best_score = float("-inf")
		best_spot = None
		
		# adding random element to the AI so that it doesn't always pick the best spot and allow for more human-like play.
		rando = random.randint(0, 3)
		if rando == 0:
			best_spot = random.choice([i for i, mark in enumerate(self.board) if not mark])
			return best_spot

        # find the best move
		for index, mark in enumerate(self.board):
			if not mark:
				self.board[index] = "X"
				score = self.minimax(computer_turn=False, depth=0)
				self.board[index] = ""
				if score > best_score:
					best_score = score
					best_spot = index
		return best_spot

	def minimax(self, computer_turn, depth):
		# Score completed games; depth favors quicker wins and slower losses.
		if self.has_won("X"):
			return 10 - depth
		if self.has_won("O"):
			return depth - 10
		if all(self.board):
			return 0

		# Explore each legal move, alternating players, and choose the best score.
		mark = "X" if computer_turn else "O"
		scores = []
		for index, current in enumerate(self.board):
			if not current:
				self.board[index] = mark
				scores.append(self.minimax(not computer_turn, depth + 1))
				self.board[index] = ""
		return max(scores) if computer_turn else min(scores)

	def check_round_end(self):
		# Update the appropriate score and announce a win, loss, or tie.
		if self.has_won("O"):
			self.wins += 1
			self.finish_round("You win!", self.BLUE)
		elif self.has_won("X"):
			self.losses += 1
			self.finish_round("Computer wins!", self.RED)
		elif all(self.board):
			self.ties += 1
			self.finish_round("It's a tie!", "#37474f")
		else:
			return False
		self.score.config(
			text=f"Wins: {self.wins}    Losses: {self.losses}    Ties: {self.ties}"
		)
		return True

	def finish_round(self, message, color):
		# Prevent further moves and show the round result in the status label.
		self.game_over = True
		self.status.config(text=message, fg=color)

	def new_round(self):
		# Clear the board and restore all buttons while keeping the running score.
		self.board = [""] * 9
		self.game_over = False
		self.status.config(text="Your turn (O)", fg="#37474f")
		for button in self.buttons:
			button.config(text="", state="normal", fg="#263238")


if __name__ == "__main__":
	# Create the Tkinter application and start its event loop.
	window = tk.Tk()
	TicTacToe(window)
	window.mainloop()
