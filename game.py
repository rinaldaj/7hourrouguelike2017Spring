import pygame
import random


class Entity:
	chroma = pygame.Color(0,0,0,1)
	health = 1
	pos = (0,0)
	size = 0
	priority = 0
	def __init__(self,pos,size):
		self.chroma = pygame.Color(0,0,0,1)
		self.health = 7
		self.pos = pos
		size = size
	def getHealth(self):
		return self.health
	def getColor(self):
		return self.chroma
	def move(self):
		return
	def put(self,pos):
		self.pos = pos
	def attack(self,victim):
		return
	def takeDamage(self,pain):
		self.health = self.health - pain
	def getPos(self):
		return self.pos

class Player(Entity):
	def __init__(self,pos,size):
		self.chroma = pygame.Color(0,255,0,1)
		self.pos = pos
		self.size = size
		self.priority = 1
		self.health = 255
	def move(self):
		pressed = pygame.key.get_pressed()
		while True:
			x ,y = self.pos
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						if x - 1 >= 0:
							self.pos = (x-1,y)
					elif event.key == pygame.K_UP:
						if y - 1 >= 0:
							self.pos = (x,y-1)
					elif event.key == pygame.K_DOWN:
						if y + 1 < size:
							self.pos = (x,y+1)
					elif event.key == pygame.K_RIGHT:
						if x + 1 < size:
							self.pos = (x+1,y)
					return
	def attack(self,victim):
		victim.takeDamage(10)
	def takeDamage(self,pain):
		Entity.takeDamage(self,pain)
		r = 255 - self.health
		if r < 0:
			r = 0
		if r > 255:
			r = 255
		g = self.health
		if g < 0:
			g = 0
		if g > 255:
			g = 255
		self.chroma = pygame.Color(r,g,0,1)
class Enemy(Entity):
	def __init__(self,pos,size):
		self.pos = pos
		self.size = size
		self.health = 20
		self.chroma = pygame.Color(255,140,0,1)
	def attack(self,victim):
		victim.takeDamage(10)
	def move(self):
		xC = random.randint(-1,2)
		yC = random.randint(-1,2)
		x,y = self.pos
		nx = x
		ny = y
		if x + xC >= 0 and x + xC < self.size:
			nx = x + xC
		if y + yC >= 0 and y + yC < self.size:
			ny = y + yC
		self.pos = (nx,ny)
class Potion(Entity):
	def __init__(self,pos,size):
		self.pos = pos
		self.size = size
		self.health = 20
		self.chroma = pygame.Color(0,0,255,1)
	def takeDamage(self,pain):
		return
	def attack(self,victim):
		victim.takeDamage(-8)
		self.health = 0

class Wall(Entity):
	def __init__(self,pos,size):
		self.pos = pos
		self.size = size
		self.health = 20
		self.chroma = pygame.Color(255,255,255,1)
	def takeDamage(self,pain):
		return
	def attack(self,victim):
		victim.takeDamage(victim.getHealth())

def buildBoard(player,level,size):
	ret = []
	for i in range(level):
		x = random.randint(0,size-1)
		y = random.randint(0,size-1)
		pos = (x,y)
		ret.append(Enemy(pos,size))
	for i in range(int(level-1)):
		x = random.randint(0,size-1)
		y = random.randint(0,size-1)
		pos = (x,y)
		ret.append(Potion(pos,size))
	for i in range(int(size + level/5)):
		x = random.randint(0,size-1)
		y = random.randint(0,size-1)
		pos = (x,y)
		ret.append(Wall(pos,size))
	ret.append(player)
	return ret
def sortByPriority(board):
	print(len(board))
	if board is None:
		return []
	elif len(board) == 1:
		return board[0]
	else:
		tmp = board[0]
		tmpl = board
		tmpl.pop(0)
		return sortByPriority([x for x in tmpl if x.priority < tmp.priority]).append(tmp).append(sortByPriority([x for x in tmpl if x.priority >= tmp.priority]))

def overlap(one,two):
	x1,y1 = one.getPos()
	x2,y2 = two.getPos()
	return x1 == x2 and y1 == y2

def updateBoard(ins,disp,size):
	#board = sortByPriority(ins)
	for i in ins:
		x,y = i.getPos()
		pygame.draw.rect(disp,i.getColor(),(x*100,y*100,100,100),0)
	whitespace = []
	for x in range(size):
		for y in range(size):
			over = False
			for j in ins:
				if overlap(Entity((x,y),size),j):
					over = True
			if not over:
				whitespace.append((x,y))
	for (x,y) in whitespace:
		pygame.draw.rect(disp,pygame.Color(0,0,0,0),(x*100,y*100,100,100),0)
		
	pygame.display.update()
def killEachOther(ins):
	for i in ins:
		for j in ins:
			if (not i is j) and i.getPos() == j.getPos():
				i.attack(j)

def eEEEvil(ins):
	ret = False
	for i in ins:
		if isinstance(i, Enemy):
			ret = True
	return ret

def playerReal(ins):
	ret = False
	for i in ins:
		if isinstance(i, Player):
			ret = True
	return ret
		

pygame.init()

size = int(input("How big of a board: "))

level = 1

display = pygame.display.set_mode((size * 100,size * 100))
pygame.display.update()
player = Player((0,0),size)
ins = buildBoard(player,level,size)


updateBoard(ins,display,size)

while playerReal(ins):
#while 1:
	while eEEEvil(ins):
		for i in ins:
			i.move()
		killEachOther(ins)
		for i in ins:
			if i.getHealth() <= 0:
				ins.remove(i)
		updateBoard(ins,display,size)
	level = level + 1
	player.put((0,0))
	ins = buildBoard(player,level,size)
	for i in ins:
		if i.getHealth() <= 0:
			ins.remove(i)
	updateBoard(ins,display,size)
print("game over")
