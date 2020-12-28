import random
import pygame
import os

os.environ["SDL_VIDEO_WINDOW_POS"] = "600,300"


pygame.init()


global width,height,size,highscore
size = 7
width,height = 110*size,110*size
screen = pygame.display.set_mode((110*size,110*size))
def load_score():
	try:
		with open("score.sf","r") as score:
			return int(score.read())
	except:
		with open("score.sf","w+") as score:
			score.write("0")
			return 0


def save_score(curscore):
	with open("score.sf","w+") as score:
		score.write(str(curscore))


def grid(m=4):
	for n in range(m):
		pygame.draw.line(screen,(32,34,29),(0,(height//m)*n),((width,(height//m)*n)),4)
		pygame.draw.line(screen,(32,34,29),((width//m)*n,0),(((width//m)*n,height)),4)
	pygame.draw.rect(screen,(32,34,29),pygame.Rect(-1,-1,width+1,height+1),6)


class Board:
	def __init__(self):
		self.game_over = False
		self.board = [[0 for i in range(size)]for i in range(size)]
		self.start = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,4,4,4,4,4,4,4,4,4,4,8]
		self.swap_hor = False
		self.swap_ver = False
		self.right,self.down,self.up,self.left = True,True,True,True
		self.last = None

		for n in range(2):
			self.board[random.randint(0,3)][random.randint(0,3)] = random.choice(self.start)


	def add_block(self):
		temp = False
		x,y = random.randint(0,len(self.board)-1),random.randint(0,len(self.board)-1)

		for n in self.board:
			for m in n:
				if m == 0:
					temp = True

		if temp:
			while self.board[y][x] != 0:
				x,y = random.randint(0,len(self.board)-1),random.randint(0,len(self.board)-1)

			self.board[y][x] = random.choice(self.start)
			self.last = (x,y)


	def draw(self):
		try:
			pygame.draw.rect(screen,(66,85,66),pygame.Rect(self.last[0]*width//size,self.last[1]*height//size,110,110))
		except: pass

		for y in range(len(self.board)):
			for x in range(len(self.board[0])):
				if self.board[y][x] != 0:
					font = pygame.font.SysFont(None, 30)
					text = font.render(f"{self.board[y][x]}", True, (224,139,79))
					text_rec = text.get_rect(center=((x+1)*width//size-(width//size)//2,(y+1)*height//size-(height//size)//2 ))
					screen.blit(text, text_rec)


	def move(self,dir_):
		"""
		Memory addresses are shared if we just use "self.control_board = self.board", 
		so changes to either list would be applied to both lists. 
		That would make the out of moves game over not possible. 
		"""
		self.control_board = str(self.board)

		if dir_ == "right":
			k,l = 0,1
			self.right = True

		elif dir_ == "down": 
			k,l = 1,0
			self.down = True

		elif dir_== "left":
			k,l = 0,1
			self.swap_hor = True
			self.swap("hor")
			self.left = True

		elif dir_ == "up":
			k,l = 1,0
			self.swap_ver = True
			self.swap("ver")
			self.up = True

		for n in range(3):
			for y in range(len(self.board)):
				for x in range(len(self.board[0])):
					x = (size-1)-x

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

		if str(self.board) == self.control_board:
			self.control(dir_)
		else: self.right,self.down,self.up,self.left = True,True,True,True

		self.add_block()


	def get_score(self):
		self.totalscore = 0
		for n in self.board:
			for m in n:
				self.totalscore += m
		return self.totalscore


	def control(self,dir_):
		if dir_ == "up":
			self.up = False

		if dir_ == "right":
			self.right = False

		if dir_ == "down":
			self.down = False

		if dir_ == "left":
			self.left = False

		if [self.left,self.right,self.up,self.down] == [False,False,False,False]:
			self.game_over = True


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


def game(highscore):
	b = Board()
	newhighscore = False
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
				if event.key == pygame.K_d:
					game_over_screen(b,200,2000,True)
					return

		b.draw()

		if b.game_over:
			score = b.get_score()
			if score > highscore:
				highscore = score
				newhighscore = True
				save_score(score)
			game_over_screen(b,score,highscore,newhighscore)
			return

		grid(size)

		pygame.display.set_caption(f'Score : {b.get_score()}')
		pygame.display.update()

def rainbow(color,state):
	if state == 1:
		return [color[0],color[1]+5,color[2]]
	
	if state == 2:
		return [color[0]-5,color[1],color[2]]
	
	if state == 3:
		return [color[0],color[1],color[2]+5]
	
	if state == 4:
		return [color[0],color[1]-5,color[2]]
	
	if state == 5:
		return [color[0]+5,color[1],color[2]]

	if state == 6:
		return [color[0],color[1],color[2]-5]

def draw_text(text,pos,size = 50,center = True, color = (29,49,120)):
	
	font = pygame.font.SysFont(None, size)
	try:
		text = font.render(text, True, color)
		if center: 
			text_rec = text.get_rect(center=pos)
			screen.blit(text, text_rec)
		else:
			screen.blit(text,pos)
	except: pass

def game_over_screen(board,score,highscore,newhighscore):
	newhighscore = newhighscore
	highscore = highscore
	score = score
	s = pygame.Surface((width//2,height))
	b = board
	b.last = None
	co = 0
	cou = 0
	coun = 0
	counter = 1
	color = [255,10,0]
	state = 1
	while True:
		co += 0.1
		if co >= 100:
			co = 100
		s.set_alpha(co)
		screen.fill((66,68,66))
		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True

		new_game = pygame.Rect(0,0,width//2,height)
		exit = pygame.Rect(width//2,0,width,height)

		mx,my = pygame.mouse.get_pos()
		b.draw()
		grid(size)
		if new_game.collidepoint((mx,my)): 
			if click:
				return
			if cou <= 20:
				cou += 0.2
		else:
			if cou >= 0:
				cou -= 1

		s.set_alpha(co+cou)
		s.fill((0,255,0))
		screen.blit(s, (0,0))

		if exit.collidepoint((mx,my)): 
			if click:
				quit()
			if coun <= 40:
				coun += 0.4
		else:
			if coun >= 0:
				coun -= 1
		s.set_alpha(co+coun)
		s.fill((255,0,0))
		screen.blit(s,(width//2,0))

		draw_text(f"New",(width//4,height//2-17))
		draw_text(f"Game",(width//4,height//2+15))
		draw_text(f"Exit",(3*width//4,height//2-17))
		draw_text(f"Game",(3*width//4,height//2+15))
		if not newhighscore:
			draw_text(f"Score : {score}",(10,10),30,False,(2,249,150))
			draw_text(f"Highscore : {highscore}",(width//2+10,10),30,False,(252,182,5))
		if newhighscore:
			counter += 1
			if counter%51 == 0:
				state+=1
				if state == 7: state = 1
			color = rainbow(color,state)
			draw_text(f"!!! New Highscore !!!",(width//2,50),60,True,[255-color[0],255-color[1],255-color[2]])
			draw_text(f"Score : {score}  ",(width//2,95),60,True,color)

		pygame.display.update()

while True:
	highscore = load_score()
	game(highscore)
