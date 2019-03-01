import re
import pandas as pd

def all_students(filename):

	try:
		df = pd.read_csv(filename, header=None)
		names = df.iloc[:,0]

		return names.tolist()
	except:
		return set()

def custom_questions(filename, all_students):

	f = open(filename, "r")
	students = {}

	for lines in f:
		information = lines.split(" ")
		questions = list(map(int, re.findall(r'\d+', lines)))
		try:
			questions.remove(2021)
		except:
			continue
		if len(questions) == 0:
			if 0 not in students:
				students[0] = [information[0]]
			else:
				students[0].append(information[0])
		else:
			for q in questions:
				if q not in students:
					students[q] = [information[0]]
				else:
					students[q].append(information[0])

	print("Q3 Custom")
	q3students = set(students[3])
	noq3students = totalq3students - q3students
	for i in q3students:
		print (i)
	print("Q3 Not Custom")
	for j in noq3students:
		print (j)

	print("Q6 Custom")
	try:
		q6students = set(students[6])
		noq6students = totalq6students - q6students
		for i in q6students:
			print (i)
		print("Q6 Not Custom")
		for j in noq6students:
			print (j)
	except:
		print("Q6 Not Custom")

	print("Q7 Custom")
	q7students = set(students[7])
	noq7students = totalq7students - q7students
	for i in q7students:
		print (i)
	print("Q7 Not Custom")
	for j in noq7students:
		print (j)

all_students = all_students("students.csv")
totalq3students = set(all_students("q3_custom.csv")) + set(all_students("q3_noCustom.csv"))
totalq6students = set(all_students("q6_custom.csv")) + set(all_students("q6_noCustom.csv"))
totalq7students = set(all_students("q7_custom.csv")) + set(all_students("q7_noCustom.csv"))
filename = "SES_Class 3A_(304-21)_directory.txt"
custom_questions(filename, all_students)