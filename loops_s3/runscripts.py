#!/usr/bin/python
from subprocess import call
import os
import json
import re
import pandas as pd
# import crop_img

scratch_projects = [

]

project_names = [

]

def find_users(filename):

	try:
		df = pd.read_csv(filename, header=None)
		names = df.iloc[:,0]

		return names.tolist()
	except:
		return []

# "AES-3A", "https://scratch.mit.edu/studios/6072920/"
# "AES-3B", "https://scratch.mit.edu/studios/6072918/"
# "AES-3C", "https://scratch.mit.edu/studios/6072915/"
# "AES-3D", "https://scratch.mit.edu/studios/6072916/"
# "GP-3", "https://scratch.mit.edu/studios/7089624/"

lsp = len(scratch_projects)

for i in range(lsp):

	project = scratch_projects[i]
	call(["python", "loopQnGen.py", project])

	call(["python3", "parse_json.py"])

	img_directory = "img_files/"

	directory = ""
	files = os.listdir(".")
	if '.DS_Store' in files:
		files.remove('.DS_Store')

	c = 0
	filedir = {}
	for filename in files:
		filedir[c] = filename
		if filename[-3:] == ".js":
			call(["node", directory + filename])
			old_name = img_directory + "scratchblocks.png"
			new_name = img_directory + filename[:-3] + ".png"
			if "script" not in filename:
				new_name = img_directory + filename[:-3] + "_0_script0" + ".png"
			try:
				os.rename(old_name, new_name)
				call(["python3", "crop_img.py", new_name, img_directory])
			except:
				print(filename)
			c += 1

	call(["python3", "maketex.py"])

	files = os.listdir('.')
	if '.DS_Store' in files:
		files.remove('.DS_Store')

	j = 0
	for filename in files:
		if filename[-3:] == "tex":
			call(["pdflatex", filename])
			j += 1

	# Clean up
	files = os.listdir('.')
	if '.DS_Store' in files:
		files.remove('.DS_Store')
	pdflist = ["pdfunite"]
	for filename in files:
		if filename[-3:] == "pdf":
			pdflist.append(filename)

	pdflist.append(project_names[i] + ".pdf")
	call(pdflist)

	file_extensions = ["tex", "aux", "log", "pdf", ".js"]
	archive = "archive/"
	for filename in files:
		file_type = filename[-3:]
		if file_type in file_extensions:
			if filename != "script.js":
				try:
					os.rename(filename, archive + filename)
				except:
					continue

	dir1 = 'json_files/'
	files = os.listdir('./' + dir1)
	if '.DS_Store' in files:
		files.remove('.DS_Store')
	for filename in files:
		os.rename(dir1 + filename, archive + filename)

	dir2 = 'user_json_files/'
	files = os.listdir('./' + dir2)
	if '.DS_Store' in files:
		files.remove('.DS_Store')
	for filename in files:
		os.rename(dir2 + filename, archive + filename)

	dir3 = 'scripts/'
	files = os.listdir('./' + dir3)
	if '.DS_Store' in files:
		files.remove('.DS_Store')
	for filename in files:
		if filename[-3:] == ".js":
			os.rename(dir3 + filename, archive + filename)

	dir4 = 'cleaned_json/'
	files = os.listdir('./' + dir4)
	if '.DS_Store' in files:
		files.remove('.DS_Store')
	for filename in files:
		os.rename(dir4 + filename, archive + filename)

	dir5 = 'img_files/'
	files = os.listdir('./' + dir5)
	if '.DS_Store' in files:
		files.remove('.DS_Store')
	for filename in files:
		os.rename(dir5 + filename, archive + filename)

	allstudents = find_users("students.csv")
	students1 = find_users("q1_custom.csv")
	students7 = find_users("q7_custom.csv")
	students8 = find_users("q8_custom.csv")

	allstudents = set(allstudents)

	studentdict = {}

	for student in allstudents:
		studentdict[student] = []

	for s1 in students1:
		studentdict[s1].append(1)

	for s7 in students7:
		studentdict[s7].append(7)

	for s8 in students8:
		studentdict[s8].append(8)

	output = "Custom Questions\n"

	for student in studentdict.keys():
		questionlist = studentdict[student]
		questionlist = set(questionlist)
		qstr = ""
		for questioncounter in questionlist:
			qstr += str(questioncounter) + " "
		output += student + " has custom questions for: " + qstr + "\n"

	student_directory = open(project_names[i] + "_directory.txt", "w")
	student_directory.write(output)
	student_directory.close()
