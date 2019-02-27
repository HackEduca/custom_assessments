from PIL import Image
import numpy as np
import os
from os import listdir

def crop(image_name, cropped_img_dir):
	im = image_name.split('/')
	myImage = Image.open(image_name)
	black = Image.new('RGBA', myImage.size)
	myImage = Image.composite(myImage, black, myImage)
	myCroppedImage = myImage.crop(myImage.getbbox())
	myCroppedImage.save(cropped_img_dir + im[1])
