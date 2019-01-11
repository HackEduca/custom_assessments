#Jean Salac
#Unit 2 Question Generator. Run with the following command: python unit2QuestionGenerator.py scratchStudioURL

import sys
import json
import requests
from pprint import pprint
import copy
import re
import random
import time
from bs4 import BeautifulSoup


#Scratch Sprite Class
class Sprite(object):
	name = ''
	scripts = [] #list of different block groups
	parent = ''
	children = []
	instructions = [] #need to allow for different sets of instructions. A list of sets of instructions

	def __init__(self, name):
		self.name = name
		self.scripts = []
		self.parent = ''
		self.children = []
		self.instructions = []
	
	def __str__(self):
		return "Sprite's Name: "+ self.name
	def __repr__(self):
		return "Sprite's Name: "+ self.name

#Sprite Constructor
def make_sprite(name):
	sprite = Sprite(name)
	return sprite

#Scratch Project Class.
class Project(object):
	ID = ''
	scripts = ''
	questions = ''
	username = '' #Scratch username
	lenQ7 = 4 #Num blocks in q7 script. Default is 4

	def __init__(self, ID):
		self.ID = ID
		self.scripts = []
		self.questions = []
		self.username = ''
		self.lenQ7 = 4

	def __str__(self):
		return "Project's Name: "+ self.ID
	def __repr__(self):
		return "Project's Name: "+ self.ID

#Project Constructor
def make_project(name):
	project = Project(name)
	return project


#Question Constructor
class Question(object):
	ID = '' #Question's ID 
	scripts = [] #Scripts that are part of the question
	scrBlks= [] #Question scripts converted to Scratchblocks syntax


	def __init__(self, ID):
		self.ID = ID
		self.scripts = []
		self.scrBlks = []

	def __str__(self):
		return "Question ID: "+ self.ID
	def __repr__(self):
		return "Question ID: "+ self.ID

#Question Constructor
def make_question(name):
	question = Question(name)
	return question


#Method to convert Scratch URL to URL needed to fetch json project
def scratch_to_API(scratch_URL):
	api_prefix = "http://projects.scratch.mit.edu/internalapi/project/"
	api_suffix = "/get/"
	project_id = "" 
	for char in scratch_URL:
		if char.isdigit():
			project_id = project_id+char
	api_URL = api_prefix + project_id + api_suffix
	return api_URL

#Method to convert Studio URL to URL needed to get Scratch IDs
def studio_to_API(studio_URL):
	api_prefix = "https://scratch.mit.edu/site-api/projects/in/"
	api_suffix = "/1/"
	project_id = "" 
	for char in studio_URL:
		if char.isdigit():
			project_id = project_id+char
	api_URL = api_prefix + project_id + api_suffix
	return api_URL


#Method to retrieve project ID from Scratch project URL
def get_proj_id(scratch_URL):
	project_id = ""
	for char in scratch_URL:
		if char.isdigit():
			project_id = project_id+char
	return project_id


#Method to iterate through the tree/list
def traverse(o, tree_types=(list,tuple)):
	if isinstance(o, tree_types):
		for value in o:
			for subvalue in traverse(value, tree_types):
				yield subvalue
	else:
		yield o


#Recursive method to find the opcode of interest
def find_index(my_list, target):
	for index, item in enumerate(my_list):
		if item == target:
			return [index]
		if isinstance(item,(list, tuple)):
			path = find_index(item, target)
			if path:
				return [index] + path
	return []

#Method to check if a string can be represented as a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#Methods to generate questions. Takes in the baseline question and project

#Question 3: Find 1 green flag script, 1 spriteClicked, 1 keyPressed from their code. Hard-code 1 spriteClicked script.
def custom_q3(Question, Project):
	#Find replacement for GreenFlag script
	gf_index = find_index(Project.scripts, 'whenGreenFlag')
	#Check if there was a green flag script 
	if len(gf_index)>0:
		potential_script = Project.scripts[gf_index[0]][gf_index[1]] 
		
		#Find any of the excluded blocks in the potential script.
		hasExc = False
		for opcode in exc_opcodes:
			exc_index = find_index(potential_script,opcode)
			if len(exc_index) > 0:
				hasExc = True
				break
		#Check if 3-4 blocks long, including the hat block, and no excluded blocks.
		if len(potential_script)>2 and len(potential_script) <5 and hasExc is False:
			Question.scripts[3] = potential_script

	#Find replacement for spriteClicked script
	sprite_index = find_index(Project.scripts, 'whenClicked')
	#Check if there was a spriteClicked script 
	if len(sprite_index)>0:
		potential_script = Project.scripts[sprite_index[0]][sprite_index[1]] 
		
		#Find any of the excluded blocks in the potential script.
		hasExc = False
		for opcode in exc_opcodes:
			exc_index = find_index(potential_script,opcode)
			if len(exc_index) > 0:
				hasExc = True
				break
		#Check if 3-4 blocks long, including the hat block, and no excluded blocks.
		if len(potential_script)>2 and len(potential_script) <5 and hasExc is False:
			Question.scripts[1] = potential_script

	#Find replacement for keyPressed script
	key_index = find_index(Project.scripts, 'whenKeyPressed')
	#Check if there was a keyPressed script 
	if len(key_index)>0:
		potential_script = Project.scripts[key_index[0]][key_index[1]] 
		
		#Find any of the excluded blocks in the potential script.
		hasExc = False
		for opcode in exc_opcodes:
			exc_index = find_index(potential_script,opcode)
			if len(exc_index) > 0:
				hasExc = True
				break
		#Check if 3-4 blocks long, including the hat block, and no excluded blocks.
		if len(potential_script)>2 and len(potential_script) <5 and hasExc is False:
			Question.scripts[2] = potential_script




#Question 6: Find a "When Green Flag". No loops, conditionals, variables, play sound.
def custom_q6(Question,Project):
	gf_index = find_index(Project.scripts, 'whenGreenFlag')	
	#Check if there was a green flag script 
	if len(gf_index)>0:
		potential_script = Project.scripts[gf_index[0]][gf_index[1]] 
		
		#Find any of the excluded blocks in the potential script.
		hasExc = False
		for opcode in exc_opcodes:
			exc_index = find_index(potential_script,opcode)
			if len(exc_index) > 0:
				hasExc = True
				break

		#Check if 4 blocks long, including the GF block, and no excluded blocks.
		if len(potential_script)==4 and hasExc is False:
			Question.scripts[0] = potential_script

		#Delete greenFlag script so it doesn't get used for question 7
		del(Project.scripts[gf_index[0]])
	

#Question 7: Find a spriteClicked or GreenFlag. No loops, conditionals, variables, play sound.
def custom_q7(Question,Project):
	#Find spriteClicked script
	sprite_index = find_index(Project.scripts, 'whenClicked')
	#Check if there was a spriteClicked script 
	if len(sprite_index)>0:
		potential_script = Project.scripts[sprite_index[0]][sprite_index[1]] 
		
		#Find any of the excluded blocks in the potential script.
		hasExc = False
		for opcode in exc_opcodes:
			exc_index = find_index(potential_script,opcode)
			if len(exc_index) > 0:
				hasExc = True
				break
		#Check if 3-4 blocks long, including the hat block, and no excluded blocks.
		if len(potential_script)>1 and len(potential_script) <5 and hasExc is False:
			Question.scripts[0] = potential_script
	
	else:
		gf_index = find_index(Project.scripts, 'whenGreenFlag')	
		#Check if there was a green flag script 
		if len(gf_index)>0:
			potential_script = Project.scripts[gf_index[0]][gf_index[1]] 
			
			#Find any of the excluded blocks in the potential script.
			hasExc = False
			for opcode in exc_opcodes:
				exc_index = find_index(potential_script,opcode)
				if len(exc_index) > 0:
					hasExc = True
					break

			#Check if 2-4 blocks long, including the GF block, and no excluded blocks.
			if len(potential_script)>1 and len(potential_script) <5 and hasExc is False:
				Question.scripts[0] = potential_script



#Method to decide if a project is going to get a custom question. 
#Args: List of projects, question number, baseline Question object, csv file to print custom projects & non custom projects
def decideCustom(list, numQ, Question, csvCustom, csvNoCustom):
	if len(list) > 0:
		#If list is even, shuffle and split in half.
		if len(list)%2==0:
			random.shuffle(list)
			for x in range(0, len(list)):
				if x < len(list)/2: #First half gets noncustom question
					list[x].questions[numQ] = copy.deepcopy(Question)
					print>>csvNoCustom, list[x].username+','+list[x].ID
				else:
					print>>csvCustom, list[x].username+','+list[x].ID
		else:
			random.shuffle(list)
			for x in range(0, len(list)-1):
				if x < len(list)/2: #First half gets noncustom question
					list[x].questions[numQ] = copy.deepcopy(Question)
					print>>csvNoCustom, list[x].username+','+list[x].ID
				else:
					print>>csvCustom, list[x].username+','+list[x].ID
			
			#Last odd element custom/generic is based on timestamp
			ts = str(time.time())
			rand_digit = int(ts[random.randint(1,len(ts)-4)])
			last = len(list)-1
			if rand_digit%2==0: #If even, get a generic question
				list[last].questions[numQ] = copy.deepcopy(Question)
				print>>csvNoCustom, list[last].username+','+list[last].ID
			else:
				print>>csvCustom, list[last].username+','+list[last].ID



#Conversion to Scratchblocks format
#Populate dictionary of opcode to block translations from txt files with opcodes and blocks
opcode_dict= {}
def populate_opcode_dict():
	global opcode_dict
	opcode_dict = {'changeXposBy:': 'change x by ()', 'show': 'show', 
	'whenIReceive': 'when I receive ()', '/': '() / ()', 
	'getParam': 'custom block parameter', 'rounded': 'round ()', 
	'doForLoop': 'for each () in ()', 'lookLike:': 'switch costume to ()', 
	'sayNothing': 'say nothing', 'timeAndDate': 'current ()', 
	'color:sees:': 'color () is touching ()?', 'changeSizeBy:': 'change size by ()', 
	'setSizeTo:': 'set size to ()%', 'fxTest': 'color fx test ()', 
	'turnRight:': 'turn right () degrees', 'mousePressed': 'mouse down?', 
	'concatenate:with:': 'join ()()', 'doPlaySoundAndWait': 'play sound () until done',
	'lineCountOfList:': 'length of ()', 'timestamp': 'days since 2000', 
	'setVideoTransparency': 'set video transparency to ()%', 
	'setLine:ofList:to:': 'replace item () of () With ()', 'warpSpeed': 'all at once', 
	'getUserId': 'user id', 'computeFunction:of:': '() of ()', 'nextCostume': 'next costume', 
	'not': 'not ()', 'changeYposBy:': 'change y by ()', 'gotoX:y:': 'go to x: () y: ()', 
	'whenClicked': 'when this sprite clicked', 'setVideoState': 'turn video ()', 
	'costumeIndex': 'costume #', 'wait:elapsed:from:': 'wait () secs', 
	'setPenHueTo:': 'set pen color to ()', 'scrollRight': 'scroll right ()', 
	'setRotationStyle': 'set rotation style ()', 'whenGreenFlag': 'when green flag clicked', 
	'stopAllSounds': 'stop all sounds', 'goBackByLayers:': 'go back () layers', 'heading': 'direction', 
	'setPenShadeTo:': 'set pen shade to ()', 'penSize:': 'set pen size to ()', 
	'playSound:': 'play sound ()', 'playDrum': 'play drum () for () beats', 
	'setTempoTo:': 'set tempo to () bpm', 'obsolete': 'obsolete', 
	'rest:elapsed:from:': 'rest for () beats', 'xpos:': 'set x to ()', 'doWhile': 'while ()', 
	'sensor:': '() sensor value', 'changePenSizeBy:': 'change pen size by ()', 
	'doWaitUntil': 'wait until ()', 'randomFrom:to:': 'pick random () to ()', 
	'letter:of:': 'letter () of ()', 'getLine:ofList:': 'item () of ()', 'stopAll': 'stop all', 
	'scale': 'size', 'hide': 'hide', 'hideAll': 'hide all sprites', 
	'doBroadcastAndWait': 'broadcast () and wait', '+': '() + ()', 'stopSound:': 'stop sound ()', 
	'contentsOfList:': '()', 'changeVar:by:': 'change () by ()', 'sensorPressed:': 'sensor ()?', 
	'abs': 'abs ()', 'changeGraphicEffect:by:': 'change () effect by ()', 
	'changePenHueBy:': 'change pen color by ()', 'COUNT': 'counter', 'tempo': 'tempo', 
	'hideList:': 'hide list ()', 'costumeName': 'costume name', 'say:': 'say ()', 
	'ypos': 'y position', 'think:': 'think ()', 'distanceTo:': 'distance to ()', 
	'whenKeyPressed': 'when () key pressed', 'filterReset': 'clear graphic effects', 
	'doUntil': 'repeat until ()', 'soundLevel': 'loudness', 'penColor:': 'set pen color to ()', 
	'broadcast:': 'broadcast ()', 'startScene': 'switch backdrop to ()', 'deleteClone': 'delete this clone', 
	'senseVideoMotion': 'video () on ()', 'timer': 'timer', '|': '() or ()', 
	'whenSceneStarts': 'when backdrop switches to ()', 'bounceOffEdge': 'if on edge, bounce', 
	'setGraphicEffect:to:': 'set () effect to ()', 'CLR_COUNT': 'clear counter', 
	'list:contains:': '() contains ()', 'doForeverIf': 'forever if ()', 'stringLength:': 'length of ()', 
	'hideVariable:': 'hide variable ()', 'readVariable': '() (Variables block)', 
	'midiInstrument:': 'set instrument to ()', 'doAsk': 'ask () and wait', 'doIf': 'if () then', 
	'backgroundIndex': 'backdrop #', 'deleteLine:ofList:': 'delete () of ()', 
	'changeVolumeBy:': 'change volume by ()', '&': '() and ()', 'getAttribute:of:': '() of ()', 
	'*': '() * ()', 'startSceneAndWait': 'switch backdrop to () and wait', 
	'changePenShadeBy:': 'change pen shade by ()', 'doRepeat': 'repeat ()', '>': '() > ()', 
	'instrument:': 'set instrument to ()', 'xpos': 'x position', 
	'think:duration:elapsed:from:': 'think () for () secs', 'nextScene': 'next backdrop', 
	'forward:': 'move () steps', 'volume': 'volume', 'mouseY': 'mouse y', 'mouseX': 'mouse x', 
	'showList:': 'show list ()', 'whenSensorGreaterThan': 'when () is greater than ()', 
	'gotoSpriteOrMouse:': 'go to ()', 'insert:at:ofList:': 'insert () at () of ()', 
	'sceneName': 'backdrop name', 'doForever': 'forever', '<': '() < ()', 
	'glideSecs:toX:y:elapsed:from:': 'glide () Secs to X: () Y: ()', 'stopScripts': 'stop ()', 
	'turnAwayFromEdge': 'point away from edge', 'noteOn:duration:elapsed:from:': 'play note () for () beats', 
	'ypos:': 'set y to ()', 'clearPenTrails': 'clear', 'drum:duration:elapsed:from:': 'play drum () for () beats', 
	'touchingColor:': 'touching color ()?', 'xScroll': 'x scroll', 'doIfElse': 'if () then, else', 
	'keyPressed:': 'key () pressed?', 'pointTowards:': 'point towards ()', 'putPenDown': 'pen down', 
	'setVar:to:': 'set () to ()', '%': '() mod ()', '-': '() - ()', 'sqrt': 'sqrt ()', 
	'showVariable:': 'show variable ()', 'answer': 'answer', 'putPenUp': 'pen up', '=': '() = ()', 
	'isLoud': 'loud?', 'append:toList:': 'add () to ()', 'whenCloned': 'when I start as a clone', 
	'timerReset': 'reset timer', 'comeToFront': 'go to front', 'INCR_COUNT': 'incr counter', 
	'setVolumeTo:': 'set volume to ()%', 'scrollUp': 'scroll Up ()', 'turnLeft:': 'turn left () degrees', 
	'doReturn': 'stop script', 'heading:': 'point in direction ()', 'stampCostume': 'stamp', 
	'getUserName': 'username', 'yScroll': 'y scroll', 'touching:': 'touching ()?', 'undefined': 'undefined', 
	'changeTempoBy:': 'change tempo by ()', 'scrollAlign': 'align scene ()', 'createCloneOf': 'create clone of ()', 
	'say:duration:elapsed:from:': 'say () for () secs'}

#Global lists for picture conversion. Look into JS library for picture conversion
bool_opcodes = []
def populate_bool_opcodes():
	global bool_opcodes
	bool_opcodes = ["touching:","touchingColor:","color:sees:",
	"mousePressed","keyPressed:","sensorPressed:",
	"<","=",">","&","|","not","list:contains:"]

reporter_opcodes = []
def populate_reporter_opcodes():
	global reporter_opcodes
	reporter_opcodes = ["xpos","ypos","heading","costumeIndex","backgroundIndex", 
	"scale","volume", "tempo", "answer", "mouseX", "mouseY", "distanceTo:", 
	"timer","computeFunction:of:","soundLevel","sensor:", "getUserName","+","-", 
	"*","/","randomFrom:to:","concatenate:with:","letter:of:","lineCountOfList:","%",
	"rounded","getLine:ofList:","lineCountOfList:","timeAndDate","timestamp"]

arg_opcodes = []
def populate_arg_opcodes():
	global arg_opcodes
	arg_opcodes = ["-","*","/","&","%","+","<","=",">","|","abs","append:toList:",
	"broadcast:","changeGraphicEffect:by:","changePenHueBy:","changePenShadeBy:",
	"changePenSizeBy:","changeSizeBy:","changeTempoBy:","changeVar:by:","changeVolumeBy:",
	"changeXposBy:","changeYposBy:","color:sees:","computeFunction:of:","concatenate:with:",
	"contentsOfList:","createCloneOf","deleteLine:ofList:","distanceTo:","doAsk",
	"doBroadcastAndWait","doForeverIf","doForLoop","doIf","doIfElse","doPlaySoundAndWait",
	"doRepeat","doUntil","doWaitUntil","doWhile","drum:duration:elapsed:from:","forward:",
	"fxTest","getAttribute:of:","getLine:ofList:","glideSecs:toX:y:elapsed:from:",
	"goBackByLayers:","gotoSpriteOrMouse:","gotoX:y:","heading:",
	"hideList:","hideVariable:","insert:at:ofList:","instrument:","keyPressed:",
	"letter:of:","lineCountOfList:","list:contains:","lookLike:","midiInstrument:","not",
	"noteOn:duration:elapsed:from:","penColor:","penSize:","playDrum","playSound:",
	"pointTowards:","randomFrom:to:","readVariable","rest:elapsed:from:","rounded",
	"say:","say:duration:elapsed:from:","scrollAlign","scrollRight","scrollUp",
	"senseVideoMotion","sensor:","sensorPressed:","setGraphicEffect:to:",
	"setLine:ofList:to:","setPenHueTo:","setPenShadeTo:","setRotationStyle","setSizeTo:",
	"setTempoTo:","setVar:to:","setVideoState","setVideoTransparency","setVolumeTo:",
	"showList:","showVariable:","sqrt","startScene","startSceneAndWait","stopScripts",
	"stopSound:","stringLength:","think:","think:duration:elapsed:from:","timeAndDate",
	"touching:","touchingColor:","turnLeft:","turnRight:","wait:elapsed:from:",
	"whenIReceive","whenKeyPressed","whenSceneStarts","whenSensorGreaterThan",
	"xpos:","ypos:"]

one_arg_opcodes =[]
def populate_one_arg():
	global one_arg_opcodes
	one_arg_opcodes = ["abs", "broadcast:","changePenHueBy:","changePenShadeBy:",
	"changePenSizeBy:","changeSizeBy:","changeTempoBy:","changeVolumeBy:",
	"changeXposBy:","changeYposBy:","contentsOfList:","createCloneOf","distanceTo:","doAsk",
	"doBroadcastAndWait","doForeverIf","doForLoop","doIf","doIfElse","doPlaySoundAndWait",
	"doRepeat","doUntil","doWaitUntil","doWhile","forward:","fxTest","goBackByLayers:","gotoSpriteOrMouse:",
	"heading:","hideList:","hideVariable:","instrument:","keyPressed:","lineCountOfList:","lookLike:",
	"midiInstrument:","not","penColor:","penSize:","playSound:","pointTowards:",
	"readVariable","rest:elapsed:from:","rounded","say:","scrollAlign","scrollRight","scrollUp","sensor:",
	"sensorPressed:","setPenHueTo:","setPenShadeTo:","setRotationStyle","setSizeTo:",
	"setTempoTo:","setVideoState","setVideoTransparency","setVolumeTo:","showList:",
	"showVariable:","sqrt","startScene","startSceneAndWait","stopScripts","stopSound:",
	"stringLength:","think:","timeAndDate","touching:","touchingColor:","turnLeft:","turnRight:",
	"wait:elapsed:from:","whenIReceive","whenKeyPressed","whenSceneStarts","whenSensorGreaterThan",
	"xpos:","ypos:"]

two_arg_opcodes =[]
def populate_two_arg():
	global two_arg_opcodes
	two_arg_opcodes = ["-","*","/","&","%","+","<","=",">","|", "append:toList:",
	"changeGraphicEffect:by:","changeVar:by:","color:sees:","computeFunction:of:",
	"concatenate:with:","deleteLine:ofList:","drum:duration:elapsed:from:","getAttribute:of:",
	"getLine:ofList:","gotoX:y:","insert:at:ofList:","letter:of:","list:contains:",
	"noteOn:duration:elapsed:from:","playDrum","randomFrom:to:","say:duration:elapsed:from:",
	"senseVideoMotion","setGraphicEffect:to:","setVar:to:","think:duration:elapsed:from:"]

three_arg_opcodes =[]
def populate_three_arg():
	global three_arg_opcodes
	three_arg_opcodes = ["glideSecs:toX:y:elapsed:from:","setLine:ofList:to:",]

c_opcodes = []
def populate_c_opcodes():
	global c_opcodes
	c_opcodes = ["doForever", "doRepeat", "doIf","doIfElse","doUntil"]

#Opcodes for blocks beyond the scope of this unit and are exluded from custom blocks
#No loops, conditionals, variables, play sound 
exc_opcodes= []
def populate_exc_opcodes():
	global exc_opcodes
	exc_opcodes = ["doForever", "doRepeat", "doIf","doIfElse","doUntil","playSound:","readVariable","showVariable:","hideVariable:"]



def main():
	
	#Populate lists of opcodes necessary
	populate_bool_opcodes()
	populate_c_opcodes()
	populate_reporter_opcodes()
	populate_arg_opcodes()
	populate_opcode_dict()
	populate_one_arg()
	populate_two_arg()
	populate_three_arg()
	populate_exc_opcodes()

	#Global TeX splices for all tests
	#Uncomment line below once picture generator is ready
	preamble = open("preamble.txt").read() 
	prefix = open("prefix.txt").read()
	q1_text = open("q1text.txt").read()
	q1_prefix = open("q1_prefix.txt").read()
	q1_suffix = open("q1_suffix.txt").read()
	q2to6 = open("q2to6.txt").read()
	ans1line = open("ans1line.txt").read()
	ans2line = open("ans2line.txt").read()
	ans3line = open("ans3line.txt").read()
	q7tex = open("q7.txt").read()
	suffix = open("suffix.txt").read()

	#Create a global lists of projects
	projects = []

	#Create a csv of all Scratch usernames and project IDs
	studentInfo = open('students.csv','w+')

	#Take in Scratch Studio URL
	studioURL = sys.argv[1]

	#Convert studio URL to the one necessary for scraping Scratch usernames and project IDs
	studio_api_url = studio_to_API(studioURL)
	r = requests.get(studio_api_url, allow_redirects=True)
	studio_html = r.content
	studio_parser = BeautifulSoup(studio_html, "html.parser")


	for project in studio_parser.find_all('li'):
		#Find the span object with owner attribute
		span_string = str(project.find("span","owner"))
		
		#Pull out scratch username
		scratch_username = span_string.split(">")[2]
		scratch_username = scratch_username[0:len(scratch_username)-3]
		
		#Get project ID
		proj_id = project.get('data-id')

		#Read json file from URL. Convert Scratch URL to Scratch API URL, then read file.
		apiURL = "http://projects.scratch.mit.edu/internalapi/project/"+proj_id+"/get/"
		json_stream = requests.get(apiURL, allow_redirects=True)
		json_filename = scratch_username+".json"
		open(json_filename, 'wb').write(json_stream.content)
		json_data= open(json_filename, "r")
		data = json.load(json_data)
		json_data.close()

		#Print to students.csv
		studentInfoLine = scratch_username+","+"https://scratch.mit.edu/projects/"+proj_id+"/"
		print>>studentInfo, studentInfoLine


		#Create a project object for this project
		newProject = make_project(proj_id)
		newProject.username = scratch_username
		projects.append(newProject)

		#Process parent sprite (background, stage, etc)
		if 'objName' in data:
			parent = make_sprite(data["objName"])
			if 'scripts' in data:
				parent.scripts = data["scripts"]
				#pull out the actual instructions, which is the 3rd index in the script
				for i in range(len(parent.scripts)):
					parent.instructions.append(parent.scripts[i][2])


		if parent.instructions:
			newProject.scripts.append(parent.instructions)


		#Iterate over children if there are children
		if 'children' in data:
			for index, item in enumerate(data["children"]):
				if 'objName' in item:
					child = make_sprite(item["objName"])
					if 'scripts' in item: 
						child.scripts = item["scripts"]
						#pull out the actual instructions, which is the 3rd index in the script
						for itr in range(len(child.scripts)):
							child.instructions.append(child.scripts[itr][2])

					child.parent = parent
					parent.children.append(child)

			for child in parent.children:
				if child.instructions:
					newProject.scripts.append(child.instructions)
					

	#Create Unit 2 Baseline Questions for customizable question.
	baseline_qn = []

	#Question 3: Find 2 non-green flag and 1 green flag scripts from their code. Hard-code 1 sprite script
	question3 = make_question("Question 3")

	question3.scripts = [
						[["whenClicked"], ["say:", "My name is Kim!"], ["playSound:", "meow"], ["hide"]],
						[["whenClicked"], ["think:duration:elapsed:from:", "Hmm...", 2], ["nextCostume"]],
						[["whenKeyPressed", "space"], ["playDrum", 1, 0.25], ["rest:elapsed:from:", 0.25]],
						[["whenGreenFlag"], ["show"], ["forward:", 10], ["hide"]]
						]

	baseline_qn.append(question3)


	#Question 6: Find a Green Flag Script
	question6 = make_question("Question 6")

	question6.scripts = [[["whenGreenFlag"], ["doPlaySoundAndWait", "meow"], ["say:duration:elapsed:from:", "I'm hungry!", 2], ["forward:", 20]]]
	
	baseline_qn.append(question6)

	#Question 7: Find a sprite Clicked or Green Flag script
	question7 = make_question("Question 7")

	question7.scripts = [[["whenKeyPressed", "space"], ["say:duration:elapsed:from:", "Let's play!", 2], ["forward:", 10], ["nextCostume"]]]

	baseline_qn.append(question7)

	#List to keep track of which projects can be customed for each question. 
	#CSV files to keep track of which students got customized questions for each classroom, if they can be customized.

	q3_customProj = []
	q3_custom = open('q3_custom.csv','w+')
	q3_noCustom = open('q3_noCustom.csv','w+')

	q6_customProj = []
	q6_custom = open('q6_custom.csv','w+')
	q6_noCustom = open('q6_noCustom.csv','w+')

	q7_customProj = []
	q7_custom = open('q7_custom.csv','w+')
	q7_noCustom = open('q7_noCustom.csv','w+')

	#Customize the questions for each project here.
	for project in projects:
		qn3_copy = copy.deepcopy(question3)
		qn6_copy = copy.deepcopy(question6)
		qn7_copy = copy.deepcopy(question7)

		#Question 3
		custom_q3(qn3_copy,project)
		#Check if we can custom q3.
		if qn3_copy.scripts != question3.scripts:
			q3_customProj.append(project)
			#Comment out to keep track of students who got a custom question if all students get custom
			#print>>q3_custom, project.username+','+project.ID

		project.questions.append(qn3_copy)

		custom_q6(qn6_copy,project)
		#Check if we can custom q6.
		if qn6_copy.scripts != question6.scripts:
			q6_customProj.append(project)
			#Comment out to keep track of students who got a custom question if all students get custom
			#print>>q6_custom, project.username+','+project.ID
		project.questions.append(qn6_copy)

		custom_q7(qn7_copy,project)
		#Check if we can custom q7.
		if qn7_copy.scripts != question7.scripts:
			q7_customProj.append(project)
			#Comment out to keep track of students who got a custom question if all students get custom
			#print>>q7_custom, project.username+','+project.ID
		project.questions.append(qn7_copy)

	#Shuffle the list of customized questions & decide which projects get a custom question
	#Comment out lines below if we want all students to get a custom question
	decideCustom(q3_customProj, 0, question3, q3_custom, q3_noCustom)
	decideCustom(q6_customProj, 1, question6, q6_custom, q6_noCustom)
	decideCustom(q7_customProj, 2, question7, q7_custom, q7_noCustom)
	
	#Convert questions into Scratchblocks format
	for project in projects:
		#Create a file of customized questions to compare json string to Scratchblocks string
		txt_name = project.username+"_jsonString.txt"
		txtFile = open(txt_name,'w+')
		for question in project.questions:
			print>>txtFile, question.ID
			print>>txtFile, '\n'
			for y in range(0,len(question.scripts)):
				print>>txtFile, "Script "+str(y)
				print>>txtFile,question.scripts[y]
			print>>txtFile, '\n'


		#Open a file that contains all the customized scripts
		customTestName = project.username+"_custom.txt"
		customTest = open(customTestName,'w+')

		#Convert lists to strings to make it easier to convert to Scratchblocks format
		for question in project.questions:

			#Shuffle scripts for q3
			if question.ID == 'Question 3':
				random.shuffle(question.scripts)
			
			temp_list = [] #List of preprocessed strings before becoming Scratchblocks format
			if len(question.scripts) > 0:
				for script in question.scripts:
					temp_list.append(str(script))

			#Iterate over json-formatted strings in temp_list and convert in to Scratchblocks format
			for i in range(0, len(temp_list)):
				# print("Script "+str(i))
				block = temp_list[i]
				#Split on comma so that items in the json list are separated
				splitList = block.split(',')
				
				#List of elements to assemble Scratchblocks strings.
				cleanStrings = []
				for j in range(0, len(splitList)):
					split = splitList[j].strip()
					cleanString = ''
					for char in split:
						if char != '[' and char != ']':
							cleanString = cleanString+char
					if len(cleanString)>0:
						#If the first character is u, remove it.
						if cleanString[0] =='u':
							cleanString = cleanString[1:len(cleanString)]

					if len(cleanString)>0:
						#Remove the apostrophes from first and last characters
						if cleanString[0] == '\'' and cleanString[len(cleanString)-1] == '\'':
							cleanString = cleanString[1:len(cleanString)-1]

					if len(cleanString)>0:
						#Remove "" from first and last characters
						if cleanString[0] == '"' and cleanString[len(cleanString)-1] == '"':
							cleanString = cleanString[1:len(cleanString)-1]

					# splitList[j]=cleanString
					cleanStrings.append(cleanString)

				#Put together string arguments that got spliced by the comma
				i1 = 0
				newList = []
				while i1 < len(cleanStrings):
					cleanString = cleanStrings[i1]
					#Check if it's a string argument that got spliced on comma, not an opcode or a numerical argument
					if cleanString not in opcode_dict and is_number(cleanString)==False: #If it is a string arg
						#Check the neighbors
						i2 = i1+1
						# print("Index of neighbor: "+ str(i2))
						if i2 < len(cleanStrings): #Start checking neighbors only if they are in range
							while i2 < len(cleanStrings) and is_number(cleanStrings[i2])==False and cleanStrings[i2] not in opcode_dict: #While it's neighbors are string arg
								cleanString = cleanString+ ','+cleanStrings[i2]
								i2 = i2+1

							newList.append(cleanString)
							i1=i2
						
						else: #It's a solo string
							newList.append(cleanString)
							i1=i1+1

					else:
						newList.append(cleanString)
						i1=i1+1

				

				#Assemble Scratchblocks string here from the elements in newList
				k=0
				scrBlk = ''
				numEvents = 0;
				event_opcodes = ['whenGreenFlag', 'whenClicked','whenIReceive','whenKeyPressed', 'whenSceneStarts','whenSensorGreaterThan']
				file_arg_opcodes = ["playSound:", "doPlaySoundAndWait","lookLike:","startScene","startSceneAndWait","whenSceneStarts"]

				while k < len(newList):
					blkPiece = newList[k]
					#Check if it's an event block. We can only have one per script
					if blkPiece in event_opcodes:
						numEvents = numEvents+1

					if numEvents > 1:
						k = k+1

					else:
						#Blocks that take one argument
						if blkPiece in one_arg_opcodes:
							plainText = opcode_dict.get(blkPiece)
							textPieces = plainText.split('(')
							inc = 2 #Default amt to increment k. May chenge if there are missing arguments

							#Look at its argument (element right after it in the list)
							#Check if it exists & is not an opcode
							if k+1 < len(newList) and newList[k+1] not in opcode_dict:
								arg1 = newList[k+1]
							
							#Make it a space
							else:
								arg1 = " "
								inc = 1
							
							#Check if it takes in a file as an argument and arg is just a raw file name
							if blkPiece in file_arg_opcodes and len(arg1) > 20:
								arg1 = 'myFile'

							if is_number(arg1):
								scrBlk = scrBlk+textPieces[0]+'('+arg1+textPieces[1]+'\n'
							else:
								#Replace the first character of the later half the string from ) to ]
								bracketString = ']'+textPieces[1][1:len(textPieces[1])]
								scrBlk = scrBlk+textPieces[0]+'['+arg1+bracketString+'\n'
							k=k+inc

						
						#Blocks that take 2 arguments
						if blkPiece in two_arg_opcodes:
							plainText = opcode_dict.get(blkPiece)
							textPieces = plainText.split('(')
							inc = 3 #Default amt to increment k. May chenge if there are missing arguments

							#Look at its 2 arguments (2 elements right after it in the list)
							#Check if the first arg exists and isn't opcode
							if k+1 < len(newList) and newList[k+1] not in opcode_dict:
								arg1 = newList[k+1]
							
							#Make it a space
							else:
								arg1 = " "
								inc = 1
							
							#Check if it has a second arg and isn't opcode
							if k+2 < len(newList) and newList[k+2] not in opcode_dict:
								arg2 = newList[k+2]
							
							#Make it a space
							else:
								arg2 = " "
								inc = 2
							
							if is_number(arg1):
								scrBlk = scrBlk+textPieces[0]+'('+arg1+textPieces[1]
							else:
								#Replace the first character of the middle string from ) to ]
								bracketString = ']'+textPieces[1][1:len(textPieces[1])]
								scrBlk = scrBlk+textPieces[0]+'['+arg1+bracketString
							if is_number(arg2):
								scrBlk = scrBlk+'('+arg2+textPieces[2]+'\n'
							else:
								bracketString = ']'+textPieces[2][1:len(textPieces[2])]
								scrBlk = scrBlk+'['+arg2+bracketString+'\n'
							k=k+inc

						#Blocks that take 3 arguments
						if blkPiece in three_arg_opcodes:
							plainText = opcode_dict.get(blkPiece)
							textPieces = plainText.split('(')
							#Look at its 3 arguments (3 elements right after it in the list)
							inc = 4 #Default amt to increment k. May chenge if there are missing arguments

							#Check if the first arg exists and isn't opcode
							if k+1 < len(newList) and newList[k+1] not in opcode_dict:
								arg1 = newList[k+1]
							
							#Make it a space
							else:
								arg1 = " "
								inc = 1
							
							#Check if it has a second arg and isn't opcode
							if k+2 < len(newList) and newList[k+2] not in opcode_dict:
								arg2 = newList[k+2]
							
							#Make it a space
							else:
								arg2 = " "
								inc = 2

							#Check if it has a second arg and isn't opcode
							if k+3 < len(newList) and newList[k+3] not in opcode_dict:
								arg3 = newList[k+3]
							
							#Make it a space
							else:
								arg3 = " "
								inc = 3
							
							if is_number(arg1):
								scrBlk = scrBlk+textPieces[0]+'('+arg1+textPieces[1]
							else:
								#Replace the first character of the middle string from ) to ]
								bracketString = ']'+textPieces[1][1:len(textPieces[1])]
								scrBlk = scrBlk+textPieces[0]+'['+arg1+bracketString
							if is_number(arg2):
								scrBlk = scrBlk+'('+arg2+textPieces[2]
							else:
								bracketString = ']'+textPieces[2][1:len(textPieces[2])]
								scrBlk = scrBlk+'['+arg2+bracketString
							if is_number(arg3):
								scrBlk = scrBlk+'('+arg3+textPieces[3]+'\n'
							else:
								bracketString = ']'+textPieces[3][1:len(textPieces[3])]
								scrBlk = scrBlk+'['+arg2+bracketString+'\n'
							k=k+inc

						#Blocks that don't take arguments
						if blkPiece not in one_arg_opcodes and blkPiece not in two_arg_opcodes and blkPiece not in three_arg_opcodes:
							if opcode_dict.get(blkPiece) is not None:
								scrBlk = scrBlk + opcode_dict.get(blkPiece)+'\n'
							k = k+1

				#Replace string when it's formatted in ScratchBlocks
				question.scrBlks.append(scrBlk)


				#Print blocks in Scratchblocks format
			for x in range(0, len(question.scrBlks)):
				print>>customTest, "Script"
				print>>customTest, question.scrBlks[x]

			#Count the number of blocks in Q7
			if question.ID == 'Question 7':
				project.lenQ7 = question.scrBlks[0].count('\n')

		#Shuffle question 1 images and assemble tex string
		q1_images = ["q1_script0","q1_script1","q1_script2","q1_script3"]
		random.shuffle(q1_images)
		q1=q1_text
		for image in q1_images:
			q1 = q1+q1_prefix+image+q1_suffix

		#Decide how many answer lines Q7 needs
		q7ans = ans1line #Default: Give them plain lines

		if project.lenQ7 == 3: #if there are 3 blocks inc hat block
			q7ans = ans2line

		if project.lenQ7 == 4: #if there are 4 blocks inc hat block
			q7ans = ans3line

		
		#Generate custom LaTeX test for each project.
		texFileName = project.username+'_test.tex'
		texFile = open(texFileName,'w+')
		# texString = prefix+project.username+"\n"+q1+q2to6+ans3line+"\n"+q7tex+q7ans+suffix
		#Comment out line above once pic generator is ready
		#Ensure username doesn't have any underscores for latex
		tex_username = project.username.replace("_","\\textunderscore ")
		texString = preamble+project.username+prefix+tex_username+"\n"+q1+q2to6+ans3line+"\n"+q7tex+q7ans+suffix
		print>>texFile, texString


					

if __name__ == '__main__':
	main()