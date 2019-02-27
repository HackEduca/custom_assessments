#Jean Salac
#Sequence Question Generator for Scratch 3. Run with the following command: python sequenceQnGen.py scratchStudioURL

import sys
import json
import requests
from pprint import pprint
import copy
import re
import random
import time
from bs4 import BeautifulSoup
import scratchAPI as sa
import navJson as nj

#Scratch Project Class.
class Project(object):
	ID = ''
	blocks = ''
	questions = ''
	username = '' #Scratch username
	#List of the block IDs of events of interest
	greenFlags=''
	spriteClickeds=''
	keyPresseds=''
	#List of the scripts of events of interest
	gfScripts=''
	scScripts=''
	kpScripts=''
	lenQ7 = 4 #Num blocks in q7 script. Default is 4

	def __init__(self, ID):
		self.ID = ID
		self.blocks = {}
		self.questions = []
		self.username = ''
		self.greenFlags=[]
		self.spriteClickeds=[]
		self.keyPresseds=[]
		self.gfScripts=[]
		self.scScripts=[]
		self.kpScripts=[]
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

	def __init__(self, ID):
		self.ID = ID
		self.scripts = []

	def __str__(self):
		return "Question ID: "+ self.ID
	def __repr__(self):
		return "Question ID: "+ self.ID

#Question Constructor
def make_question(name):
	question = Question(name)
	return question

#Custom question functions. TODO: Add excluded opcodes
#Question 3: Find 1 green flag script, 1 spriteClicked, or 1 keyPressed from their code. Hard-code 1 spriteClicked script.
#Check if 2-4 blocks long, including the hat block, and no excluded blocks.
#Takes in project and creates a custom question for project
def customize_q3(project):
	q3=make_question('Question 3')
	q3.scripts = [
	#Sprite clicked generic script
	{"2bY`2_e=7csW+EwXTmt*":{"opcode":"event_whenthisspriteclicked","next":"1NO^;2u%X1UuOUWv=g@3","parent":None,"inputs":{},"fields":{},"shadow":False,"topLevel":True,"x":31,"y":70},
	"1NO^;2u%X1UuOUWv=g@3":{"opcode":"looks_thinkforsecs","next":"({Hy9IC?|G1zX7Vg}PD~","parent":"2bY`2_e=7csW+EwXTmt*","inputs":{"MESSAGE":[1,[10,"Hmm..."]],"SECS":[1,[4,"2"]]},"fields":{},"shadow":False,"topLevel":False},
	"({Hy9IC?|G1zX7Vg}PD~":{"opcode":"looks_nextcostume","next":None,"parent":"1NO^;2u%X1UuOUWv=g@3","inputs":{},"fields":{},"shadow":False,"topLevel":False}},
	
	#Key pressed generic script
	{"|t8aA]$@rWg|sqH9aF*|":{"opcode":"event_whenkeypressed","next":"3_~E+N!i*F7k=nnDArGG","parent":None,"inputs":{},"fields":{"KEY_OPTION":["space",None]},"shadow":False,"topLevel":True,"x":35,"y":288},
	"3_~E+N!i*F7k=nnDArGG":{"opcode":"sound_playuntildone","next":None,"parent":"|t8aA]$@rWg|sqH9aF*|","inputs":{"SOUND_MENU":[1,"3j^lzgy/7HneNCgKcxB4"]},"fields":{},"shadow":False,"topLevel":False},
	"3j^lzgy/7HneNCgKcxB4":{"opcode":"sound_sounds_menu","next":None,"parent":"3_~E+N!i*F7k=nnDArGG","inputs":{},"fields":{"SOUND_MENU":["Drum",None]},"shadow":True,"topLevel":False}},

	#First GF generic script
	{"Jclia0i/TNh|5,RYxc(Q":{"opcode":"event_whenflagclicked","next":"%h@_UWp3nK]|v,HUnze^","parent":None,"inputs":{},"fields":{},"shadow":False,"topLevel":True,"x":31,"y":446},
	"%h@_UWp3nK]|v,HUnze^":{"opcode":"looks_show","next":"=Jt{3ymiml+o?L*E2eZp","parent":"Jclia0i/TNh|5,RYxc(Q","inputs":{},"fields":{},"shadow":False,"topLevel":False},
	"=Jt{3ymiml+o?L*E2eZp":{"opcode":"motion_movesteps","next":"){8C;vZSkS;[y$cf*2g$","parent":"%h@_UWp3nK]|v,HUnze^","inputs":{"STEPS":[1,[4,"10"]]},"fields":{},"shadow":False,"topLevel":False},
	"){8C;vZSkS;[y$cf*2g$":{"opcode":"looks_hide","next":None,"parent":"=Jt{3ymiml+o?L*E2eZp","inputs":{},"fields":{},"shadow":False,"topLevel":False}},

	#Hardcoded Sprite Clicked generic script
	{"GUWjki5uit`:iE@Ma$:i":{"opcode":"event_whenthisspriteclicked","next":"ylXf!!CJ;i=H$?)r7Z^3","parent":None,"inputs":{},"fields":{},"shadow":False,"topLevel":True,"x":24,"y":687},
	"ylXf!!CJ;i=H$?)r7Z^3":{"opcode":"looks_say","next":"yqe=V4B67J.]I$?l~?y#","parent":"GUWjki5uit`:iE@Ma$:i","inputs":{"MESSAGE":[1,[10,"My name is Kim!"]]},"fields":{},"shadow":False,"topLevel":False},
	"yqe=V4B67J.]I$?l~?y#":{"opcode":"sound_playuntildone","next":"xW;Q8e$g_IfY4L`!K=mz","parent":"ylXf!!CJ;i=H$?)r7Z^3","inputs":{"SOUND_MENU":[1,"83vG.7=/MQeKg8lNN3HE"]},"fields":{},"shadow":False,"topLevel":False},
	"83vG.7=/MQeKg8lNN3HE":{"opcode":"sound_sounds_menu","next":None,"parent":"yqe=V4B67J.]I$?l~?y#","inputs":{},"fields":{"SOUND_MENU":["Meow",None]},"shadow":True,"topLevel":False},
	"xW;Q8e$g_IfY4L`!K=mz":{"opcode":"looks_hide","next":None,"parent":"yqe=V4B67J.]I$?l~?y#","inputs":{},"fields":{},"shadow":False,"topLevel":False}}
	]

	#If they have sprite clicked scripts
	if len(project.scScripts)>0:
		for script in project.scScripts:
			if len(script)>=2 and len(script)<=4:
				#Replace generic sprite clicked script
				q3.scripts[0]=script
				break
		
	#If they have key pressed scripts
	if len(project.kpScripts)>0: 
		for script in project.kpScripts:
			#Replace generic key pressed script 
			if len(script)>=2 and len(script)<=4:
				q3.scripts[1]=script
				break

	#If they have green flag scripts
	if len(project.gfScripts)>0: 
		for script in project.gfScripts:
			#Replace first generic GF script 
			if len(script)>=2 and len(script)<=4:
				q3.scripts[2]=script
				break

	project.questions.append(q3)



#Question 6: Find a "When Green Flag". No loops, conditionals, variables, play sound.
#Check if 4 blocks long, including the GF block, and no excluded blocks.
#Takes in project and creates a custom question for project
def customize_q6(project):
	q6 = make_question('Question 6')
	for script in project.gfScripts:
		#If GF script is exactly 4 blocks long
		if len(script)==4:
			q6.scripts.append(script)
			break
	project.questions.append(q6)

	

#Question 7: Find a spriteClicked or GreenFlag. No loops, conditionals, variables, play sound.
#Check if 2-4 blocks long, including the GF block, and no excluded blocks.
#Takes in project and creates a custom question for project
def customize_q7(project):
	q7 = make_question('Question 7')
	#If they have sprite clicked scripts
	if len(project.scScripts)>0:
		for script in project.scScripts:
			if len(script)>=2 and len(script)<=4:
				q7.scripts.append(script)
				break
	else: #use a green flag script
		for script in project.gfScripts:
			if len(script)>=2 and len(script)<=4:
				q7.scripts.append(script)
				break
	project.questions.append(q7)



#Function to decide which projects get custom code.
#Args: Set of all candidate projects, sets & csv files for custom projects & non custom projects,
def decide_custom(candidates, custom, noCustom,csvCustom,csvNoCustom):
	candidates = list(candidates)
	if len(candidates) > 0:
		#If list is even, shuffle and split in half.
		if len(candidates)%2==0:
			random.shuffle(candidates)
			for x in range(0, len(candidates)):
				if x < len(candidates)/2: #First half gets noncustom question
					noCustom.add(candidates[x])
					print>>csvNoCustom, candidates[x].username+','+candidates[x].ID
				else:
					custom.add(candidates[x])
					print>>csvCustom, candidates[x].username+','+candidates[x].ID
		else:
			random.shuffle(candidates)
			for x in range(0, len(candidates)-1):
				if x < len(candidates)/2: #First half gets noncustom question
					noCustom.add(candidates[x])
					print>>csvNoCustom, candidates[x].username+','+candidates[x].ID
				else:
					custom.add(candidates[x])
					print>>csvCustom, candidates[x].username+','+candidates[x].ID
			
			#Last odd element custom/generic is based on timestamp
			ts = str(time.time())
			rand_digit = int(ts[random.randint(1,len(ts)-4)])
			last = len(candidates)-1
			if rand_digit%2==0: #If even, get a generic question
				noCustom.add(candidates[last])
				print>>csvNoCustom, candidates[last].username+','+candidates[last].ID
			else:
				custom.add(candidates[last])
				print>>csvCustom, candidates[last].username+','+candidates[last].ID

#Function to check for excluded opcodes
def has_exc(script):
	exc_opcodes=['control_repeat','control_repeat_until','control_forever','control_if ',
	'control_if_else','data_hidevariable','data_showvariable','data_changevariableby','sound_play']
	for block in script:
		blockInfo=script[block]
		blockOpcode=blockInfo['opcode']
		if blockOpcode in exc_opcodes:
			return True
	return False


def main():

	#Create a global lists of projects
	projects = []
	#Create a csv of all Scratch usernames and project IDs
	studentInfo = open('students.csv','w+')

	#Take in Scratch Studio URL
	studioURL = sys.argv[1]

	#Convert studio URL to the one necessary for scraping Scratch usernames and project IDs.
	#Pull projects until page number does not exist

	#Initialize studio URL and requests
	pageNum = 1
	studio_api_url = sa.studio_to_API(studioURL,pageNum)
	r = requests.get(studio_api_url, allow_redirects=True)

	#While the studio API URL exists, pull all the projects
	while(r.status_code == 200):
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
			apiURL = sa.create_API_URL(proj_id)
			json_stream = requests.get(apiURL, allow_redirects=True)
			user_directory = "user_json_files/"
			json_filename = user_directory + scratch_username+".json"
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

			#Add project blocks 
			newProject.blocks = nj.get_blocks(data)

			#Add project to the global list of projects
			projects.append(newProject)

		pageNum+=1
		studio_api_url = sa.studio_to_API(studioURL,pageNum)
		r = requests.get(studio_api_url, allow_redirects=True)

	#Set of projects with candidate code for each question
	q3_cands = set() #Check if 2-4 blocks long, including the hat block, and no excluded blocks. 1 green flag script, 1 spriteClicked, or 1 keyPressed
	q6_cands = set() #Check if exactly 4 blocks long, including the GF block, and no excluded blocks. Green flag only
	q7_cands = set() #Check if 2-4 blocks long, including the GF block, and no excluded blocks. spriteClicked or green flag

	#Find projects with candidate code
	for project in projects:
		project.greenFlags= nj.find_blocks(project.blocks,'event_whenflagclicked')
		project.spriteClickeds = nj.find_blocks(project.blocks,'event_whenthisspriteclicked')
		project.keyPresseds = nj.find_blocks(project.blocks,'event_whenkeypressed')

		#If there are any green flag blocks in the project
		if len(project.greenFlags) > 0:
			for block in project.greenFlags:
				gfScript=nj.create_script(project.blocks, block)
				if has_exc(gfScript)==False:
					project.gfScripts.append(gfScript)

					if len(gfScript)==4:
						q6_cands.add(project)
					
					if len(gfScript)>=2 and len(gfScript)<=4:
						q3_cands.add(project)
						q7_cands.add(project)
					
			
		#If there are any sprite clicked blocks in the project
		if len(project.spriteClickeds) > 0:
			for block in project.spriteClickeds:
				spriteScript=nj.create_script(project.blocks, block)
				if has_exc(spriteScript)==False:
					project.scScripts.append(spriteScript)
					if len(spriteScript)>=2 and len(spriteScript)<=4:
						q3_cands.add(project)
						q7_cands.add(project)
					

		#If there are any key pressedblocks in the project
		if len(project.keyPresseds) > 0:
			for block in project.keyPresseds:
				keyScript=nj.create_script(project.blocks, block) 
				if has_exc(keyScript)==False:
					project.kpScripts.append(keyScript)
					if len(keyScript)>=2 and len(keyScript)<=4:
						q3_cands.add(project)
					

	#Decide which projects get custom code
	q3_custom = set()
	q3_noCustom = set()
	q3_custom_csv = open('q3_custom.csv','w+')
	q3_noCustom_csv = open('q3_noCustom.csv','w+')
	decide_custom(q3_cands, q3_custom, q3_noCustom,q3_custom_csv,q3_noCustom_csv)

	q6_custom = set()
	q6_noCustom = set()
	q6_custom_csv = open('q6_custom.csv','w+')
	q6_noCustom_csv = open('q6_noCustom.csv','w+')
	decide_custom(q6_cands, q6_custom, q6_noCustom,q6_custom_csv,q6_noCustom_csv)

	q7_custom = set()
	q7_noCustom = set()
	q7_custom_csv = open('q7_custom.csv','w+')
	q7_noCustom_csv = open('q7_noCustom.csv','w+')
	decide_custom(q7_cands, q7_custom, q7_noCustom,q7_custom_csv,q7_noCustom_csv)

	#Create custom questions for chosen projects
	directory = "json_files/"
	for project in q3_custom:
		customize_q3(project)
		
		for question in project.questions:
			if question.ID == 'Question 3':
				for i in range(0,len(question.scripts)):
					filename = directory + project.username+'_q3_script'+str(i)+'.json'
					q3_file = open(filename,'w+')
					print>>q3_file,question.scripts[i]
					print>>q3_file,'\n'
	
	for project in q6_custom:
		customize_q6(project)
		filename = directory + project.username+'_q6.json'
		q6_file = open(filename,'w+')
		
		for question in project.questions:
			if question.ID == 'Question 6':
				for script in question.scripts:
					print>>q6_file,script
					print>>q6_file,'\n'

	for project in q7_custom:
		customize_q7(project)
		filename = directory + project.username+'_q7.json'
		q7_file = open(filename,'w+')
		
		for question in project.questions:
			if question.ID == 'Question 7':
				for script in question.scripts:
					print>>q7_file,script
					print>>q7_file,'\n'



if __name__ == '__main__':
	main()