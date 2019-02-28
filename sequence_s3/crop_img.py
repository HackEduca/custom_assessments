import PIL
from PIL import Image
import numpy as np
import os
from os import listdir
import sys

def crop():
	image_name = sys.argv[1]
	cropped_img_dir = sys.argv[2]
	im = image_name.split('/')
	myImage = Image.open(image_name)
	black = Image.new('RGBA', myImage.size)
	myImage = Image.composite(myImage, black, myImage)
	myCroppedImage = myImage.crop(myImage.getbbox())
	myCroppedImage.save(cropped_img_dir + im[1])

crop()