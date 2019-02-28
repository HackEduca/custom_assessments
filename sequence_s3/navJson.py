#Jean Salac
#Functions to navigate Scratch 3 json file

import sys
import json

#Function to gather all the blocks from Scratch project's json
#Takes in json data and returns a dictionary of blocks
def get_blocks(jsonData):
	try:
		projInfo = jsonData['targets']
		allBlocks={}
		for item in projInfo:
			blocks = item['blocks']
			for blockName in blocks:
				blockInfo=blocks[blockName]
				#Add to all blocks dictionary: key=blockName, value=blockInfo
				allBlocks[blockName] = blockInfo
	except:
		allBlocks = {}
	return allBlocks

#Function to count the number of blocks of a certain opcode was used.
#Args: list of all the projects' blocks and opcode of interest
#Returns number of times block was used
def count_blocks(blocks,opcode):
	total = 0
	for blockName in blocks:
		blockInfo=blocks[blockName]
		#Block info is also a dictionary
		blockOpcode = blockInfo['opcode']
		if blockOpcode == opcode:
			total+=1
	return total

#Function to find desired blocks
#Args: list of all the projects' blocks and opcode of interest
#Returns a list of block IDs with the desired opcode
def find_blocks(blocks, opcode):
	found_blocks=[]

	for blockName in blocks:
		blockInfo=blocks[blockName]
		#Block info is also a dictionary
		blockOpcode = blockInfo['opcode']
		if blockOpcode == opcode:
			found_blocks.append(blockName)
	
	return found_blocks


#Function to create a script 
#Args: list of all the projects' blocks and block ID
#Returns a dictionary of the blocks in the script that contains the block of interest
#Scripts have to be runnable by scratch, i.e. first block must be an event, and there must be something after the event.
def create_script(blocks, blockID):
	script = {}
	event_opcodes = ['event_whenflagclicked', 'event_whenthisspriteclicked','event_whenbroadcastreceived','event_whenkeypressed', 'event_whenbackdropswitchesto','event_whengreaterthan']

	#Find all blocks that come before
	curBlockID = blockID #Initialize with blockID of interest
	while curBlockID is not None:
		curBlockInfo = blocks[curBlockID] #Pull out info about the block
		script[curBlockID]=curBlockInfo #Add the block itself to the script dictionary

		#Get parent info out
		parentID = curBlockInfo['parent'] #Block that comes before has key 'parent'
		# parentInfo = blocks[parentID]
		opcode = curBlockInfo['opcode']

		#If the block is not part of a script (i.e. it's the first block, but is not an event), return empty dictionary
		if parentID is None and opcode not in event_opcodes:
			script = {}
			return script

		#Iterate: set parent to curBlock
		curBlockID = parentID

	#Find all blocks that come after
	curBlockID = blockID #Initialize with blockID of interest
	while curBlockID is not None:
		curBlockInfo = blocks[curBlockID] #Pull out info about the block
		script[curBlockID]=curBlockInfo #Add the block itself to the script dictionary

		#Get next info out
		nextID = curBlockInfo['next'] #Block that comes after has key 'next'
		#nextInfo = blocks[nextID]
		opcode = curBlockInfo['opcode']
		
		#If the block is not a script (i.e. it's an event but doesn't have anything after), return empty dictionary
		if nextID is None and opcode in event_opcodes:
			script = {}
			return script

		#Iterate: Set next to curBlock
		curBlockID = nextID

	return script




# def main():
# 	# Enter some arbitrary project json file to test functions as cmd line argument
# 	json_file = sys.argv[1]

# 	with open(json_file) as f:
# 		data = json.load(f)
	
# 	#Scratch 3 json file is a giant multinested dictionary.
# 	#First layer has one key: 'targets'
# 	#Value is all the project informaton (mostly sprites, & some internal Scratch specs) 
# 	projInfo = data['targets']

# 	#Pull out all the blocks from a project
# 	all_blocks = {}
# 	for item in projInfo:
# 		blocks = item['blocks']
# 		for blockName in blocks:
# 			blockInfo=blocks[blockName]
# 			#Add to all_blocks dictionary: key=blockName, value=blockInfo
# 			all_blocks[blockName] = blockInfo

# 	#Test count_blocks function
# 	#print(count_blocks(all_blocks,'event_whenthisspriteclicked'))

# 	#Test find_blocks function
# 	sprite_clicked = find_blocks(all_blocks,'event_whenthisspriteclicked')
# 	# for item in sprite_clicked:
# 	# 	print(item)
	
# 	#Test create scripts 
# 	all_scripts = [] #List of scripts, which will be dictionaries
# 	for item in sprite_clicked:
# 		script = create_script(all_blocks,item)
# 		if len(script)>0:
# 			all_scripts.append(script)

# 	for item in all_scripts:
# 		print(item)
# 		print('\n')

# if __name__ == '__main__':
# 	main()