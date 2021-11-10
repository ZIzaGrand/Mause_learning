import numpy as np
import random
import pandas as pd

class maus_learning:

	def __init__(self, maze):

		self.q_values = np.zeros((len(maze[0]) * len(maze), 4))
		self.df = pd.DataFrame(self.q_values, columns=[' up ', 'down', 'right', 'left'])
		self.df.index.name = 'States'

		self.field = np.arange(len(maze[0]) * len(maze)).reshape(len(maze), len(maze[0]))

		self.maze = maze
		cats = []
		i = 0
		for row in maze:
			ii = 0
			for cat in row:
				if cat == 1:
					cats.append(i * len(row) + ii)
				ii += 1
			i += 1
		self.cats = cats

		self.Y = 0
		self.X = 0

		self.stop = True
		self.reward = 0
		self.die = -1000
		self.chees = 1000

		self.count_chize = 0



	def stop_learning(self):
		if self.stop == True:
			self.stop = False
			print("learning switching-oof ")
		else:
			self.stop = True
			print("learning switching-on ")
		return self.stop


	def back_calculation(self, q_values, state, learning_rate=0.5, gamma=0.9):

		this_state = self.field[self.Y][self.X]

		td_target = self.reward + gamma * self.q_values[self.state][action]
		td_error = td_target - self.q_values[self.this_state][self.action]
		self.q_values[self.state][self.action] += learning_rate * td_error


	def back_step(self, reward):

		if move == 0 or 2:
			self.action = move + 1
			self.back_calculation(self.q_values, self.state)
		else:
			self.action = move - 1
			self.back_calculation(self.q_values, self.state)


	def calculation(self, q_values, state, learning_rate=0.5, gamma=0.9):


		next_state = self.field[self.Y][self.X]

		td_target = self.reward + gamma * np.max(self.q_values[next_state])
		td_error = td_target - self.q_values[self.state][self.action]
		self.q_values[self.state][self.action] += learning_rate * td_error


	def reset(self):

		self.Y = 0
		self.X = 0

	def win(self, state, action1, chees):
		if state == len(self.maze[0]) * len(self.maze) - 1:
			self.q_values[self.state][self.action] += self.chees
			self.reset()
			self.count_chize += 1

	def cat(self, state, action1, cats):

		for i in self.cats:
			
			if self.state == i:
				self.q_values[self.state][self.action] += self.die
				self.reset()


	def step(self, q_values, state):
		if np.random.random() < 0.05 and self.stop == True:
			move =  np.random.choice(4)

		else:
			move = np.argmax(self.q_values[self.state])
		
		return move

	def line_movement(self, move, state):
		
		if move == 0 and self.Y > 0: #up
			self.Y -= 1
			self.reward = -0.5

		elif move == 1 and self.Y < len(self.maze) - 1: # down
			self.Y += 1
			self.reward = -0.5

		elif move == 2 and self.X < len(self.maze[0]) - 1: #right
			self.X += 1
			self.reward = -0.5

		elif move == 3 and self.X > 0: #left
			self.X -= 1
			self.reward = -0.5

		else:
			self.q_values[self.state][self.action] += -1000
			self.reward = 0

		return self.Y, self.X, self.reward

	def nihachu_pridumivat(self):

		self.z_field = np.zeros((len(self.maze), len(self.maze[0])))
		self.state = self.field[self.Y][self.X]

		self.action = self.step(self.q_values, self.state)

		self.cat(self.state, self.action, self.cats)
		self.win(self.state, self.action, self.chees)

		self.Y, self.X, self.reward = self.line_movement(self.action, self.state)

		self.z_field[self.Y][self.X] = 1


		self.calculation(self.q_values, self.state)
		self.back_step(self.reward, move)

		return self.z_field

	def nada(self, count_n = 1):
		self.count_chize = 1
		while count_n > self.count_chize:
			self.nihachu_pridumivat()





#l = maus_learning()
#l.nihachu_pridumivat()