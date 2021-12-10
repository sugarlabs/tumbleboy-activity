#	This file was created for the game "Tumble Boy", by
#	Bob Rost, Chris Jackson, Eben Myers, and Tom Corbett.
#	Please study it, learn from it, change it, and share it.


from source.Graphics import *
from source.Constants import *
import sys, pygame, os, math
from pygame.locals import *

class Board:
	def __init__(self):
		self.Clear()

	#no return value
	def Clear(self):
		self.width = 0			# This number will change as the board grows
		self.height = 0			# This number will change as the board grows
		self.blocks = []		# Will fill this array will SetBlock(). An array of arrays.
		self.bumpers = []		# Will fill this array with pairs of [x,y] bumper centers
		self.block_images = []
		self.image = None
		self.image_width = 0
		self.image_height = 0
		self.SetTheme("default")

	def Width(self):	return self.width
	def Height(self):	return self.height

	def SetTheme(self, folder_name):
		#print "Board::SetTheme(%s)" % (folder_name)
		self.theme = "data/themes/"+folder_name+"/"
		self.block_images = []
		self.image = None

	#returns an [x,y] pair
	def GetStartPosition(self):
		#print "FIND START BLOCK IN %ix%i board" % (self.width, self.height)
		for y in range(self.height):
			for x in range(self.width):
				if (self.BlockAt(x,y) == BLOCK_START):
					#print "FOUND START BLOCK "+str([x,y])
					return [x,y]
		return [0,0]
	
	#returns either None or an [x,y,radius] pair
	def GetCollidingBumper(self, x,y):
		for b in self.bumpers:
			dx = b[0]-x
			dy = b[1]-y
			dist = math.sqrt(dx*dx + dy*dy)
			if (dist<=1.0): return [b[0],b[1],dist]
		return None

	#returns a boolean to indicate success or failure
	def SetBlock(self, x, y, blocktype): #x and y may not be negative, and ideally should be integers
		if (y<0 or x<0): return False
		x = int(x)	#make sure x is an integer
		y = int(y)	#make sure y is an integer
		while (y>=self.height): #make sure there are enough rows for the Y index
			self.blocks.append([])
			self.height += 1
		while (len(self.blocks[y]) <= x): #make sure there are enough columns in this row for the X index
			self.blocks[y].append(BLOCK_NONE)
		if (x >= self.width): self.width = x+1
		self.blocks[y][x] = blocktype	#set the appropriate spot on the board
		if (blocktype == BLOCK_BUMPER):
			self.bumpers.append([x+0.5,y+0.5])
		return True

	#returns a real number
	def HeightAt(self, x, y): # x and y may be any real number
		if (x<0 or y<0 or x>=self.width or y>=self.height): return MAX_DEPTH
		blocktype = self.BlockAt(x,y)
		if (blocktype == BLOCK_NONE): return MAX_DEPTH
		elif (blocktype == BLOCK_FLOOR): return 0
		elif (blocktype == BLOCK_WALL): return 1
		elif (blocktype == BLOCK_WALL2): return 1
		elif (blocktype == BLOCK_WALL3): return 1
		elif (blocktype == BLOCK_DOUBLEWALL): return 2
		elif (blocktype == BLOCK_DOUBLEWALL2): return 2
		elif (blocktype == BLOCK_DOUBLEWALL3): return 2
		elif (blocktype == BLOCK_START): return 0
		elif (blocktype == BLOCK_GOAL): return 0
		elif (blocktype == BLOCK_RAMP_RIGHT):	return (x - int(x))
		elif (blocktype == BLOCK_RAMP_LEFT):	return 1.0 - (x-int(x))
		elif (blocktype == BLOCK_RAMP_UP):		return 1.0 - (y-int(y))
		elif (blocktype == BLOCK_RAMP_DOWN):	return (y - int(y))
		elif (blocktype == BLOCK_BUMPER):		return 0
		else: return MAX_DEPTH #unknown block type

	#returns one of the block constants
	def BlockAt(self, x, y): # x and y may be any real number
		if (x<0 or y<0 or x>=self.width or y>=self.height): return BLOCK_NONE
		x = int(x)
		y = int(y)
		if (x >= len(self.blocks[y])): return BLOCK_NONE
		else: return self.blocks[y][x]


	def Draw(self, screen, offset_x, offset_y):
		if (self.image == None):
			self.RenderToImage()
			if (self.image == None): return #an error occurred
		screen.blit(self.image, Rect(offset_x, offset_y, self.image_width, self.image_height))


	def LoadBlockImages(self):
		size = PIXEL_SIZE+PIXEL_BORDER
		self.block_images = [
			None,										# BLOCK_NONE
			LoadImage(self.theme+"floor.png",		size,size),	# BLOCK_FLOOR
			LoadImage(self.theme+"floor2.png",		size,size),	# BLOCK_FLOOR2
			LoadImage(self.theme+"floor3.png",		size,size),	# BLOCK_FLOOR3
			LoadImage(self.theme+"wall.png",		size,size),	# BLOCK_WALL
			LoadImage(self.theme+"wall2.png",		size,size),	# BLOCK_WALL2
			LoadImage(self.theme+"wall3.png",		size,size),	# BLOCK_WALL3
			LoadImage(self.theme+"doublewall.png",	size,size),	# BLOCK_DOUBLEWALL
			LoadImage(self.theme+"doublewall2.png",	size,size),	# BLOCK_DOUBLEWALL2
			LoadImage(self.theme+"doublewall3.png",	size,size),	# BLOCK_DOUBLEWALL3
			LoadImage(self.theme+"startfloor.png",	size,size),	# BLOCK_START
			LoadImage(self.theme+"goal.png",		size,size),	# BLOCK_GOAL
			LoadImage(self.theme+"rampright.png",	size,size),	# BLOCK_RAMP_RIGHT
			LoadImage(self.theme+"rampleft.png",	size,size),	# BLOCK_RAMP_LEFT
			LoadImage(self.theme+"rampup.png",		size,size),	# BLOCK_RAMP_UP
			LoadImage(self.theme+"rampdown.png",	size,size),	# BLOCK_RAMP_DOWN
			LoadImage(self.theme+"bumper.png",		size,size),	# BLOCK_BUMPER
			None #unused
			]

	def RenderToImage(self):
		self.LoadBlockImages()
		self.image_width = self.width * PIXEL_SIZE + PIXEL_BORDER
		self.image_height = self.height * PIXEL_SIZE + PIXEL_BORDER
		#print "rendering image "+str([self.image_width, self.image_height])
		blocksize = PIXEL_SIZE + PIXEL_BORDER
		self.image = pygame.Surface((self.image_width, self.image_height))

		for y in range(self.height):
			for x in range(self.width):
				type = self.BlockAt(x,y)
				if (self.block_images[type]!=None):
					self.image.blit(self.block_images[type], Rect(x*PIXEL_SIZE,y*PIXEL_SIZE,blocksize, blocksize))

