#!/usr/bin/python
from subprocess import call
import os

files = os.listdir('pdf_files')
if '.DS_Store' in files:
	files.remove('.DS_Store')

list_of_files = ""

for filename in files:
	list_of_files += filename + " "

call(["pdfunite", files, "all_assessments.pdf"])