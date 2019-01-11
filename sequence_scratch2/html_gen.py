#Jean Salac
#File to generate scratchblocks html files
#Run with python html_gen.py customScriptFile.txt

import sys
from pprint import pprint

def main():
	#Read scratchblocks html prefixes and suffixes
	html_prefix = open("html_prefix.txt").read()
	html_suffix = open("html_suffix.txt").read()

	#Read in file with scripts in scratchblocks syntax
	script_file = open(sys.argv[1]).read()
	scripts = script_file.split("Script")
	#Remove the first blank element
	scripts = scripts[1:len(scripts)]

	script_names = ["q3_script0","q3_script1","q3_script2","q3_script3","q6_script0","q7_script0"]

	for i in range(0,len(scripts)):
		#Generate html file for each script
		script = scripts[i].strip()
		html_file = open(script_names[i]+".html",'w+')
		html_text = html_prefix+script+html_suffix
		print>>html_file, html_text


if __name__ == '__main__':
	main()