#	This file was created for the game "Tumble Boy", by
#	Bob Rost, Chris Jackson, Eben Myers, and Tom Corbett.
#	Please study it, learn from it, change it, and share it.

from pygame.locals import * #for Rect object

use_small_screen = False
if (use_small_screen): scale = 1.0
else: scale = (825.0 / 480.0) #scale up to XO screen size (native is 1200x825)

#scale = 600.0/480.0

SCREEN_SIZE = [640*scale, 480*scale]
SCREEN_MARGIN		=	200*scale		# Amount of border to have on the screen to show the ball
PIXEL_SIZE			=	64*scale		# Standard pixel size of a block
PIXEL_BORDER		=	12*scale		# Pixel border for depth cues
BALL_PIXEL_SIZE		=	64*scale		# Size of the ball in pixels
BALLSPRITE_OFFSETX	=	2*scale		# Additional pixels X to offset ball sprite
BALLSPRITE_OFFSETY	=	15*scale		# Additional pixels Y to offset ball sprite
BALLSPRITE_WIDTH	=	70*scale		# Pixel width of the ball sprite
BALLSPRITE_HEIGHT	=	81*scale		# Pixel height of the ball sprite
GOOD_JOB_SIZE		=	[300*scale,300*scale]	# Pixel size of the good job sprite
MENU_ANIM_RECT		=	Rect(460*scale,260*scale,140*scale,162*scale)	# Bounds of the animated boy on the title screen
WIN_ANIM_RECT		=	Rect(326*scale,0, 105*scale,116*scale)

MAX_SPEED			=	2.0		# Maximum normal roll speed, in blocks per second.
BUMPER_SPEED		=	4.0		# Speed that a ball is thrown from a bumper block.
GRAVITY				=	8.0		# Amount of gravity to apply to a falling object.
MAX_DEPTH			=	-5.0	# Depth when a ball is considered lost.
BALL_FORCE			=	1
BALL_DRAG			=	0.003		# Drag applied to ball while rolling
WALL_ELASTICITY		=	0.6
BALL_CLIMB			=	0.75	# Highest amount a ball may immediately climb
BALL_RADIUS			=	0.45	# Ball's collision radius
BUMPER_HEIGHT		=	0.2

ANIM_LEAN_SPEED		=	0.25	# Minimum speed to use lean animations
GROUND_SOUND_SPEED	=	2		# Minimum speed for hitting ground to make a sound
WALL_SOUND_SPEED	=	1		# Minimum speed for hitting wall to make a sound

KEY_UP		=	273
KEY_DOWN	=	274
KEY_LEFT	=	276
KEY_RIGHT	=	275
KEY_QUIT	=	27

# The order of these BLOCK_* values must match the function LoadBlockImages() in Board.py
BLOCK_NONE			=	0		# Empty space. The ball will fall through this.
BLOCK_FLOOR			=	1		# Standard floor. The ball will roll on this.
BLOCK_FLOOR2		=	2		# Standard floor. The ball will roll on this.
BLOCK_FLOOR3		=	3		# Standard floor. The ball will roll on this.
BLOCK_WALL			=	4		# Standard wall. The ball will collide with this, or may roll on top.
BLOCK_WALL2			=	5		# Standard wall. The ball will collide with this, or may roll on top.
BLOCK_WALL3			=	6		# Standard wall. The ball will collide with this, or may roll on top.
BLOCK_DOUBLEWALL	=	7		# Double-high wall. The ball will collide with this.
BLOCK_DOUBLEWALL2	=	8		# Double-high wall. The ball will collide with this.
BLOCK_DOUBLEWALL3	=	9		# Double-high wall. The ball will collide with this.
BLOCK_START			=	10		# Player starting block
BLOCK_GOAL			=	11		# Level ending goal block
BLOCK_RAMP_RIGHT	=	12		# Ramp leading right
BLOCK_RAMP_LEFT		=	13		# Ramp leading left
BLOCK_RAMP_UP		=	14		# Ramp leading up
BLOCK_RAMP_DOWN		=	15		# Ramp leading down
BLOCK_BUMPER		=	16		# Spring-loaded bumper

# The order of these SOUND_* values must match the function LoadSounds() in Sound.py
SOUND_NONE			=	0
SOUND_START_LEVEL	=	1
SOUND_LOSE_BALL		=	2
SOUND_HIT_WALL		=	3
SOUND_HIT_GROUND	=	4
SOUND_HIT_BUMPER	=	5
SOUND_WIN_LEVEL		=	6
SOUND_WIN_GAME		=	7

#The order of these BOY_* values must be even numbers, for the functions in Ball.py
BOY_RESTING			=	0
BOY_RIGHT			=	2
BOY_LEFT			=	4
BOY_UP				=	6
BOY_DOWN			=	8
