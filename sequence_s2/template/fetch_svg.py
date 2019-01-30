#Jean Salac
#File to grab svg from html console log
#Run with python fetch_svg.py nameOfFile (of type String)

import os
import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.chrome.options import Options

def main():
	filename = sys.argv[1]
	#Get console log for html script
	fileURL = 'file://'+str(os.path.abspath(filename+".html"))
	d = DesiredCapabilities.CHROME
	d['loggingPrefs'] = { 'browser':'ALL' }
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	#Mac Path
	driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=chrome_options)
	#Linux Path
	#driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',chrome_options=chrome_options)
	# load html file
	driver.get(fileURL)
	#open svg file for console logs
	test_pic = open(filename+'.svg','w+')

	#get console logs
	for entry in driver.get_log('browser'):
	    message = entry.get('message')
	    message_parts = message.split('"')
	    #Fetch svg
	    svg = message_parts[1]
	    for i in range(2,len(message_parts)-1):
	    	svg = svg+'"'+message_parts[i]
	    svg = svg + message_parts[len(message_parts)-1]
	    svg = svg.replace("\\u003C","<")
	    svg = svg.replace('\\"','"')
	    svg = svg.replace("\\n"," ")
	    print>>test_pic,svg
		


if __name__ == '__main__':
	main()