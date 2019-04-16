#!/usr/bin/python
from subprocess import call
import os
import json
import re
import pandas as pd
# import crop_img

scratch_projects = [
"https://scratch.mit.edu/studios/6064583/"
]

project_names = [
"TES-3C"
]

def find_users(filename):

	try:
		df = pd.read_csv(filename, header=None)
		names = df.iloc[:,0]

		return names.tolist()
	except:
		return []

# Finished "https://scratch.mit.edu/studios/5831048/", "SES_Class 3A_(304-21)"
# "https://scratch.mit.edu/studios/5831055/", "SES_Class_4B_(309-24)",
# "https://scratch.mit.edu/studios/5831042/", "SES_Class_3B_(305-21)",
# "https://scratch.mit.edu/studios/5830937/", "SES_Class_3C_(307-22)",
# "https://scratch.mit.edu/studios/5831053/", "SES_Class_4A_(302-24)",
# "https://scratch.mit.edu/studios/5831059/", "SES_Class_4C_(300-23*)",
# "https://scratch.mit.edu/studios/5831066/", "SES_Class_5A_(311-23)",
# "https://scratch.mit.edu/studios/5831076/", "SES_Class_5B_(312-23)",
# "https://scratch.mit.edu/studios/5752419/", "GP_3rd"

# 2
# "AES-3A", "https://scratch.mit.edu/studios/5932307/"
# "AES-3B", "https://scratch.mit.edu/studios/5928999/"
# "AES-3C", "https://scratch.mit.edu/studios/5920444/"
# "AES-3D", "https://scratch.mit.edu/studios/5995133/"
# 2 (Santa Ana)
# "https://scratch.mit.edu/studios/5839918/"
# "santa_ana_1"

# 3
# "TCS-3A_(207)", "https://scratch.mit.edu/studios/5878374/"
# "TCS-3B_(208)", "https://scratch.mit.edu/studios/5885890/"
# "TCS-3C_(209)", "https://scratch.mit.edu/studios/5885892/"
# "TCS-4A_(305)", "https://scratch.mit.edu/studios/5878375/"
# "TCS-4B_(306)", "https://scratch.mit.edu/studios/5885896/"
# "TCS-5A_(303)", "https://scratch.mit.edu/studios/5878376/"
# "TCS-5B_(304)", "https://scratch.mit.edu/studios/5885889/"

# 4 
# "santa_ana_2", "https://scratch.mit.edu/studios/6047879/"

# 5
# "TES-3A", "https://scratch.mit.edu/studios/6046422/"
# "TES-3B", "https://scratch.mit.edu/studios/6050808/"
# "TES-3C", "https://scratch.mit.edu/studios/6064583/"

lsp = len(scratch_projects)

for i in range(lsp):

	# project = scratch_projects[i]
	# call(["python", "sequenceQnGen.py", project])

	# call(["python3", "parse_json.py"])

	# img_directory = "img_files/"

	# directory = ""
	# files = os.listdir(".")
	# if '.DS_Store' in files:
	# 	files.remove('.DS_Store')

	# c = 0
	# filedir = {}
	# for filename in files:
	# 	filedir[c] = filename
	# 	if filename[-3:] == ".js":
	# 		call(["node", directory + filename])
	# 		old_name = img_directory + "scratchblocks.png"
	# 		new_name = img_directory + filename[:-3] + ".png"
	# 		if "script" not in filename:
	# 			new_name = img_directory + filename[:-3] + "_script0" + ".png"
	# 		try:
	# 			os.rename(old_name, new_name)
	# 			call(["python3", "crop_img.py", new_name, img_directory])
	# 		except:
	# 			print(filename)
	# 		c += 1

	# call(["python3", "maketex.py"])

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
	students3 = find_users("q3_custom.csv")
	students6 = find_users("q6_custom.csv")
	students7 = find_users("q7_custom.csv")

	allstudents = set(allstudents)

	studentdict = {}

	for student in allstudents:
		studentdict[student] = []

	for s3 in students3:
		studentdict[s3].append(3)

	for s6 in students6:
		studentdict[s6].append(6)

	for s7 in students7:
		studentdict[s7].append(7)

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
