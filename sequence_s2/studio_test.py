#Jean Salac
#File to test project URL fetching from scratch studio link

import sys
import json
import requests
from pprint import pprint
from bs4 import BeautifulSoup

def main():
	url = 'https://scratch.mit.edu/site-api/projects/in/4823921/1/'
	r = requests.get(url, allow_redirects=True)
	studio_html = r.content
	soup = BeautifulSoup(studio_html, "html.parser")
	for project in soup.find_all('li'):
		#Find the span object with owner attribute
		span_string = str(project.find("span","owner"))
		scratchID = span_string.split(">")[2]
		scratchID = scratchID[0:len(scratchID)-3]
		print(scratchID)
		#Get project ID
		print(project.get('data-id'))
		print("\n")
		


if __name__ == '__main__':
	main()