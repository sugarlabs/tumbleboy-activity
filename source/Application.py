#	This file was created for the game "Tumble Boy", by
#	Bob Rost, Chris Jackson, Eben Myers, and Tom Corbett.
#	Please study it, learn from it, change it, and share it.

from source.Constants import *
from source.Game import *
from source.Graphics import *
from source.Sound import *
from source.LevelMaps import *
import sys, pygame, os, glob
from pygame.locals import *
#import pango #for testing fonts


class Application:
	def __init__(self, pygame_screen):
		print "created application"
		self.screen = pygame_screen
		self.game = Game(pygame_screen, self)	#the main game object
		self.should_quit = False
		self.playing = False
		self.welcome_image = None
		self.win_image = None
		self.win_timer = 0
		self.menu_anim1 = None
		self.menu_anim2 = None
		self.win_anim1 = None
		self.win_anim2 = None
		self.anim_timer = 0

	def WinGame(self):
		self.win_timer = 10

	def Update(self, dt):
		if (self.playing):
			self.game.Update(dt)
			if (self.game.should_quit):
				self.playing = False
		else:
			self.anim_timer += dt
			if (self.anim_timer > 1): self.anim_timer -= 1
			if (self.win_timer > 0):
				self.win_timer -= dt
			pass

	def Draw(self):
		if (self.playing):
			self.game.Draw()
		else:
			self.DrawUI()

	def MouseMoved(self, pos):
		if (self.playing):
			self.game.MouseMoved(pos)

	def KeyPressed(self, key):
		if (self.playing):
			self.game.KeyPressed(key)
		else:
			print "pressed "+str(key)
			if (key == KEY_QUIT): self.should_quit = True
			else: #any key to start the game
				self.game.StartPlaying()
				self.playing = True #start the game

	def KeyReleased(self, key):
		self.game.KeyReleased(key)

	def DrawUI(self):
		if (self.win_timer > 0):
			if (self.win_image == None):
				self.win_image = LoadImage("data/menus/win_game.png", SCREEN_SIZE[0], SCREEN_SIZE[1])
				if (self.win_image == None):
					return
				self.win_anim1 = LoadImage("data/menus/win_anim1.png", WIN_ANIM_RECT[2], WIN_ANIM_RECT[3])
				self.win_anim2 = LoadImage("data/menus/win_anim2.png", WIN_ANIM_RECT[2], WIN_ANIM_RECT[3])
			self.screen.blit(self.win_image, Rect(0,0,SCREEN_SIZE[0],SCREEN_SIZE[1]))
			if (self.anim_timer > 0.5):
				self.screen.blit(self.win_anim1, WIN_ANIM_RECT)
			else:
				self.screen.blit(self.win_anim2, WIN_ANIM_RECT)
		else:
			if (self.welcome_image == None):
				self.welcome_image = LoadImage("data/menus/main_menu.png", SCREEN_SIZE[0], SCREEN_SIZE[1])
				if (self.welcome_image==None):
					print "could not load welcome image"
					return
				self.menu_anim1 = LoadImage("data/menus/menu_anim1.png", MENU_ANIM_RECT[2],MENU_ANIM_RECT[3])
				self.menu_anim2 = LoadImage("data/menus/menu_anim2.png", MENU_ANIM_RECT[2],MENU_ANIM_RECT[3])
			self.screen.blit(self.welcome_image, Rect(0,0,SCREEN_SIZE[0],SCREEN_SIZE[1]))
			if (self.anim_timer > 0.5):
				self.screen.blit(self.menu_anim1, MENU_ANIM_RECT)
			else:
				self.screen.blit(self.menu_anim2, MENU_ANIM_RECT)

