import os
import json
import re

def txt_to_json(directory, outputdirectory, filename):

	txtfile = open(os.path.relpath(directory + filename), 'r')
	fn = filename.split('.')[0]
	c = 0
	p = 1
	for l in txtfile:
		if(len(l) > 1):
			jsonfile = open(outputdirectory + fn + '.json', 'w')
			l2 = l.replace("u\'","\"")
			line = l2.replace("\']","\"]")
			line = line.replace("\')","\")")
			line = line.replace("(\'","(\"")
			line = line.replace("[\'","[\"")
			line = line.replace("\',","\",")
			line = line.replace("{\'","{\"")
			line = line.replace("\'}","\"}")
			line = line.replace(": \'",": \"")
			line = line.replace(", \'",", \"")
			line = line.replace("\':","\":")
			line = line.replace("u\"","\"")
			line = line.replace("None","null")
			line = line.replace("True","\"True\"")
			line = line.replace("False","\"False\"")
			while True:
				try:
					result = json.loads(line)
					break
				except Exception as e:
					if(p == 1):
						print(line)
					p += 1
					# print(l)
					print(line[225:])
					print(e)
					result = ""
					break
				c += 1
			json.dump(result, jsonfile)
			jsonfile.close()

	jsonfilename = outputdirectory + fn + '.json'

	return jsonfilename