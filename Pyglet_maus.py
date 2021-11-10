import pyglet
import random as rnd
import numpy as np
import random
import pandas as pd
import time
from mause_learning import maus_learning

# стандартный лаберинт
maze = [
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
		[1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
		[0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
		[0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
		[0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
		[0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0,],
		[0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
		[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
		[0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
		[0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
		[0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
		[0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
		[0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
		[0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
		[0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
		[0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
		[0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1,],
		[0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1,],
		[0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,],
		[0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,]]

#maus_hod = [[0 for ii in range(len(maze[0]))] for i in range(len(maze))]

class GameOfLife:
	def __init__(self, window_width, window_height, matrix=[[]], cell_size = 10):
		# ширина и длинна нашего окна в зависимости от размера квадратов и величины массива стенок
		self.grid_width = round(cell_size * len(matrix[0]))
		self.grid_height = round(cell_size * len(matrix))

		print(f'{self.grid_width}, {self.grid_height}  размер окна')

		self.matrix = matrix # сохраняем полученную матрицу лабиринта
		self.cell_size = cell_size # размер квадратов
		self.cells = matrix[::-1] # переворачиваем полученный массив, связано с началом отрисовки снизу слева
		self.cicle = 0 # количество шагов
		self.maus_learning_L = maus_learning(self.matrix)
		self.sleep_time = 0 # скаолько кадров надо пропустить
		self.sleep_time_n = 0 # какой кадр пропускается по счёту
		self.maus_massiv_not_normal = [] # массив нахождения мыши, в пришёдшей форме
		self.set_probel_L = False # нажат ли пробел

		self.first_run = True # первый ли запуск

	def get_len(self):
		return([self.grid_width, self.grid_height]) # возвращает размер заданного окна

	def get_index_1(self, massiv):
		# ищем мышку (1) в нашем массиве
		for row in range(0, len(massiv)):
			if 1 in massiv[row]:
				return([len(massiv) - row - 1, massiv[row].index(1)])

		return([0,0])

	def set_massiv_maus(self, massiv):
		self.maus_massiv = massiv # получаем массив с мышкой

	def draw(self):
		# предварительное обучение мыши. Визуал не запуститься, пока мыш не найдёт заданое кол раз сыр
		if self.first_run:
			# self.cicle = 100
			self.maus_learning_L.nada(self.cicle)
		self.first_run = False
		# уменьшение скорости
		if not self.set_probel_L:			
			if not (self.sleep_time_n < self.sleep_time):
				self.maus_massiv_not_normal = self.maus_learning_L.nihachu_pridumivat()
				self.cicle += 1 # увеличиваем наш шаг
				self.sleep_time_n = 0
			else:
				self.sleep_time_n += 1
		mas = [] # нормализированный массив (оригинальный не подходит)
		i = 0
		# пересоздаём наш массив с нормальным видом
		for t in self.maus_massiv_not_normal:
			mas.append([])
			i += 1
			for tt in t:
				if tt == 1.:
					mas[i-1].append(1)
				else:
					mas[i-1].append(0)

		self.set_massiv_maus(mas) # сохраняем массив

		# отрисовываем стенки лаберинта
		for row in range(0, len(self.cells)):
			for col in range(0,  len(self.cells[0])):
				if self.cells[row][col] == 1:
					self.drow_cube_in_matrix(row, col) 
					
		# сыр
		self.drow_cube_in_matrix(0, len(self.matrix[0]) - 1, (1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0))

		# отрисовываем нашу мышку
		maus_massiv = self.get_index_1(self.maus_massiv)
		self.drow_cube_in_matrix(maus_massiv[0], maus_massiv[1], (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5))
		

	def get_cicle(self):
		return self.cicle # возвращаем наш сейчас шаг

	def set_plus_timer(self, time_plus = 0):
		# увеличиваем пропуск кадров на заданое время
		if time_plus + self.sleep_time >= 0:
			self.sleep_time += time_plus
		return self.sleep_time

	def set_probel(self):
		self.set_probel_L = self.set_probel_L == False

	def drow_cube_in_matrix(self, row, col, c3f = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)):
		# отрисовываем кубик в задаеых координатах и заданным цветом
		squere_coords = (col * self.cell_size,                  row * self.cell_size,
						 col * self.cell_size,                  row * self.cell_size + self.cell_size,
						 col * self.cell_size + self.cell_size, row * self.cell_size,
						 col * self.cell_size + self.cell_size, row * self.cell_size + self.cell_size)

		pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
									 [0,1,2, 1, 2, 3],
									 ('c3f', c3f),
									 ('v2i', squere_coords))


class Window(pyglet.window.Window):
	def __init__(self, maze_l, cycle=0):
		super().__init__()
		# инструкция
		print('''
			Для отключения обучения нажмите "S" (Ы) 
				Мыш перестанет разбиваться о стены
			Для замедления передвижения мыши Стрелка вниз
			Для ускорения передвижения мыши Стрелка вверх
			Для остановки мыши нажмите пробел
			''')
		# задаём стенки лаберинта 
		self.gameOfLife = GameOfLife(self.get_size()[0], # размер окна (пока не нужно)
									 self.get_size()[1], # размер окна
									 maze_l, # передаём массив стенок
									 40) # размер квадрата

		# перезадаём размер окна в зависимости от размера квадратов и заданой матрицы стенок
		len_c = self.gameOfLife.get_len() 
		self.set_size(len_c[0], len_c[1])

		self.gameOfLife.cicle = cycle # количество предобучающих находок сыра

		self.fps = 120 # фпс
		self.sleep_time = 0 # через скаолько кадров будет слдующая отрсовка
		self.lerning = True # включено обучение или нет

		# устанавливаем частоту кадров
		pyglet.clock.schedule_interval(self.update, 1.0 / self.fps)

	def on_key_press(self, symbol, modifiers):
		# проверям нажатие стрелки вверх и вниз
		if symbol in [65362, 65364]:
			if symbol in [65362]:
				self.sleep_time = self.gameOfLife.set_plus_timer(1)
			elif symbol in [65364]:
				self.sleep_time = self.gameOfLife.set_plus_timer(-1)

		# проверка нажатия пробела
		if symbol in [32]: 
			self.gameOfLife.set_probel()

		if symbol in [115]: # s
			self.lerning = self.gameOfLife.maus_learning_L.stop_learning()

		#print(symbol)

	def on_draw(self):
		# задаём название окна
		self.set_caption(f'{self.sleep_time} | {self.gameOfLife.get_cicle()} | обучение {self.lerning}')
		# отчищаем окно
		self.clear()
		# отрисовываем новый слой
		self.gameOfLife.draw()

	def update(self, dt):
		# при каждой попытке перерисовать поле
		pass

def run_program(maze_l, cycle = 0):
	window = Window(maze_l, cycle)
	pyglet.app.run()

if __name__ == '__main__':
	window = Window(maze, 100)
	pyglet.app.run()