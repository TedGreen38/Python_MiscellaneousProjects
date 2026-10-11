"""A simple calculator with mouse and keyboard input."""

# Imports provide safe expression parsing, arithmetic operations, and the Tk GUI.
import ast
import operator
import tkinter as tk
from tkinter import ttk

_BINARY = {
	ast.Add: operator.add,
	ast.Sub: operator.sub,
	ast.Mult: operator.mul,
	ast.Div: operator.truediv,
	ast.Mod: operator.mod,
}
_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def calculate(expression):
	"""Evaluate basic arithmetic without executing arbitrary Python code."""
	# Parse the input as an expression and evaluate only explicitly supported nodes.
	tree = ast.parse(expression, mode="eval")

	def evaluate(node):
		if isinstance(node, ast.Expression):
			return evaluate(node.body)
		if isinstance(node, ast.Constant) and type(node.value) in (int, float):
			return node.value
		if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
			return _BINARY[type(node.op)](evaluate(node.left), evaluate(node.right))
		if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
			return _UNARY[type(node.op)](evaluate(node.operand))
		raise ValueError("Unsupported expression")

	return evaluate(tree)


# Build the calculator window, its controls, and their event handlers.
class Calculator:
	def __init__(self, root):
		self.root = root
		root.title("Calculator")
		root.resizable(False, False)
		background = "#003b1f"
		neon_green = "#39ff14"
		root.configure(background=background)

		style = ttk.Style(root)
		style.theme_use("clam")
		style.configure(".", background=background, foreground=neon_green)
		style.configure(
			"TButton",
			background="black",
			foreground=neon_green,
			bordercolor=neon_green,
			lightcolor=neon_green,
			darkcolor=neon_green,
			borderwidth=2,
			relief="solid",
			padding=6,
		)
		style.map(
			"TButton",
			background=[("active", "#111111"), ("pressed", "#222222")],
			foreground=[("active", neon_green), ("pressed", neon_green)],
		)
		style.configure(
			"TEntry",
			fieldbackground="black",
			foreground=neon_green,
			insertcolor=neon_green,
			bordercolor=neon_green,
			lightcolor=neon_green,
			darkcolor=neon_green,
			borderwidth=2,
		)
		self.value = tk.StringVar()

		# Create the expression display and arrange the calculator buttons.
		self.display = ttk.Entry(root, textvariable=self.value, justify="right", font=("Arial", 22))
		self.display.grid(row=0, column=0, columnspan=4, padx=8, pady=8, sticky="nsew", ipady=8)

		buttons = (
			("C", "⌫", "(", ")"),
			("7", "8", "9", "÷"),
			("4", "5", "6", "×"),
			("1", "2", "3", "−"),
			("0", ".", "%", "+"),
			("=",),
		)
		for row, labels in enumerate(buttons, start=1):
			for column, label in enumerate(labels):
				ttk.Button(
					root,
					text=label,
					command=lambda item=label: self.press(item),
				).grid(
					row=row,
					column=column,
					columnspan=4 if label == "=" else 1,
					padx=4,
					pady=4,
					sticky="nsew",
					ipadx=8,
					ipady=10,
				)
		for column in range(4):
			root.columnconfigure(column, minsize=64, weight=1)

		# Send keyboard input to the calculator's keyboard handler.
		root.bind("<Key>", self.on_key)
		self.display.focus_set()

	# Apply a button press to the expression display or calculate its result.
	def press(self, key):
		if key == "C":
			self.value.set("")
		elif key == "⌫":
			self.value.set(self.value.get()[:-1])
		elif key == "=":
			self.solve()
		else:
			self.value.set(self.value.get() + {"÷": "/", "×": "*", "−": "-"}.get(key, key))

	# Support typing expressions and the Enter, Escape, and Backspace keys.
	def on_key(self, event):
		if event.keysym in ("Return", "KP_Enter"):
			self.solve()
		elif event.keysym == "Escape":
			self.value.set("")
		elif event.keysym == "BackSpace":
			self.value.set(self.value.get()[:-1])
		elif event.char in "0123456789.+-*/()%":
			self.value.set(self.value.get() + event.char)
		else:
			return
		return "break"

    # Calculate the result of the expression in the display.
	def solve(self):
		try:
			self.value.set(str(calculate(self.value.get())))
		except (SyntaxError, ValueError, ZeroDivisionError, OverflowError):
			self.value.set("Error")

# Main entry point for the calculator application.
if __name__ == "__main__":
	app = tk.Tk()
	Calculator(app)
	app.mainloop()
