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

#Scratch Project Class.
class Project(object):
	ID = ''
	blocks = ''
	questions = ''
	username = '' #Scratch username
	lenQ7 = 4 #Num blocks in q7 script. Default is 4

	def __init__(self, ID):
		self.ID = ID
		self.blocks = {}
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
	scripts = [] #Question scripts in json form
	scrBlks= [] #Question scripts in Scratchblocks syntax


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

			#Add project blocks 
			projInfo = data['targets']
			for item in projInfo:
				blocks = item['blocks']
				for blockName in blocks:
					blockInfo=blocks[blockName]
					#Add to projects' blocks dictionary: key=blockName, value=blockInfo
					newProject.blocks[blockName] = blockInfo
				

			#Add project to the global list of projects
			projects.append(newProject)

		pageNum+=1
		studio_api_url = sa.studio_to_API(studioURL,pageNum)
		r = requests.get(studio_api_url, allow_redirects=True)

	for project in projects:
		print(project.username+"\n")
		for blockName in project.blocks:
			print(blockName)
			print('\n')
			print(project.blocks[blockName])
			print('\n')


if __name__ == '__main__':
	main()