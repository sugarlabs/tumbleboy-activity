#	This file was created for the game "Tumble Boy", by
#	Bob Rost, Chris Jackson, Eben Myers, and Tom Corbett.
#	Please study it, learn from it, change it, and share it.

import pygame
from pygame.locals import *

# returns either an image file, or None
def LoadImage(filename, w=0, h=0):
	try:
		image = pygame.image.load(filename)
		if (w>0 and h>0):
			return pygame.transform.scale(image, (int(w), int(h)))
		else:
			return image
	except pygame.error:
		print "Could not load image "+filename
		return None

# a class for drawing a picture
class StaticImage:
	def __init__(self, pygame_screen, filename, x=0, y=0):
		self.screen = pygame_screen	
		try:
			self.image = pygame.image.load(filename)	#load image from disk
			self.rect = self.image.get_rect()
		except pygame.error:
			self.image = None
			self.rect = Rect(0,0,0,0)

	def SetPosition(self, upper_left): #pass an array of [x,y]
		self.rect.left = upper_left[0]
		self.rect.top = upper_left[1]

	#no return value
	def Draw(self):
		if ((self.screen == None) or (self.image==None)): return
		self.screen.blit(self.image, self.rect)


#a class for drawing an animated sprite
class Character:
	def __init__(self, pygame_screen):
		self.rect = Rect(0,0,0,0)	# position (upper left) and size (width and height)
		self.images = []		# we will fill this array with AddImage()
		self.frame_delta = 0.5	# default 2 frames per second
		self.current_frame = 0	# current animation frame
		self.timer = 0			# animation frame timer
		self.screen = pygame_screen
		pass

	#returns bool
	def SetAnimationFramesPerSecond(self, fps):
		if (fps < 0):
			return False
		elif (fps == 0):
			frame_delta = 0
			return True
		else:
			frame_delta = 1.0 / fps
			return True

	#no return value
	def SetPosition(self, upper_left): #pass an array of [x,y]
		self.rect.left = upper_left[0]
		self.rect.top = upper_left[1]

	#returns bool
	def AddImage(self, filename):
		try: newimage = pygame.image.load(filename)	#load image from disk
		except pygame.error: return False			#error loading image

		if (len(self.images)==0): #adding first image
			self.rect = newimage.get_rect()
			self.rect.width = 100
			self.rect.height = 100
		self.images.append(newimage)

	#no return value
	def UpdateAnimation(self, dt):
		if (len(self.images) == 0): return
		self.timer += dt
		while (self.timer >= self.frame_delta):
			self.timer -= self.frame_delta
			self.current_frame = (self.current_frame+1) % len(self.images)

	#no return value
	def Draw(self):
		if ((self.screen == None) or (len(self.images)==0)): return
		self.screen.blit(self.images[self.current_frame], self.rect)
