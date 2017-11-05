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
							return
					elif event.key == pygame.K_UP:
						if y - 1 >= 0:
							self.pos = (x,y-1)
							return
					elif event.key == pygame.K_DOWN:
						if y + 1 < size:
							self.pos = (x,y+1)
							return
					elif event.key == pygame.K_RIGHT:
						if x + 1 < size:
							self.pos = (x+1,y)
							return
	def attack(self,victim):
		victim.takeDamage(10)
	def takeDamage(self,pain):
		Entity.takeDamage(self,pain)
		self.chroma = pygame.Color(255 - self.health,self.health,0,1)
class Enemy(Entity):
	def __init__(self,pos,size):
		self.pos = pos
		self.size = size
		self.health = 20
		self.chroma = pygame.Color(255,140,0,1)
	def attack(self,victim):
		victim.takeDamage(5)
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
	def takeDamage(self):
		return
	def attack(self,victim):
		victim.takeDamage(-8)
		self.health = 0


def buildBoard(player,level,size):
	ret = []
	for i in range(level):
		x = random.randint(0,size)
		y = random.randint(0,size)
		pos = (x,y)
		ret.append(Enemy(pos,size))
	for i in range(int(level/6)):
		x = random.randint(0,size)
		y = random.randint(0,size)
		ret.append(Potion((x,y),size))
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

def updateBoard(ins,disp):
	#board = sortByPriority(ins)
	for i in ins:
		x,y = i.getPos()
		pygame.draw.rect(disp,i.getColor(),(x*100,y*100,100,100),0)
	pygame.display.update()
		

pygame.init()

size = int(input("How big of a board: "))

level = 1

display = pygame.display.set_mode((size * 100,size * 100))
pygame.display.update()
player = Player((0,0),size)
ins = buildBoard(player,level,size)


updateBoard(ins,display)

while player.getHealth() > 0:
	for i in ins:
		i.move()
	updateBoard(ins,display)
