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
		self.pos

class Player(Entity):
	def __init__(self,pos,size):
		self.chroma = pygame.Color(0,255,0,1)
		self.pos = pos
		self.size = size
		self.priority = 1
		self.health = 255
	def move(self):
		pressed = pygame.key.get_pressed()
		while (not pressed ):
			pressed = pygame.key.get_pressed()
		x ,y = self.pos
		if pressed['a']:
			if x - 1 >= 0:
				self.pos = (x-1,y)
		elif pressed['s']:
			if y - 1 >= 0:
				self.pos = (x,y-1)
		elif pressed['w']:
			if y + 1 < size:
				self.pos = (x,y+1)
		elif pressed['a']:
			if x + 1 < size:
				self.pos = (x+1,y)
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




print("hello world")
