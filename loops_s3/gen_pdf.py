#!/usr/bin/python
from subprocess import call
import os

custom_questions = ["ig428862",
"jo428856",
"mm430328",
"rm417703",
"en428861",
"al430369",
"da422719",
"ol428822",
"ea428817",
"zm438366",
"mp429597",
"jg421519",
"cm421509",
"dj425312",
"md430147",
"ck428750"]

assessment_directory = '/custom_assessments/'

files = os.listdir('.' + assessment_directory)
if '.DS_Store' in files:
	files.remove('.DS_Store')
print(files)
for filename in files:
	if filename[-3:] == "tex":
		for user in custom_questions:
			if user in filename:
				print(user)
				# call(["pdflatex", assessment_directory + filename])
				break
