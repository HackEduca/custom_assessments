#Jean Salac
#Python script to generate csv files of logins and passwords given a csv of schools and teachers

import sys
import csv
from pprint import pprint
import random

def main():
	file = open(sys.argv[1])
	csv_file = csv.reader(file)
	words = ["the","dog","cat","are","but","you","act","mat","can","her",
	"was","one","our","out","day","get","has","him","his","her","how","man",
	"new","now","old","see","two","way","who","boy","did","its","let","put",
	"say","she","too","use","dad","mom","arm","leg"]

	for line in csv_file:
		scratchFileName="ScratchUse_"+line[0]+line[1]+".csv"
		scratchCSV = open(scratchFileName,"w+")
		teacherFileName="TeacherUse_"+line[0]+line[1]+".csv"
		teacherCSV=open(teacherFileName,"w+")
		header = "Student First Name,Student Last Name,Username,Password"
		print>>teacherCSV, header
		
		#Create 30 accounts
		i = 1
		for i in range(1,31):
			username = line[0]+line[1]+str(i)
			password = str(random.randint(0,99))+words[random.randint(0,len(words)-1)]+str(random.randint(0,99))
			scratchRow = username+","+password
			teacherRow = " , ,"+username+","+password
			print>>scratchCSV, scratchRow
			print>>teacherCSV, teacherRow
			i=i+1
		




if __name__ == '__main__':
	main()