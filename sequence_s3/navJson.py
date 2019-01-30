#Jean Salac
#Functions to navigate Scratch 3 json file

#Input: list of all the projects' blocks and opcode of interest
#Returns a dictionary of all the blocks for the script that contains the opcode of interest
#def create_script(blocks, opcode):

def main():
	# Enter some arbitrary project json file to test functions as cmd line argument
	json_file = sys.argv[1]

	with open(json_file) as f:
		data = json.load(f)
	
	#Scratch 3 json file is a giant multinested dictionary.
	#First layer has one key: 'targets'
	#Value is all the project informaton (mostly sprites, & some internal Scratch specs) 
	projInfo = data['targets']

	#Pull out all the blocks from a project
	all_blocks = {}
	for item in projInfo:
		blocks = item['blocks']
		for blockName in blocks:
			blockInfo=blocks[blockName]
			#Add to all_blocks dictionary: key=blockName, value=blockInfo
			all_blocks[blockName] = blockInfo

if __name__ == '__main__':
	main()