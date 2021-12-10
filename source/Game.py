#	This file was created for the game "Tumble Boy", by
#	Bob Rost, Chris Jackson, Eben Myers, and Tom Corbett.
#	Please study it, learn from it, change it, and share it.


from source.Graphics import *
from source.Board import *
from source.Ball import *
from source.Sound import *
from source.LevelMaps import *
import sys, pygame, os, glob
from pygame.locals import *
#import pango #for testing fonts

class Game:
	def __init__(self, pygame_screen, parent_app):
		self.parent_app = parent_app
		self.should_quit = False
		self.screen = pygame_screen
		self.screen_offset = [0,0]

		self.wait_timer = 0 #post-level wait
		self.good_job_image = None

		self.board = Board()
		self.ball = Ball()

		self.pressed_up = False
		self.pressed_down = False
		self.pressed_right = False
		self.pressed_left = False

		self.level_names = []
		self.next_level = 12
		self.LoadLevelList()
		
		self.level_name = ""
		self.level_name_image = None
		self.level_name_rect = Rect(0,0,0,0)

		self.debug_num_frames = 0
		self.debug_frame_timer = 0

	def StartPlaying(self):
		self.Clear()
		self.should_quit = False
		self.next_level = 0
		self.LoadLevelList()
		self.LoadNextLevel()

	def LoadLevelList(self):
		self.level_names = glob.glob("data/levels/*.txt")
		self.level_names.sort()
		self.next_level = 0
		#print self.level_names

	def LoadNextLevel(self):
		#print "load %i from %s" % (self.next_level, str(self.level_names))
		n = len(self.level_names)
		if (self.next_level >= n):
			self.should_quit = True
			self.parent_app.WinGame()
			return
		filename = self.level_names[self.next_level]
		#print "LOADING LEVEL: "+filename
		self.LoadLevel(filename)
		self.next_level += 1

	def Clear(self):
		self.ball = None
		self.board.Clear()

	def WinLevel(self):
		print "WIN LEVEL"
		PlaySound(SOUND_WIN_LEVEL)
		self.wait_timer = 3.5

	def GetLevelName(self, filename):
		return os.path.splitext(os.path.basename(filename))[0]

	def LoadLevel(self, filename):
		#print "LEVEL NAME "+filename
		self.level_name = self.GetLevelName(filename)
		f = pygame.font.Font(None, 32)
		(fontw, fonth) = f.size(self.level_name)
		self.level_name_image = f.render(self.level_name, True, (255,255,255), (0,0,0,100))
		self.level_name_rect = Rect(10,10,fontw,fonth)

		self.ball = Ball() #reset ball
		self.board.Clear()
		level_info = level_init(filename)
		level_map = level_info['level_map']
		level_attributes = level_info['level_attributes']
		
		for key in level_attributes:
			value = level_attributes[key]
			if (key == 'boy'): self.ball.SetTheme(value)
			if (key == 'theme'): self.board.SetTheme(value)
			#print "%s = %s" % (key, value)

		#BUILD THE BOARD
		cur_row = 0
		for row in level_map:
			cur_col = 0
			for mapsquare in row:
				self.board.SetBlock(cur_col,cur_row,mapsquare)
				cur_col = cur_col + 1
			cur_row = cur_row + 1

		self.ball.SetBoard(self.board)
		startpos = self.board.GetStartPosition()
		self.ball.SetPosition(startpos[0], startpos[1], 0)
		PlaySound(SOUND_START_LEVEL)


	def Update(self, dt):
		if (self.wait_timer > 0):
			self.wait_timer -= dt
			if (self.wait_timer <= 0):
				self.LoadNextLevel()
			return

		#global people
		#self.people.UpdateAnimation(dt)
		force = self.GetKeyDirection()
		self.ball.AddForce(force[0]*dt*BALL_FORCE, force[1]*dt*BALL_FORCE)
		self.ball.Update(dt)
		#if (self.ball.position[1] > 5): self.WinLevel()
		if (self.ball.IsAboveGoal()): self.WinLevel()

		#self.debug_num_frames += 1
		#self.debug_frame_timer += dt
		#if (False and self.debug_frame_timer >= 1.0):
		#	print str(self.debug_num_frames) + "FPS" 
		#	self.debug_num_frames = 0
		#	self.debug_frame_timer -= 1.0
		#self.debug_frame_rate = 1.0 / dt
		pass

	def MouseMoved(self, pos): #pos is an array [x,y]
		#print self.board.HeightAt(pos[0]/64.0, pos[1]/64.0)
		#global people
		#self.people.SetPosition(pos)
		pass

	def KeyPressed(self, key):
		if (key==KEY_UP): self.pressed_up = True
		elif (key==KEY_DOWN): self.pressed_down = True
		elif (key==KEY_LEFT): self.pressed_left = True
		elif (key==KEY_RIGHT): self.pressed_right = True
		elif (key==KEY_QUIT): self.should_quit = True

	def KeyReleased(self, key):
		if (key==KEY_UP): self.pressed_up = False
		elif (key==KEY_DOWN): self.pressed_down = False
		elif (key==KEY_LEFT): self.pressed_left = False
		elif (key==KEY_RIGHT): self.pressed_right = False

	def Draw(self):
		self.screen.fill([0,0,0])
		(offsetx,offsety) = self.GetScreenOffset()
		if (self.board != None): self.board.Draw(self.screen, offsetx, offsety)
		if (self.ball != None): self.ball.Draw(self.screen, offsetx, offsety)
		if (self.wait_timer > 0):
			if (self.good_job_image == None):
				self.good_job_image = LoadImage("data/menus/good_job.png", GOOD_JOB_SIZE[0], GOOD_JOB_SIZE[1])
			if (self.good_job_image != None):
				rx = GOOD_JOB_SIZE[0]*0.5
				ry = GOOD_JOB_SIZE[1]*0.5
				self.screen.blit(self.good_job_image,Rect(
					SCREEN_SIZE[0]*0.5-rx,
					SCREEN_SIZE[1]*0.5-ry,
					rx, ry))
		if (self.level_name_image != None):
			self.screen.blit(self.level_name_image, self.level_name_rect)


	#returns a pair [x,y]
	#positive offset shifts the screen to the right and down (for a ball on the left and top)
	#offsets will generally be negative as the ball goes +x and +y
	def GetScreenOffset(self):
		if (self.ball == None): return [0,0]
		(ox, oy) = (self.screen_offset[0], self.screen_offset[1])
		(px, py, pz) = self.ball.GetPosition()
		px = px*PIXEL_SIZE
		py = py*PIXEL_SIZE
		
		maxx = -(px - SCREEN_MARGIN)
		minx = -(px+SCREEN_MARGIN+BALL_PIXEL_SIZE-SCREEN_SIZE[0])
		maxy = -(py - SCREEN_MARGIN)
		miny = -(py+SCREEN_MARGIN+BALL_PIXEL_SIZE-SCREEN_SIZE[1])
		if (ox < minx): ox = minx
		if (ox > maxx): ox = maxx
		if (oy < miny): oy = miny
		if (oy > maxy): oy = maxy

		#print [ox, oy]
		self.screen_offset = [ox,oy]
		return self.screen_offset

	#def OLDGetScreenOffset(self):
	#	if (self.ball == None): return [0,0]
	#	(ox, oy) = (self.screen_offset[0], self.screen_offset[1])
	#	(px, py, pz) = self.ball.GetPosition()
	#	px = px*PIXEL_SIZE
	#	py = py*PIXEL_SIZE
	#	if (ox > (px - SCREEN_MARGIN)): ox = (SCREEN_MARGIN - px)
	#	elif ((ox+SCREEN_SIZE[0]) < (px+SCREEN_MARGIN+BALL_PIXEL_SIZE)): ox = SCREEN_SIZE[0]-(px+SCREEN_MARGIN+BALL_PIXEL_SIZE)
	#	if (oy > (py - SCREEN_MARGIN)): oy = (SCREEN_MARGIN - py)
	#	elif ((oy+SCREEN_SIZE[1]) < (py+SCREEN_MARGIN+BALL_PIXEL_SIZE)): oy = SCREEN_SIZE[1]-(py+SCREEN_MARGIN+BALL_PIXEL_SIZE)
	#	#print ox
	#	self.screen_offset = [ox,oy]
	#	return self.screen_offset


		
	#returns a vector [dx, dy], based on the arrow keys held down
	def GetKeyDirection(self):
		dx = 0
		dy = 0
		if (self.pressed_up): dy -= 1
		if (self.pressed_down): dy += 1
		if (self.pressed_right): dx += 1
		if (self.pressed_left): dx -= 1
		if (dx!=0 and dy!=0):
			# if dx and dy are both not zero, then our direction magnitude is greater
			# than 1.0, so we can divide by the square root of 2 to re-normalize it.
			dx /= 1.41421
			dy /= 1.41421
		return [dx,dy]

