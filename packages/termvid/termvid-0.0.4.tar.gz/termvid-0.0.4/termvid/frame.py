import sys
import math
import blessed
import cv2
import random
import numpy as np

term = blessed.Terminal()


class Frame:
	x = y = w = h = 0
	h_res = w_res = 1

	def __init__(self, pos, dimensions):
		self.x, self.y = pos
		self.w, self.h = dimensions
		self.h *= self.h_res
		self.w *= self.w_res

	def reposition(self, xy):
		self.x, self.y = xy

	def resize(self, dimensions):
		self.w, self.h = dimensions
		self.h *= self.h_res
		self.w *= self.w_res

	def draw(self, data):
		pass

	def fit(self, data):
		background = np.zeros((self.h, self.w, 3), np.uint8)
		h, w, channels = data.shape

		aspect_ratio = h / w
		screen_aspect_ratio = self.h / self.w

		width = self.w
		change = width / w
		height = round(change * h)
		tocut = height - self.h
		data = cv2.resize(data, (width, height), fx=0.5, fy=0.5)

		if tocut > 0:
			y_offset = 0
			y_snip = math.floor(tocut/2)
		else:
			y_offset = math.floor((-1 * tocut)/2)
			y_snip = 0

		# print(term.height)
		# print(tocut)
		# print(y_offset)
		# input(y_snip)

		# x_offset = round((self.w - width)/2)
		background[y_offset:y_offset+height] = data[y_snip:height-y_snip]
		return background


class HDFrame(Frame):
	h_res, w_res = 2, 1
	data = None

	def draw(self, data):
		if data is None:
			return
		data = self.fit(data)
		if self.data is None:
			self.data = data
		row_num = 0
		row_y = 0
		for row, old_row in zip(data[::2], self.data[::2]):
			outrow = ""
			for x, pixel in enumerate(row):
				old_pixel = old_row[x]
				try:
					next_row_pixel = data[row_num + 1, x]
					old_next_row_pixel = self.data[row_num + 1, x]
				except IndexError:
					old_next_row_pixel = next_row_pixel = (255, 0, 0)
				# input(pixel)
				outpixel = term.on_color_rgb(*reversed(pixel)) + term.color_rgb(*reversed(next_row_pixel)) + '▄'
				# if old_next_row_pixel.tolist() != next_row_pixel.tolist() or pixel.tolist() != old_pixel.tolist():
					# sys.stdout.write(term.move_xy(self.x + x, self.y + row_y) + outpixel)
					# sys.stdout.flush()
				outrow += outpixel
			sys.stdout.write(term.move_xy(self.x, self.y + row_y) + outrow)
			sys.stdout.flush()
			row_num += 2
			row_y += 1

class ASCIIFrame(Frame):
	def draw(self, data):
		if data is None:
			return
		data = self.fit(data)
		for y, row in enumerate(data):
			outrow = ""
			for x, pixel in enumerate(row):
				brightness = round(10 * (np.average(pixel)/255)) - 1
				outrow += term.on_color_rgb(0, 0, 0) + term.white +" .:-=+*#%@"[brightness]
			sys.stdout.write(term.move_xy(self.x, self.y + y) + outrow)
			sys.stdout.flush()
