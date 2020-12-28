import random
import pygame
import os

os.environ["SDL_VIDEO_WINDOW_POS"] = "600,300"


pygame.init()

screen = pygame.display.set_mode((440,440))


global width,height
width,height = 440,440

def grid(m=4):
	for n in range(m):
		pygame.draw.line(screen,(32,34,29),(0,(height//m)*n),((width,(height//m)*n)),4)
		pygame.draw.line(screen,(32,34,29),((width//m)*n,0),(((width//m)*n,height)),4)
	pygame.draw.rect(screen,(32,34,29),pygame.Rect(-1,-1,width+1,height+1),6)

class Board:
	def __init__(self):
		self.board = [[0 for i in range(4)]for i in range(4)]
		self.start = [2,2,2,2,2,2,4,4,4,4,8]
		self.swap_hor = False
		self.swap_ver = False

		for n in range(2):
			self.board[random.randint(0,3)][random.randint(0,3)] = random.choice(self.start)


	def add_block(self):
		temp = False
		x,y = random.randint(0,3),random.randint(0,3)
		for n in self.board:
			for m in n:
				if m == 0:
					temp = True
		if temp:
			while self.board[y][x] != 0:
				x,y = random.randint(0,3),random.randint(0,3)
			self.board[y][x] = random.choice(self.start)

	def draw(self):
		for y in range(len(self.board)):
			for x in range(len(self.board[0])):
				if self.board[y][x] != 0:
					font = pygame.font.SysFont(None, 30)
					text = font.render(f"{self.board[y][x]}", True, (224,139,79))
					text_rec = text.get_rect(center=((x+1)*width//4-(width//4)//2,(y+1)*height//4-(height//4)//2 ))
					screen.blit(text, text_rec)


	def move(self,dir_):
		if dir_ == "right":
			k,l = 0,1
		elif dir_ == "down": 
			k,l = 1,0
		elif dir_== "left":
			k,l = 0,1
			self.swap_hor = True
			self.swap("hor")
		elif dir_ == "up":
			k,l = 1,0
			self.swap_ver = True
			self.swap("ver")
		for n in range(3):
			for y in range(len(self.board)):
				for x in range(len(self.board[0])):
					x = 3-x
					if self.board[y][x] != 0:
						try:
							if self.board[y+k][x+l] == 0:
								self.board[y+k][x+l],self.board[y][x] = self.board[y][x],0
						except: continue
					try:
						if self.board[y][x] == self.board[y+k][x+l]:
							self.board[y+k][x+l] *= 2
							self.board[y][x] = 0
					except: continue
		if self.swap_hor:
			self.swap_hor = False
			self.swap("hor")
		elif self.swap_ver:
			self.swap_ver = False
			self.swap("ver")

		self.add_block()

	def swap(self,dir_):
		self.temp = []
		if dir_ == "ver":
			for n in range(len(self.board)):
				self.temp.append(self.board[-1-n])
			self.board = self.temp
		if dir_ == "hor":
			for n in range(len(self.board[0])):
				self.copy = self.board[n]
				self.copy.reverse()
				self.temp.append(self.copy)

	def log(self):
		for b in self.board:
			print(b)

def game():
	b = Board()
	b.log()
	while True:
		screen.fill((66,68,66))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					b.move("right")
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					b.move("down")
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					b.move("left")
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					b.move("up")
		b.draw()

		grid(4)

		pygame.display.update()


game()
