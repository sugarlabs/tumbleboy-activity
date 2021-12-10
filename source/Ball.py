#	This file was created for the game "Tumble Boy", by
#	Bob Rost, Chris Jackson, Eben Myers, and Tom Corbett.
#	Please study it, learn from it, change it, and share it.


from source.Graphics import *
from source.Constants import *
from source.Sound import *
import sys, pygame, os, math
import pygame.transform
from pygame.locals import *

class Ball:
	def __init__(self): #, pygame_screen):
		self.on_ground = True
		self.position = [0,0,0] #3d position
		self.velocity = [0,0,0] #3d velocity
		self.board = None
		self.images = None

		self.anim_pose = BOY_RESTING
		self.anim_frame = 0	#must be either 0 or 1
		self.anim_timer = 0	#determine
		self.SetTheme("boy1")

	def SetTheme(self, folder_name):
		self.theme = "data/themes/"+folder_name+"/"
		self.images = None

	def SetBoard(self, board):
		self.board = board

	def AddForce(self, dx, dy):
		(vx,vy,vz) = self.velocity
		start_speed = math.sqrt(vx*vx + vy*vy + vz*vz)
		vx += dx
		vy += dy
		end_speed = math.sqrt(vx*vx + vy*vy + vz*vz)
		if (start_speed>=MAX_SPEED and end_speed>start_speed):
			return #don't let players accelerate faster than max speed
		self.velocity = [vx, vy, vz]

	def IsAboveGoal(self):
		if (self.board == None): return False
		type = self.board.BlockAt(self.position[0]+0.5, self.position[1]+0.5)
		return (type == BLOCK_GOAL)

	def Update(self, dt):
		(vx,vy,vz) = self.velocity
		(px,py,pz) = self.position
		if (pz <= MAX_DEPTH and self.board!=None):
			startpos = self.board.GetStartPosition()
			self.SetPosition(startpos[0], startpos[1], 0)
			self.velocity = [0,0,0]
			self.on_ground = False
			PlaySound(SOUND_LOSE_BALL)
			return

		if (self.on_ground):
			vx -= vx*BALL_DRAG
			vy -= vy*BALL_DRAG
			self.velocity = [vx,vy,vz]
		px += vx*dt
		py += vy*dt
		pz += vz*dt

		if (self.board == None):
			self.position = [px, py, pz]
			return

		#collide with bumpers
		if (pz>=-1 and pz<=BUMPER_HEIGHT):
			b = self.board.GetCollidingBumper(px+0.5,py+0.5) #center of the ball
			if (b!=None):
				dx = b[0]-0.5-px
				dy = b[1]-0.5-py
				angle = math.atan2(dy, dx)
				vx = -math.cos(angle)*BUMPER_SPEED
				vy = -math.sin(angle)*BUMPER_SPEED
				self.velocity = [vx,vy,vz]
				self.position = [
					self.position[0]+vx*dt,
					self.position[1]+vy*dt,
					self.position[2]]
				#print "angle=%f, radius=%0.02f pos (%0.02f, %0.02f, %0.02f), vel (%0.02f, %0.02f, %0.02f)" % \
				#	(angle, b[2], \
				#	self.position[0], self.position[1], self.position[2], \
				#	self.velocity[0], self.velocity[1], self.velocity[2])
				PlaySound(SOUND_HIT_BUMPER)
				return

		#collide with level
		height_beneath = self.board.HeightAt(px+0.5,py+0.5)
		if (height_beneath < pz): #no floor beneath
			self.on_ground = False
			vz += -GRAVITY*dt
		elif (height_beneath > pz): #hit the ground
			if (-vz >= GROUND_SOUND_SPEED): PlaySound(SOUND_HIT_GROUND)
			if (vz >= 0): #going up a ramp
				pz = height_beneath
				vz = (height_beneath - pz) / dt
				self.on_ground = False
			else:
				pz = height_beneath
				vz = 0
				self.on_ground = True

		#shift ball away from wall if in it
		height_left = self.board.HeightAt(px+0.5-BALL_RADIUS,py+0.5)
		height_right = self.board.HeightAt(px+0.5+BALL_RADIUS,py+0.5)
		height_up = self.board.HeightAt(px+0.5,py+0.5-BALL_RADIUS)
		height_down = self.board.HeightAt(px+0.5,py+0.5+BALL_RADIUS)
		myz = pz+0.5
		if (height_left>myz):		self.position[0] = self.position[0]+0.02
		elif (height_right>myz):	self.position[0] = self.position[0]-0.02
		if (height_up>myz):			self.position[1] = self.position[1]+0.02
		elif (height_down>myz):		self.position[1] = self.position[1]-0.02

		dx = 0
		if (vx > 0): dx = BALL_RADIUS
		elif (vx < 0): dx = -BALL_RADIUS

		dy = 0
		if (vy > 0): dy = BALL_RADIUS
		elif (vy < 0): dy = -BALL_RADIUS

		height_x = self.board.HeightAt(px+0.5+dx, py+0.5)
		height_y = self.board.HeightAt(px+0.5, py+0.5+dy)
		speed = math.sqrt(vx*vx + vy*vy)
		if (height_x - pz >= BALL_CLIMB):
			vx = -vx*WALL_ELASTICITY
			if (speed >= WALL_SOUND_SPEED): PlaySound(SOUND_HIT_WALL)
		if (height_y - pz >= BALL_CLIMB):
			vy = -vy*WALL_ELASTICITY
			if (speed >= WALL_SOUND_SPEED): PlaySound(SOUND_HIT_WALL)

		px = self.position[0]+vx*dt
		py = self.position[1]+vy*dt
		self.position = [px,py,pz]
		self.velocity = [vx,vy,vz]

		self.anim_timer += speed*dt
		if (self.anim_timer > 0.2):
			self.anim_timer = 0
			self.anim_frame = (self.anim_frame+1)%2
		if (vx > ANIM_LEAN_SPEED): self.anim_pose = BOY_RIGHT
		elif (vx < -ANIM_LEAN_SPEED): self.anim_pose = BOY_LEFT
		elif (vy < -ANIM_LEAN_SPEED): self.anim_pose = BOY_UP
		elif (vy > ANIM_LEAN_SPEED): self.anim_pose = BOY_DOWN
		else: self.anim_pose = BOY_RESTING
		#print "position (%0.02f, %0.02f, %0.02f)" % (px,py,pz)


	def SetPosition(self,x,y,z):
		self.position = [x,y,z]

	def GetPosition(self):
		return self.position

	def Draw(self, screen, offsetx, offsety):
		if (self.images == None):
			self.SetupImages()
			if (self.images == None): return #error occurred
		scale_index = self.ScaleIndex(self.position[2])
		(w,h,offsx,offsy) = self.images[scale_index][0]
		screen.blit(
			self.images[scale_index][1][self.anim_pose+self.anim_frame],
			Rect(
				self.position[0]*PIXEL_SIZE + offsetx - BALLSPRITE_OFFSETX + offsx,
				self.position[1]*PIXEL_SIZE + offsety - BALLSPRITE_OFFSETY + offsy,
				w, h))

	def ScaleIndex(self, z):
		#1.0 scale is at index 2
		index = (z+1.25) / 0.5
		if (index < 0): return 0
		elif (index >= 5): return 5
		else: return int(index)
		z = z+0.75

	def SetupImages(self):
		#boy sprites are 70 x 81 pixels
		theme = self.theme
		boy_images = [
			LoadImage(theme+"tbrest1.png"),		# BOY_RESTING frame 1
			LoadImage(theme+"tbrest2.png"),		# BOY_RESTING frame 2
			LoadImage(theme+"tbright1.png"),	# BOY_RIGHT frame 1
			LoadImage(theme+"tbright2.png"),	# BOY_RIGHT frame 2
			LoadImage(theme+"tbleft1.png"),		# BOY_LEFT frame 1
			LoadImage(theme+"tbleft2.png"),		# BOY_LEFT frame 2
			LoadImage(theme+"tbup1.png"),		# BOY_UP frame 1
			LoadImage(theme+"tbup2.png"),		# BOY_UP frame 2
			LoadImage(theme+"tbdown1.png"),		# BOY_DOWN frame 1
			LoadImage(theme+"tbdown2.png"),		# BOY_DOWN frame 2
			]
		#print boy_images
		self.images = [
			self.ResizedImageList(boy_images, 0.8),
			self.ResizedImageList(boy_images, 0.9),
			self.ResizedImageList(boy_images, 1.0),
			self.ResizedImageList(boy_images, 1.05),
			self.ResizedImageList(boy_images, 1.1),
			self.ResizedImageList(boy_images, 1.15)
			]
		self.anim_pose = BOY_RESTING
		self.anim_frame = 0

	def ResizedImageList(self, images, scale):
		width = int(scale * BALLSPRITE_WIDTH)
		height = int(scale * BALLSPRITE_HEIGHT)
		offsx = (BALLSPRITE_WIDTH - width)*0.5
		offsy = (BALLSPRITE_HEIGHT - height)*0.5
		resized_images = []
		for i in images:
			resized_images.append(pygame.transform.scale(i, (width, height)))
		return [[width, height, offsx, offsy], resized_images]
