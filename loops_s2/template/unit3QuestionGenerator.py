#Jean Salac
#Unit 3 Question Generator. Run with the following command: python unit3QuestionGenerator.py scratchStudioURL

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
	lenQ6 = 4 #Length of script in q6; default is 4 (repeat + 3 blocks)
	lenQ7 = 0 #Length of script in q7; default is 0.

	def __init__(self, ID):
		self.ID = ID
		self.scripts = []
		self.questions = []
		self.username = ''
		self.lenQ6 = 4
		self.lenQ7 = 0

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
	scripts = [] #Scripts/answers that are part of the question
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

#Method to check if a string is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
 

#Methods to customize questions. Takes in the baseline question and project

#Question 1: Find a repeat block
def custom_q1(Question, Project):
	opcode_index = find_index(Project.scripts, 'doRepeat')
	#print(Project.username)
	if len(opcode_index)>0: #If a script is found
		#print(opcode_index)

		#Return the whole script with the loop
		found_script = Project.scripts[opcode_index[0]]
		for i in range(1,len(opcode_index)-1):
			found_script = found_script[opcode_index[i]]

		#If the loop is not empty
		if found_script[2] is not None:
			#Check if 1-5 blocks in the loop
			if len(found_script[2])>0 and len(found_script[2])<6:
				Question.scripts[0] = found_script


#Question 6: Find a loop from their code. 2-3 blocks in the loop
def custom_q6(Question,Project):
	#If both don't work find, a repeat loop
	doRepeat_index = find_index(Project.scripts, 'doRepeat')
	if len(doRepeat_index)>0: #If a script is found
		
		#Return the whole script with the loop
		doRepeat = Project.scripts[doRepeat_index[0]]
		for i in range(1,len(doRepeat_index)-1):
			doRepeat = doRepeat[doRepeat_index[i]]
		
		#Check for excluded blocks
		hasExc = False
		for opcode in exc_opcodes:
			exc_index = find_index(doRepeat,opcode)
			if len(exc_index) > 0:
				hasExc = True
				break

		#If the loop is not empty
		if doRepeat[2] is not None:
			#Check if 2-3 blocks in the loop
			if len(doRepeat[2])>1 and len(doRepeat[2])<4 and hasExc is False:
				Question.scripts[0] = doRepeat

#Question 7: Find a loop from their code. 1-5 blocks in the loop
def custom_q7(Question,Project):
	#If both don't work find, a repeat loop
	doRepeat_index = find_index(Project.scripts, 'doRepeat')
	if len(doRepeat_index)>0: #If a script is found
		
		#Return the whole script with the loop
		doRepeat = Project.scripts[doRepeat_index[0]]
		for i in range(1,len(doRepeat_index)-1):
			doRepeat = doRepeat[doRepeat_index[i]]
		
		#Check for excluded blocks
		hasExc = False
		for opcode in exc_opcodes:
			exc_index = find_index(doRepeat,opcode)
			if len(exc_index) > 0:
				hasExc = True
				break

		#If the loop is not empty
		if doRepeat[2] is not None:
			#Check if 1-5 blocks in the loop
			if len(doRepeat[2])>0 and len(doRepeat[2])<6 and hasExc is False:
				Question.scripts.append(doRepeat)


#Method to decide if a project is going to get a custom question. 
#Shuffles the list of projects. The first half gets nonCustom question
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
	opcode_dict = {'changeXposBy:': 'Change X by ()', 'show': 'Show', 
	'whenIReceive': 'When I Receive ()', '/': '() / ()', 
	'getParam': 'custom block parameter', 'rounded': 'Round ()', 
	'doForLoop': 'For Each () in ()', 'lookLike:': 'Switch Costume to ()', 
	'sayNothing': 'Say Nothing', 'timeAndDate': 'Current ()', 
	'color:sees:': 'Color () is Touching ()?', 'changeSizeBy:': 'Change Size by ()', 
	'setSizeTo:': 'Set Size to ()%', 'fxTest': 'Color FX Test ()', 
	'turnRight:': 'Turn Right () Degrees', 'mousePressed': 'Mouse Down?', 
	'concatenate:with:': 'Join ()()', 'doPlaySoundAndWait': 'Play Sound () Until Done',
	'lineCountOfList:': 'Length of ()', 'timestamp': 'Days Since 2000', 
	'setVideoTransparency': 'Set Video Transparency to ()%', 
	'setLine:ofList:to:': 'Replace Item () of () With ()', 'warpSpeed': 'All at Once', 
	'getUserId': 'User ID', 'computeFunction:of:': '() of ()', 'nextCostume': 'Next Costume', 
	'not': 'Not ()', 'changeYposBy:': 'Change Y by ()', 'gotoX:y:': 'Go to X: () Y: ()', 
	'whenClicked': 'When This Sprite Clicked', 'setVideoState': 'Turn Video ()', 
	'costumeIndex': 'Costume #', 'wait:elapsed:from:': 'Wait () Secs', 
	'setPenHueTo:': 'Set Pen Color to ()', 'scrollRight': 'Scroll Right ()', 
	'setRotationStyle': 'Set Rotation Style ()', 'whenGreenFlag': 'When Green Flag Clicked', 
	'stopAllSounds': 'Stop All Sounds', 'goBackByLayers:': 'Go Back () Layers', 'heading': 'Direction', 
	'setPenShadeTo:': 'Set Pen Shade to ()', 'penSize:': 'Set Pen Size to ()', 
	'playSound:': 'Play Sound ()', 'playDrum': 'Play Drum () for () Beats', 
	'setTempoTo:': 'Set Tempo to () bpm', 'obsolete': 'Obsolete', 
	'rest:elapsed:from:': 'Rest for () Beats', 'xpos:': 'Set X to ()', 'doWhile': 'While ()', 
	'sensor:': '() Sensor Value', 'changePenSizeBy:': 'Change Pen Size by ()', 
	'doWaitUntil': 'Wait Until ()', 'randomFrom:to:': 'Pick Random () to ()', 
	'letter:of:': 'Letter () of ()', 'getLine:ofList:': 'Item () of ()', 'stopAll': 'Stop All', 
	'scale': 'Size', 'hide': 'Hide', 'hideAll': 'Hide All Sprites', 
	'doBroadcastAndWait': 'Broadcast () and Wait', '+': '() + ()', 'stopSound:': 'Stop Sound ()', 
	'contentsOfList:': '()', 'changeVar:by:': 'Change () by ()', 'sensorPressed:': 'Sensor ()?', 
	'abs': 'Abs ()', 'changeGraphicEffect:by:': 'Change () Effect by ()', 
	'changePenHueBy:': 'Change Pen Color by ()', 'COUNT': 'Counter', 'tempo': 'Tempo', 
	'hideList:': 'Hide List ()', 'costumeName': 'Costume Name', 'say:': 'Say ()', 
	'ypos': 'Y Position', 'think:': 'Think ()', 'distanceTo:': 'Distance to ()', 
	'whenKeyPressed': 'When () Key Pressed', 'filterReset': 'Clear Graphic Effects', 
	'doUntil': 'Repeat Until ()', 'soundLevel': 'Loudness', 'penColor:': 'Set Pen Color to ()', 
	'broadcast:': 'Broadcast ()', 'startScene': 'Switch Backdrop to ()', 'deleteClone': 'Delete This Clone', 
	'senseVideoMotion': 'Video () on ()', 'timer': 'Timer', '|': '() or ()', 
	'whenSceneStarts': 'When Backdrop Switches to ()', 'bounceOffEdge': 'If on Edge, Bounce', 
	'setGraphicEffect:to:': 'Set () Effect to ()', 'CLR_COUNT': 'Clear Counter', 
	'list:contains:': '() Contains ()', 'doForeverIf': 'Forever If ()', 'stringLength:': 'Length of ()', 
	'hideVariable:': 'Hide Variable ()', 'readVariable': '() (Variables block)', 
	'midiInstrument:': 'Set Instrument to ()', 'doAsk': 'Ask () and Wait', 'doIf': 'If () Then', 
	'backgroundIndex': 'Backdrop #', 'deleteLine:ofList:': 'Delete () of ()', 
	'changeVolumeBy:': 'Change Volume by ()', '&': '() and ()', 'getAttribute:of:': '() of ()', 
	'*': '() * ()', 'startSceneAndWait': 'Switch Backdrop to () and Wait', 
	'changePenShadeBy:': 'Change Pen Shade by ()', 'doRepeat': 'Repeat ()', '>': '() > ()', 
	'instrument:': 'Set Instrument to ()', 'xpos': 'X Position', 
	'think:duration:elapsed:from:': 'Think () for () Secs', 'nextScene': 'Next Backdrop', 
	'forward:': 'Move () Steps', 'volume': 'Volume', 'mouseY': 'Mouse Y', 'mouseX': 'Mouse X', 
	'showList:': 'Show List ()', 'whenSensorGreaterThan': 'When () is greater than ()', 
	'gotoSpriteOrMouse:': 'Go to ()', 'insert:at:ofList:': 'Insert () at () of ()', 
	'sceneName': 'Backdrop Name', 'doForever': 'Forever', '<': '() < ()', 
	'glideSecs:toX:y:elapsed:from:': 'Glide () Secs to X: () Y: ()', 'stopScripts': 'Stop ()', 
	'turnAwayFromEdge': 'Point Away From Edge', 'noteOn:duration:elapsed:from:': 'Play Note () for () Beats', 
	'ypos:': 'Set Y to ()', 'clearPenTrails': 'Clear', 'drum:duration:elapsed:from:': 'Play Drum () for () Beats', 
	'touchingColor:': 'Touching Color ()?', 'xScroll': 'X Scroll', 'doIfElse': 'If () Then, Else', 
	'keyPressed:': 'Key () Pressed?', 'pointTowards:': 'Point Towards ()', 'putPenDown': 'Pen Down', 
	'setVar:to:': 'Set () to ()', '%': '() Mod ()', '-': '() - ()', 'sqrt': 'Sqrt ()', 
	'showVariable:': 'Show Variable ()', 'answer': 'Answer', 'putPenUp': 'Pen Up', '=': '() = ()', 
	'isLoud': 'Loud?', 'append:toList:': 'Add () to ()', 'whenCloned': 'When I Start as a Clone', 
	'timerReset': 'Reset Timer', 'comeToFront': 'Go to Front', 'INCR_COUNT': 'Incr Counter', 
	'setVolumeTo:': 'Set Volume to ()%', 'scrollUp': 'Scroll Up ()', 'turnLeft:': 'Turn Left () Degrees', 
	'doReturn': 'Stop Script', 'heading:': 'Point in Direction ()', 'stampCostume': 'Stamp', 
	'getUserName': 'Username', 'yScroll': 'Y Scroll', 'touching:': 'Touching ()?', 'undefined': 'Undefined', 
	'changeTempoBy:': 'Change Tempo by ()', 'scrollAlign': 'Align Scene ()', 'createCloneOf': 'Create Clone of ()', 
	'say:duration:elapsed:from:': 'Say () for () Secs'}

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

#Opcodes for blocks beyond the scope of this unit and are excluded from custom blocks
#No conditionals, variables, play sound 
exc_opcodes= []
def populate_exc_opcodes():
	global exc_opcodes
	exc_opcodes = ["doForever","doIf","doIfElse","doUntil","playSound:","readVariable","showVariable:","hideVariable:"]



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
	prefix = open("prefix.txt").read()
	q1to5 = open("q1-5.txt").read()
	ans1line = open("ans1line.txt").read()
	ans2line = open("ans2line.txt").read()
	ans3line = open("ans3line.txt").read()
	q6text = open("q6text.txt").read()
	qn7custom = open("qn7custom.txt").read()
	qn7generic = open("qn7generic.txt").read()
	extrachallenge = open("extrachallenge.txt").read()

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
					

	#Create Unit 3 Baseline Questions
	baseline_qn = []

	#Question 1: Find a repeat block in their code and replace how many times it repeats.
	question1 = make_question("Question 1")

	question1.scripts = [["doRepeat", 9, [["forward:", 10], ['wait:elapsed:from:',5], ["playSound:", "woof"]]]]

	baseline_qn.append(question1)

	#Question 6: Find a loop from their code with 2-3 blocks
	question6 = make_question("Question 6")

	question6.scripts = [["doRepeat", 8, [["nextCostume"], ["forward:", 15], ['doPlaySoundAndWait', "moo"]]]]
	
	baseline_qn.append(question6)

	#Question 7: Find a loop with 1-5 blocks
	question7 = make_question("Question 7")
	
	baseline_qn.append(question7)


	#List to keep track of which projects can be customed for each question. 
	#CSV files to keep track of which students got customized questions for each classroom, if they can be customized.
	q1_customProj = []
	q1_custom = open('q1_custom.csv','w+')
	q1_noCustom = open('q1_noCustom.csv','w+')

	q6_customProj = []
	q6_custom = open('q6_custom.csv','w+')
	q6_noCustom = open('q6_noCustom.csv','w+')

	q7_customProj = []
	q7_custom = open('q7_custom.csv','w+')
	q7_noCustom = open('q7_noCustom.csv','w+')

	#Customize the questions for each project here.
	for project in projects:

		#Deep copy of each baseline question
		qn1_copy = copy.deepcopy(question1)
		qn6_copy = copy.deepcopy(question6)
		qn7_copy = copy.deepcopy(question7)

		#Question 1
		custom_q1(qn1_copy, project)
		#Check if we can custom q1. Add project to the list of customizable projects for question 1
		if qn1_copy.scripts != question1.scripts:
			q1_customProj.append(project)
		project.questions.append(qn1_copy)

		custom_q6(qn6_copy,project)
		#Check if we can custom q6.
		if qn6_copy.scripts != question6.scripts:
			q6_customProj.append(project)
		project.questions.append(qn6_copy)
		
		custom_q7(qn7_copy,project)
		#Check if we can custom q7.
		if qn7_copy.scripts != question7.scripts:
			q7_customProj.append(project)
		project.questions.append(qn7_copy)


	#Shuffle the list of customized questions & decide which projects get a custom question
	decideCustom(q1_customProj, 0, question1, q1_custom, q1_noCustom)
	decideCustom(q6_customProj, 1, question6, q6_custom, q6_noCustom)
	decideCustom(q7_customProj, 2, question7, q7_custom, q7_noCustom)
	
	#Convert questions into Scratchblocks format. Only run this for customizable questions
	customQns = ["Question 1","Question 6", "Question 7"]
	
	for project in projects:
		#Create a file of customized questions to compare json string to Scratchblocks string
		txt_name = project.username+"_jsonString.txt"
		txtFile = open(txt_name,'w+')
		for question in project.questions:
			if question.ID in customQns:
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
			if question.ID in customQns:
				
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

							#Remove the apostrophes from first and last characters
							if cleanString[0] == '\'' and cleanString[len(cleanString)-1] == '\'':
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

			#Count the number of blocks in Q6 or Q7
			if question.ID == 'Question 6':
				project.lenQ6 = question.scrBlks[0].count('\n')

			if question.ID == 'Question 7' and len(question.scripts)!=0:
				project.lenQ7 = question.scrBlks[0].count('\n')

		#Decide how many answer lines Q6 needs
		q6ans = ans1line #Default: Give them plain lines

		if project.lenQ6 == 3: #if there are 3 blocks inc repeat block
			q6ans = ans2line

		if project.lenQ6 == 4: #if there are 4 blocks inc repeat block
			q6ans = ans3line

		#Decide if Q7 is custom or generic
		qn7 = qn7generic

		if project.lenQ7 != 0:
			qn7 = qn7custom

		#Generate custom LaTeX test for each project.
		texFileName = project.username+'_test.tex'
		texFile = open(texFileName,'w+')
		texString = prefix + " "+ project.username + "\n"+ q1to5+q6ans+q6text+qn7+extrachallenge
		print>>texFile, texString


					

if __name__ == '__main__':
	main()