#	This file was created for the game "Tumble Boy", by
#	Bob Rost, Chris Jackson, Eben Myers, and Tom Corbett.
#	Please study it, learn from it, change it, and share it.

import sys, pygame, os
from pygame.locals import *

def PlaySound(which):
	global sounds
	if (which<0 or which>=len(sounds)): return
	sounds[which].play()

def LoadSounds():
	global sounds
	sounds = [
		None,										# SOUND_NONE
		LoadSound("data/sounds/start_level.ogg"),	# SOUND_START_LEVEL
		LoadSound("data/sounds/lose_ball.ogg"),		# SOUND_LOSE_BALL
		LoadSound("data/sounds/hit_wall.ogg"),		# SOUND_HIT_WALL
		LoadSound("data/sounds/hit_ground.ogg"),	# SOUND_HIT_GROUND
		LoadSound("data/sounds/hit_bumper.ogg"),	# SOUND_HIT_BUMPER
		LoadSound("data/sounds/win_level.ogg"),		# SOUND_WIN_LEVEL
		LoadSound("data/sounds/win_game.ogg"),		# SOUND_WIN_GAME
		None #unused
		]
	#sounds = [
	#	None,										# SOUND_NONE
	#	LoadSound("data/sounds/start_level.wav"),	# SOUND_START_LEVEL
	#	LoadSound("data/sounds/lose_ball.wav"),		# SOUND_LOSE_BALL
	#	LoadSound("data/sounds/hit_wall.wav"),		# SOUND_HIT_WALL
	#	LoadSound("data/sounds/hit_ground.wav"),	# SOUND_HIT_GROUND
	#	LoadSound("data/sounds/hit_bumper.wav"),	# SOUND_HIT_BUMPER
	#	LoadSound("data/sounds/win_level.wav"),		# SOUND_WIN_LEVEL
	#	LoadSound("data/sounds/win_game.wav"),		# SOUND_WIN_GAME
	#	None #unused
	#	]

def LoadSound(filename):
	class NoneSound: #a dummy class in case a sound cannot load
		def play(self): pass
	if (not pygame.mixer or not pygame.mixer.get_init()): #make sure mixer is initialized
		print "mixer not initialized"
		return NoneSound()
	try:
		sound = pygame.mixer.Sound(filename)
	except pygame.error, message:
		print "could not load sound "+filename
		return NoneSound()
	#print "returning sound"
	return sound

