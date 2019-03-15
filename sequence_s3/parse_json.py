import os
import json
import re
import util.clean_opcodes as co
import util.txt_to_json as txtjson

def parse_json(jsonfile):

	with open(jsonfile) as f:
		events = json.load(f)

	commands = []
	startkey = None

	for key in events:
		# import ipdb
		# ipdb.set_trace()
		val = events[key]
		if(val['parent'] is None):
			startkey = key

	while(startkey is not None):
		val = events[startkey]
		oc = val['opcode']
		try:
			sbcode = op_codes[oc][0]
		except:
			break
		ipval = val['inputs']
		if len(ipval) == 0:
			ipval = None
		fval = val['fields']
		if len(fval) == 0:
			fval = None
		cm = (sbcode, ipval, fval)
		commands.append(cm)
		startkey = val['next']

	return commands

def parse_commands(commands):

	lencm = len(commands)
	result = ""

	for i in range(lencm):
		val = commands[i][0]
		inputs = commands[i][1]
		fields = commands[i][2]
		if inputs is None and fields is None:
			result += val
		elif inputs is not None:
			partialresult = cm_input(val, inputs, "(")
			partialresult = cm_input(partialresult, inputs, "[")
			result += partialresult
		else:
			partialresult = fd_input(val, fields, "(")
			result += partialresult
		result += "%0A"

	result = result.replace("Glide ()", "Glide (1)")
	result = result.replace("X: () Y: ()", "X: (1) Y: (1)")
	result = result.replace("Backdrop to ()", "Backdrop to (backdrop v)")
	result = result.replace("Turn () Degrees Right", "Turn cw (10) degrees")
	result = result.replace("Turn () Degrees Left", "Turn ccw (10) degrees")
	result = result.replace("Ask ()", "Ask (Hi)")
	result = result.replace("Change () Effect by ()", "Change (effect v) Effect by (1)")
	result = result.replace("()", "(1)")
	result = result.replace("(", "%5B")
	result = result.replace(")", "%5D")
	result = result.replace("For", " for")
	result = result.replace("'m", " am")
	result = result.replace("t's", "t is")
	result = result.replace("'", "")
	result = result.replace(" ", "%20")

	# with open('scratch_code.txt', 'w') as f:
	# 	f.write(result)
	return result

def cm_input(val, inputs, delimiter):

	if delimiter not in val:
		return val
	vallist = val.split(delimiter)
	result = ""
	i = 0
	lenval = len(vallist)
	c = 0
	for v in vallist:
		if(i < lenval-1):
			inputval = findinputval(inputs, c)
			if inputval == "sound":
				inputval = "sound v"
			elif inputval == "costume":
				inputval = "costume v"
			elif inputval is not None:
				try:
					inputval = inputval.replace("(", " ")
					inputval = inputval.replace(")", " ")
				except:
					inputval = ""
			else:
				inputval = ""
			result += v + delimiter + inputval
			c += 1
		else:
			result += v
		i += 1

	return result

def fd_input(val, fields, delimiter):

	if delimiter not in val:
		return val
	vallist = val.split(delimiter)
	result = ""
	i = 0
	result += vallist[0] + delimiter + findfieldval(fields) + vallist[1]

	return result

def findinputval(inputs, counter):

	if 'MESSAGE' in inputs:
		if counter == 0:
			message = inputs['MESSAGE'][1][1]
			if len(message) >= 25:
				message = message[:22] + "..."
			return message
	if 'SECS' in inputs:
		if counter == 1:
			return inputs['SECS'][1][1]
	if 'STEPS' in inputs:
		return inputs['STEPS'][1][1]
	if 'DURATION' in inputs:
		return inputs['DURATION'][1][1]
	if 'SOUND_MENU' in inputs:
		return "sound"
	if 'COSTUME' in inputs:
		return "costume"
	return None

def findfieldval(fields):

	if 'KEY_OPTION' in fields:
		return fields['KEY_OPTION'][0] + " v"

def create_script(directory, default_script, data, filename):

	f = open(default_script, "r")
	script = f.readlines()
	fn = filename.split(".")
	script_name = directory + fn[0] + ".js"

	custom_script = open(script_name, "w")
	for line in script:
		code = "const block_code = \'" + data + "\';"
		line = line.replace("const block_code = \'\';", code)
		custom_script.write(line)

def find_files(directory):

	files = os.listdir(directory)
	return files

directory = "json_files/"
files = find_files(directory)
if '.DS_Store' in files:
	files.remove('.DS_Store')
op_codes = co.clean_opcodes("opcodes.csv")
output_directory = "cleaned_json/"
q7dict = {}
for filename in files:
	try:
		jsonfile = txtjson.txt_to_json(directory, output_directory, filename)
		default_script = "script.js"
		commands = parse_json(jsonfile)
		scratchblocks_commands = parse_commands(commands)
		create_script("", default_script, scratchblocks_commands, filename)
		if "q7" in filename:
			n_commands = scratchblocks_commands.count("%0A")
			q7dict[filename[:-5]] = n_commands
	except:
		continue
with open("q7dict.json", "w") as outfile:
	json.dump(q7dict, outfile)
