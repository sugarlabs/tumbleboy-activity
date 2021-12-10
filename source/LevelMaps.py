#	This file was created for the game "Tumble Boy", by
#	Bob Rost, Chris Jackson, Eben Myers, and Tom Corbett.
#	Please study it, learn from it, change it, and share it.
from source.Constants import *


def level_init(level_file):
	"""loads the level template file, and parses the data, returning a final set"""
	global map_tile_types
	global level_props

	#set the defaults
	setLevelDefaults()

	#Load File
	lvl = open(level_file)  #do we want to error check this?
	lvl_list = []
	lvl_reached = False
	for lvl_line in lvl:
		if lvl_reached:
			if lvl_line[0:3] == "!!!":
				lvl_reached = False
			else:
				lvl_list.append(parseLine(lvl_line)) #append this line to the list
		else: #not at level yet check for the start cue ("!!!")
			if lvl_line[0] == ".":
				#this is a variable - send the line to be checked
				assess_level_variable(lvl_line)
			if lvl_line[0:3] == "!!!":  #found the start queue
				lvl_reached = True

	#return the level map & properties
	return {"level_attributes": level_props, "level_map":lvl_list}

def level_init(level_file):
	"""loads the level template file, and parses the data, returning a final set"""
	global map_tile_types
	global level_props

	#set the defaults
	setLevelDefaults()

	#Load File
	lvl = open(level_file)  #do we want to error check this?
	lvl_list = []
	lvl_reached = False
	for lvl_line in lvl:
		if lvl_reached:
			if lvl_line[0:3] == "!!!":
				lvl_reached = False
			else:
				lvl_list.append(parseLine(lvl_line)) #append this line to the list
				# lvl_list.append(lvl_line) #append this line to the list
		else: #not at level yet check for the start cue ("!!!")
			if lvl_line[0] == ".":
				#this is a variable - send the line to be checked
				assess_level_variable(lvl_line)
			if lvl_line[0:3] == "!!!":  #found the start queue
				lvl_reached = True

	#return the level map & properties
	return {"level_attributes": level_props, "level_map":lvl_list}

def setLevelDefaults():
	global map_tile_types
	global level_props
	map_tile_types = {}
	map_tile_types[" "]=BLOCK_NONE
	map_tile_types["-"]=BLOCK_FLOOR
	map_tile_types["="]=BLOCK_FLOOR2
	map_tile_types["+"]=BLOCK_FLOOR3
	map_tile_types["#"]=BLOCK_WALL
	map_tile_types["w"]=BLOCK_WALL2
	map_tile_types["W"]=BLOCK_WALL3
	map_tile_types["%"]=BLOCK_DOUBLEWALL
	map_tile_types["d"]=BLOCK_DOUBLEWALL2
	map_tile_types["D"]=BLOCK_DOUBLEWALL3
	map_tile_types["$"]=BLOCK_START
	map_tile_types["1"]=BLOCK_GOAL
	map_tile_types["<"]=BLOCK_RAMP_RIGHT
	map_tile_types[">"]=BLOCK_RAMP_LEFT
	map_tile_types["v"]=BLOCK_RAMP_UP
	map_tile_types["^"]=BLOCK_RAMP_DOWN
	map_tile_types["@"]=BLOCK_BUMPER

	level_props = {}
	#level_props["name"] = "DefaultName"
	#level_props["author"] = ""
	#level_props["theme"] = "DefaultPath"
	#level_props["boy"] = "DefaultPath"
	#level_props["instructions"] = "Default Instructions"
	#level_props["bgcol"] = "#000000"
	#level_props["textcol"] = "#FFFFFF" 

def parseLine(mapline):
	return map(test_map_item, mapline[:-1])
           
def test_map_item(mapitem):
	""" tests an individual character to make sure it is valid"""
	#validate against the list
	if map_tile_types.has_key(mapitem):
		return map_tile_types[mapitem]
	else:
		return BLOCK_NONE
    
def assess_level_variable(lvl_line):
	#look for the space
	level_attribute = get_bracket_info(lvl_line)
	if level_attribute != -1:
		level_props[level_attribute["name"]] = level_attribute["data"]
		#see if the attribute is a valid one
		#if level_props.has_key(level_attribute["name"]):
			#replace the data in that section
			#level_props[level_attribute["name"]] = level_attribute["data"]
    
def get_bracket_info(br_string):
	"""returns an associative array of the bracket name and contents"""
	# attribute data format is:
	# .attname {attdata}
	# returns ["name":attname, "data":attdata]
	wordend = br_string.find(" ")
	bracketstart = br_string.find("{")
	bracketend = br_string.find("}")

	if bracketstart == -1: #no bracket beginning, not a valid attribute
		return -1
	if bracketend == -1: #go to end of line if no closing bracket
		bracketend = len(br_string)
	if (wordend == -1) or (bracketstart < wordend):
		wordend = bracketstart #no space before bracket
		
	attribute = br_string[1:wordend] # 1-index eliminates the '.'
	data = br_string[(bracketstart + 1): bracketend]

	return {"name":attribute, "data": data}
