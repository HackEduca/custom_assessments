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
	loop=''
	#List of the scripts of events of interest
	gfScripts=''
	scScripts=''
	kpScripts=''
	lpScripts=''
	lenQ7 = 4 #Num blocks in q7 script. Default is 4

	def __init__(self, ID):
		self.ID = ID
		self.blocks = {}
		self.questions = []
		self.username = ''
		self.greenFlags=[]
		self.spriteClickeds=[]
		self.keyPresseds=[]
		self.loop=[]
		self.gfScripts=[]
		self.scScripts=[]
		self.kpScripts=[]
		self.lpScripts=[]
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
def customize_q1(project):
	q1=make_question('Question 1')
	for script in project.lpScripts:
		if len(script)>=2 and len(script)<=4:
			q1.scripts.append(script)
			break

	project.questions.append(q1)



#Question 6: Find a "When Green Flag". No loops, conditionals, variables, play sound.
#Check if 4 blocks long, including the GF block, and no excluded blocks.
#Takes in project and creates a custom question for project
def customize_q7(project):
	q7 = make_question('Question 7')
	for script in project.lpScripts:
		if len(script)>=3 and len(script)<=4:
			q7.scripts.append(script)
			break
	project.questions.append(q7)

	

#Question 7: Find a spriteClicked or GreenFlag. No loops, conditionals, variables, play sound.
#Check if 2-4 blocks long, including the GF block, and no excluded blocks.
#Takes in project and creates a custom question for project
def customize_q8(project):
	q8 = make_question('Question 8')
	for script in project.lpScripts:
		if len(script)>=2 and len(script)<=6:
			q8.scripts.append(script)
			break
	project.questions.append(q8)



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
	exc_opcodes=['control_repeat_until','control_forever','control_if ',
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
		username_set = set()


		for project in studio_parser.find_all('li'):
			#Find the span object with owner attribute
			span_string = str(project.find("span","owner"))
			
			#Pull out scratch username
			scratch_username = span_string.split(">")[2]
			scratch_username = scratch_username[0:len(scratch_username)-3]
			if (scratch_username not in username_set):
				username_set.add(scratch_username)
				
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
	q1_cands = set() # Check if len is >=2 and <5, 1-3 blocks in loop
	q7_cands = set() # 2 or 3 blocks in loop
	q8_cands = set() # 1-5 blocks in the loop

	#Find projects with candidate code
	for project in projects:
		project.loop = nj.find_blocks(project.blocks,'control_repeat')
		if len(project.loop) > 0:
			for block in project.loop:
				lpScript=nj.create_script(project.blocks, block)
				if has_exc(lpScript)==False:
					project.lpScripts.append(lpScript)
					lps = len(lpScript)
					if lps <= 4:
						q1_cands.add(project)
						if lps >= 3:
							q7_cands.add(project)
					if lps >= 2 and lps <= 6:
						q8_cands.add(project)

	#Decide which projects get custom code
	q1_custom = set()
	q1_noCustom = set()
	q1_custom_csv = open('q1_custom.csv','w+')
	q1_noCustom_csv = open('q1_noCustom.csv','w+')
	decide_custom(q1_cands, q1_custom, q1_noCustom,q1_custom_csv,q1_noCustom_csv)

	q7_custom = set()
	q7_noCustom = set()
	q7_custom_csv = open('q7_custom.csv','w+')
	q7_noCustom_csv = open('q7_noCustom.csv','w+')
	decide_custom(q7_cands, q7_custom, q7_noCustom,q7_custom_csv,q7_noCustom_csv)

	q8_custom = set()
	q8_noCustom = set()
	q8_custom_csv = open('q8_custom.csv','w+')
	q8_noCustom_csv = open('q8_noCustom.csv','w+')
	decide_custom(q8_cands, q8_custom, q8_noCustom,q8_custom_csv,q8_noCustom_csv)

	#Create custom questions for chosen projects
	directory = "json_files/"
	for project in q1_custom:
		customize_q1(project)
		
		for question in project.questions:
			if question.ID == 'Question 1':
				for i in range(0,len(question.scripts)):
					filename = directory + project.username+'_q1_script'+str(i)+'.json'
					q1_file = open(filename,'w+')
					print>>q1_file,question.scripts[i]
					print>>q1_file,'\n'
	
	for project in q7_custom:
		customize_q7(project)
		filename = directory + project.username+'_q7.json'
		q7_file = open(filename,'w+')
		
		for question in project.questions:
			if question.ID == 'Question 7':
				for script in question.scripts:
					print>>q7_file,script
					print>>q7_file,'\n'
 
	for project in q8_custom:
		customize_q8(project)
		filename = directory + project.username+'_q8.json'
		q8_file = open(filename,'w+')
		
		for question in project.questions:
			if question.ID == 'Question 8':
				for script in question.scripts:
					print>>q8_file,script
					print>>q8_file,'\n'



if __name__ == '__main__':
	main()