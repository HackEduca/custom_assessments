import os
import pandas as pd
import json

def all_users(filename):

	try:
		df = pd.read_csv(filename, header=None)
		names = df.iloc[:,0]

		return names.tolist()
	except:
		return []

def create_assessment(custom_directory, user, q1, q7, q8, img_dir, img_list, q7dict):

	custom_am = open(user+".tex", "w")
	assessment = []
	n_questions = user + " has custom questions for: "

	# Header
	hf = open(custom_directory+"header.tex")
	header = hf.readlines()
	for h in header:
		if "Scratch Username: " in h:
			username = h.split("Scratch Username: ")
			if ("_" in user):
				user = user.replace("_", "")
			line = "Scratch Username: " + user + "\n"
		else:
			line = h
		assessment.append(line)

	# Question 1
	q1f = open(custom_directory+"q1.tex")
	q1lines = q1f.readlines()
	if user in q1:
		n_questions += " Q1"
		q1lines = custom_question(q1lines, user, img_dir, img_list)
	for line in q1lines:
		assessment.append(line)

	# Question 2 to 6
	q26f = open(custom_directory+"q26.tex")
	q26lines = q26f.readlines()
	for line in q26lines:
		assessment.append(line)

	# Question 7
	q7counter = 0
	if user+"_q7_0" in q7dict:
		q7counter = q7dict[user+"_q7_0"]
	if q7counter == 3:
		q7f = open(custom_directory + "q7_1.tex")
	else:
		q7f = open(custom_directory+"q7.tex")
	q7lines = q7f.readlines()
	if user in q7:
		n_questions += " Q7"
		q7lines = custom_question(q7lines, user, img_dir, img_list)
	for line in q7lines:
		assessment.append(line)

	# Question 8
	if user in q8:
		q8f = open(custom_directory+"q8_1.tex")
	else:
		q8f = open(custom_directory+"q8.tex")
	q8lines = q8f.readlines()
	if user in q8:
		n_questions += " Q8"
		q8lines = custom_question(q8lines, user, img_dir, img_list)
	for line in q8lines:
		assessment.append(line)

	for l in assessment:
		custom_am.write(l)

	custom_am.close()
	hf.close()
	q1f.close()
	q26f.close()
	q7f.close()
	q8f.close()

def custom_question(qlines, user, img_directory, img_list):

	input_img = {}

	for i in img_list:
		img = i.split("_")
		if img[0] == user:
			c = i[len(i)-5]
			input_img[c] = [i]

	cust_q = []

	img_counter = 0
	for l in qlines:
		gen_img = str(img_counter) + ".png"
		if gen_img in l:
			if str(img_counter) in input_img:
				img = input_img[str(img_counter)]
				lines = l.split("{")
				lines = lines[1].split("}")
				cust_img = user + "_" + lines[0]
				newl = l.replace(lines[0], cust_img)
				newl = newl.replace("q7_", "q7_0_")
				newl = newl.replace("q8_", "q8_0_")
				newl = newl.replace("scale=.3", "scale=.2")
				# newl = newl.replace("1cm", "0.5cm")
				cust_q.append(newl)
				img_counter += 1
			else:
				cust_q.append(l)
			img_counter += 1
		else:
			cust_q.append(l)

	return cust_q

all_students = all_users("students.csv")
q1_students = all_users("q1_custom.csv")
q7_students = all_users("q7_custom.csv")
q8_students = all_users("q8_custom.csv")
with open('q7dict.json') as q7jsonfile:
	q7dict = json.load(q7jsonfile)
custom_directory = "custom_scratch3/"
img_directory = "img_files"
img_list = os.listdir(img_directory)
if '.DS_Store' in img_list:
	img_list.remove('.DS_Store')
setstudents = set(all_students)
for student in all_students:
	create_assessment(custom_directory, student, q1_students, 
		q7_students, q8_students, img_directory, img_list, q7dict)

