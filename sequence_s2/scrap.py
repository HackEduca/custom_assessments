from pprint import pprint
import sys
import random

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#Populate dictionary of opcode to block translations from txt files with opcodes and blocks
opcode_dict= {}
def populate_opcode_dict():
	global opcode_dict
	opcode_dict = {'changeXposBy:': 'change x by ()', 'show': 'show', 
	'whenIReceive': 'when I receive ()', '/': '() / ()', 
	'getParam': 'custom block parameter', 'rounded': 'round ()', 
	'doForLoop': 'for each () in ()', 'lookLike:': 'switch costume to ()', 
	'sayNothing': 'say nothing', 'timeAndDate': 'current ()', 
	'color:sees:': 'color () is touching ()?', 'changeSizeBy:': 'change size by ()', 
	'setSizeTo:': 'set size to ()%', 'fxTest': 'color fx test ()', 
	'turnRight:': 'turn right () degrees', 'mousePressed': 'mouse down?', 
	'concatenate:with:': 'join ()()', 'doPlaySoundAndWait': 'play sound () until done',
	'lineCountOfList:': 'length of ()', 'timestamp': 'days since 2000', 
	'setVideoTransparency': 'set video transparency to ()%', 
	'setLine:ofList:to:': 'replace item () of () With ()', 'warpSpeed': 'all at once', 
	'getUserId': 'user id', 'computeFunction:of:': '() of ()', 'nextCostume': 'next costume', 
	'not': 'not ()', 'changeYposBy:': 'change y by ()', 'gotoX:y:': 'go to x: () y: ()', 
	'whenClicked': 'when this sprite clicked', 'setVideoState': 'turn video ()', 
	'costumeIndex': 'costume #', 'wait:elapsed:from:': 'wait () secs', 
	'setPenHueTo:': 'set pen color to ()', 'scrollRight': 'scroll right ()', 
	'setRotationStyle': 'set rotation style ()', 'whenGreenFlag': 'when green flag clicked', 
	'stopAllSounds': 'stop all sounds', 'goBackByLayers:': 'go back () layers', 'heading': 'direction', 
	'setPenShadeTo:': 'set pen shade to ()', 'penSize:': 'set pen size to ()', 
	'playSound:': 'play sound ()', 'playDrum': 'play drum () for () beats', 
	'setTempoTo:': 'set tempo to () bpm', 'obsolete': 'obsolete', 
	'rest:elapsed:from:': 'rest for () beats', 'xpos:': 'set x to ()', 'doWhile': 'while ()', 
	'sensor:': '() sensor value', 'changePenSizeBy:': 'change pen size by ()', 
	'doWaitUntil': 'wait until ()', 'randomFrom:to:': 'pick random () to ()', 
	'letter:of:': 'letter () of ()', 'getLine:ofList:': 'item () of ()', 'stopAll': 'stop all', 
	'scale': 'size', 'hide': 'hide', 'hideAll': 'hide all sprites', 
	'doBroadcastAndWait': 'broadcast () and wait', '+': '() + ()', 'stopSound:': 'stop sound ()', 
	'contentsOfList:': '()', 'changeVar:by:': 'change () by ()', 'sensorPressed:': 'sensor ()?', 
	'abs': 'abs ()', 'changeGraphicEffect:by:': 'change () effect by ()', 
	'changePenHueBy:': 'change pen color by ()', 'COUNT': 'counter', 'tempo': 'tempo', 
	'hideList:': 'hide list ()', 'costumeName': 'costume name', 'say:': 'say ()', 
	'ypos': 'y position', 'think:': 'think ()', 'distanceTo:': 'distance to ()', 
	'whenKeyPressed': 'when () key pressed', 'filterReset': 'clear graphic effects', 
	'doUntil': 'repeat until ()', 'soundLevel': 'loudness', 'penColor:': 'set pen color to ()', 
	'broadcast:': 'broadcast ()', 'startScene': 'switch backdrop to ()', 'deleteClone': 'delete this clone', 
	'senseVideoMotion': 'video () on ()', 'timer': 'timer', '|': '() or ()', 
	'whenSceneStarts': 'when backdrop switches to ()', 'bounceOffEdge': 'if on edge, bounce', 
	'setGraphicEffect:to:': 'set () effect to ()', 'CLR_COUNT': 'clear counter', 
	'list:contains:': '() contains ()', 'doForeverIf': 'forever if ()', 'stringLength:': 'length of ()', 
	'hideVariable:': 'hide variable ()', 'readVariable': '() (Variables block)', 
	'midiInstrument:': 'set instrument to ()', 'doAsk': 'ask () and wait', 'doIf': 'if () then', 
	'backgroundIndex': 'backdrop #', 'deleteLine:ofList:': 'delete () of ()', 
	'changeVolumeBy:': 'change volume by ()', '&': '() and ()', 'getAttribute:of:': '() of ()', 
	'*': '() * ()', 'startSceneAndWait': 'switch backdrop to () and wait', 
	'changePenShadeBy:': 'change pen shade by ()', 'doRepeat': 'repeat ()', '>': '() > ()', 
	'instrument:': 'set instrument to ()', 'xpos': 'x position', 
	'think:duration:elapsed:from:': 'think () for () secs', 'nextScene': 'next backdrop', 
	'forward:': 'move () steps', 'volume': 'volume', 'mouseY': 'mouse y', 'mouseX': 'mouse x', 
	'showList:': 'show list ()', 'whenSensorGreaterThan': 'when () is greater than ()', 
	'gotoSpriteOrMouse:': 'go to ()', 'insert:at:ofList:': 'insert () at () of ()', 
	'sceneName': 'backdrop name', 'doForever': 'forever', '<': '() < ()', 
	'glideSecs:toX:y:elapsed:from:': 'glide () Secs to X: () Y: ()', 'stopScripts': 'stop ()', 
	'turnAwayFromEdge': 'point away from edge', 'noteOn:duration:elapsed:from:': 'play note () for () beats', 
	'ypos:': 'set y to ()', 'clearPenTrails': 'clear', 'drum:duration:elapsed:from:': 'play drum () for () beats', 
	'touchingColor:': 'touching color ()?', 'xScroll': 'x scroll', 'doIfElse': 'if () then, else', 
	'keyPressed:': 'key () pressed?', 'pointTowards:': 'point towards ()', 'putPenDown': 'pen down', 
	'setVar:to:': 'set () to ()', '%': '() mod ()', '-': '() - ()', 'sqrt': 'sqrt ()', 
	'showVariable:': 'show variable ()', 'answer': 'answer', 'putPenUp': 'pen up', '=': '() = ()', 
	'isLoud': 'loud?', 'append:toList:': 'add () to ()', 'whenCloned': 'when I start as a clone', 
	'timerReset': 'reset timer', 'comeToFront': 'go to front', 'INCR_COUNT': 'incr counter', 
	'setVolumeTo:': 'set volume to ()%', 'scrollUp': 'scroll Up ()', 'turnLeft:': 'turn left () degrees', 
	'doReturn': 'stop script', 'heading:': 'point in direction ()', 'stampCostume': 'stamp', 
	'getUserName': 'username', 'yScroll': 'y scroll', 'touching:': 'touching ()?', 'undefined': 'undefined', 
	'changeTempoBy:': 'change tempo by ()', 'scrollAlign': 'align scene ()', 'createCloneOf': 'create clone of ()', 
	'say:duration:elapsed:from:': 'say () for () secs'}

def main():
	# prefix_file = sys.argv[1]
	# q1txt_file = sys.argv[2]
	# q1_prefix_file = sys.argv[3]
	# q1_suffix_file = sys.argv[4]
	# q1to6_file = sys.argv[5]
	# ans2line_file = sys.argv[5]
	# ans3line_file = sys.argv[6]
	# q7_file = sys.argv[7]
	# suffix_file = sys.argv[8]

	prefix = open("prefix.txt").read()
	q1_text = open("q1text.txt").read()
	q1_prefix = open("q1_prefix.txt").read()
	q1_suffix = open("q1_suffix.txt").read()
	q2to6 = open("q2to6.txt").read()
	ans2line = open("ans2line.txt").read()
	ans3line = open("ans3line.txt").read()
	q7tex = open("q7.txt").read()
	suffix = open("suffix.txt").read()

	q1_images = ["q1_script0","q1_script1","q1_script2","q1_script3"]
	random.shuffle(q1_images)
	q1=q1_text
	for image in q1_images:
		q1 = q1+q1_prefix+image+q1_suffix

	texFile = open("test.tex",'w+')
	texString = prefix+"JSalac \n"+q1+q2to6+ans2line+"\n"+q7tex+ans3line+suffix
	print>>texFile, texString
	

if __name__ == '__main__':
	main()