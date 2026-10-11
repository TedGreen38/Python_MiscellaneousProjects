"""This is code for a simple Pong game that was made in Python."""

import random
import threading
import tkinter as tk
import math

try:
	import winsound
except ImportError:
	winsound = None


WIDTH, HEIGHT = 800, 500
PADDLE_W, PADDLE_H = 12, 90
BALL_SIZE = 14


class Pong:
	# Set up the game window, canvas, starting state, and keyboard/game loop.
	def __init__(self, root):
		self.root = root
		root.title("Pong")
		root.resizable(False, False)
		root.configure(bg="white")
		root.geometry(f"{WIDTH + 10}x{HEIGHT + 10}")

		self.canvas = tk.Canvas(
			root, width=WIDTH, height=HEIGHT, bg="white", highlightthickness=0
		)
		self.canvas.place(x=0, y=0)

		self.player_y = self.computer_y = HEIGHT / 2
		self.ball_x, self.ball_y = WIDTH / 2, HEIGHT / 2
		self.ball_vx, self.ball_vy = 5, 3
		self.player_score = self.computer_score = 0
		self.pressed = set()
		self.particles = []
		self.shake = 0

		self.canvas.create_rectangle(10, 0, WIDTH / 2, HEIGHT, fill="red", outline="")
		self.canvas.create_rectangle(
			WIDTH / 2, 0, WIDTH, HEIGHT, fill="blue", outline=""
		)
		self.canvas.create_line(
			WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="white", dash=(8, 10)
		)
		self.player = self.canvas.create_rectangle(0, 0, 0, 0, fill="white")
		self.computer = self.canvas.create_rectangle(0, 0, 0, 0, fill="white")
		self.ball = self.canvas.create_oval(
			0, 0, 0, 0, fill="white", outline="white", width=3
		)
		self.score = self.canvas.create_text(
			WIDTH / 2, 35, fill="white", font=("Impact", 50), text="0     0"
		)
		self.canvas.create_text(
			WIDTH / 2,
			HEIGHT - 18,
			fill="white",
			font=("Arial", 11),
			text="Use the Up and Down arrow keys",
		)

		root.bind_all("<KeyPress>", self.key_down)
		root.bind_all("<KeyRelease>", self.key_up)
		self.draw()
		self.tick()

	# Track a key while it is being held so the paddle can move continuously.
	def key_down(self, event):
		self.pressed.add(event.keysym)

	# Stop tracking a key when it is released.
	def key_up(self, event):
		self.pressed.discard(event.keysym)

	# Play a short, non-blocking chiptune-style beep when sound is available.
	def play_sound(self, frequency):
		if winsound is not None:
			threading.Thread(
				target=winsound.Beep, args=(frequency, 45), daemon=True
			).start()

	# Return the ball to the center and launch it in the requested direction.
	def reset_ball(self, direction):
		self.ball_x, self.ball_y = WIDTH / 2, HEIGHT / 2
		self.ball_vx = 5 * direction
		self.ball_vy = random.choice((-3, -2, 2, 3))

	# Create a speed-scaled particle burst and screen shake at an impact.
	def impact_effect(self, x, y, color):
		speed = math.hypot(self.ball_vx, self.ball_vy)
		count = min(24, 7 + int(speed * 1.5))
		for _ in range(count):
			angle = random.uniform(0, 2 * math.pi)
			velocity = random.uniform(1.5, 4.5) * min(speed / 6, 2)
			item = self.canvas.create_oval(0, 0, 0, 0, fill=color, outline="")
			self.particles.append([
				item, x, y, math.cos(angle) * velocity,
				math.sin(angle) * velocity, random.randint(12, 22),
			])
		self.shake = max(self.shake, min(12, speed * 0.8))

	# Advance particles and remove them when their lifespan expires.
	def update_particles(self):
		for particle in self.particles[:]:
			item, x, y, vx, vy, life = particle
			x += vx
			y += vy
			vy += 0.12
			life -= 1
			if life <= 0:
				self.canvas.delete(item)
				self.particles.remove(particle)
				continue
			particle[1:6] = [x, y, vx * 0.97, vy, life]
			radius = max(1, life / 8)
			self.canvas.coords(item, x - radius, y - radius, x + radius, y + radius)

	# Update the canvas positions of both paddles, the ball, and the score.
	def draw(self):
		self.canvas.coords(
			self.player,
			30,
			self.player_y - PADDLE_H / 2,
			30 + PADDLE_W,
			self.player_y + PADDLE_H / 2,
		)
		self.canvas.coords(
			self.computer,
			WIDTH - 30 - PADDLE_W,
			self.computer_y - PADDLE_H / 2,
			WIDTH - 30,
			self.computer_y + PADDLE_H / 2,
		)
		radius = BALL_SIZE / 2
		self.canvas.coords(
			self.ball,
			self.ball_x - radius,
			self.ball_y - radius,
			self.ball_x + radius,
			self.ball_y + radius,
		)
		self.canvas.itemconfigure(
			self.score, text=f"{self.player_score}     {self.computer_score}"
		)

	# Advance player and computer movement, handle collisions and scoring, then schedule the next frame.
	def tick(self):
		if "Up" in self.pressed:
			self.player_y -= 7
		if "Down" in self.pressed:
			self.player_y += 7
		self.player_y = max(PADDLE_H / 2, min(HEIGHT - PADDLE_H / 2, self.player_y))

		# A slower computer opponent follows the ball.
		if self.ball_y < self.computer_y - 8:
			self.computer_y -= 4
		elif self.ball_y > self.computer_y + 8:
			self.computer_y += 4
		self.computer_y = max(
			PADDLE_H / 2, min(HEIGHT - PADDLE_H / 2, self.computer_y)
		)

		self.ball_x += self.ball_vx
		self.ball_y += self.ball_vy
		radius = BALL_SIZE / 2

		if self.ball_y - radius <= 0 or self.ball_y + radius >= HEIGHT:
			self.ball_vy *= -1
			self.impact_effect(
				self.ball_x, max(radius, min(HEIGHT - radius, self.ball_y)), "#ffd166"
			)
			self.play_sound(880)

		player_right = 30 + PADDLE_W
		if (
			self.ball_vx < 0
			and self.ball_x - radius <= player_right
			and self.ball_x + radius >= 30
			and self.player_y - PADDLE_H / 2 <= self.ball_y <= self.player_y + PADDLE_H / 2
		):
			self.ball_x = player_right + radius
			self.ball_vx = abs(self.ball_vx) * 1.05
			self.ball_vy += (self.ball_y - self.player_y) * 0.08
			self.impact_effect(self.ball_x, self.ball_y, "white")
			self.play_sound(660)

		computer_left = WIDTH - 30 - PADDLE_W
		if (
			self.ball_vx > 0
			and self.ball_x + radius >= computer_left
			and self.ball_x - radius <= WIDTH - 30
			and self.computer_y - PADDLE_H / 2 <= self.ball_y <= self.computer_y + PADDLE_H / 2
		):
			self.ball_x = computer_left - radius
			self.ball_vx = -abs(self.ball_vx) * 1.05
			self.ball_vy += (self.ball_y - self.computer_y) * 0.08
			self.impact_effect(self.ball_x, self.ball_y, "white")
			self.play_sound(740)

		if self.ball_x + radius < 0:
			self.computer_score += 1
			self.reset_ball(1)
		elif self.ball_x - radius > WIDTH:
			self.player_score += 1
			self.reset_ball(-1)

		self.update_particles()
		self.draw()
		self.shake *= 0.78
		if self.shake < 0.4:
			self.shake = 0
			offset_x = offset_y = 0
		else:
			offset_x = random.randint(-int(self.shake), int(self.shake))
			offset_y = random.randint(-int(self.shake), int(self.shake))
		self.canvas.place(x=1 + offset_x, y=1 + offset_y)
		self.root.after(16, self.tick)


if __name__ == "__main__":
	window = tk.Tk()
	Pong(window)
	window.mainloop()
