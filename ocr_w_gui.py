#!/usr/bin/env python3


# USAGE
# python ocr.py --image images/example_01.png
# python ocr.py --image images/example_02.png  --preprocess blur

from tkinter import *
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import csv
import tkinter as tk


def ocr_pro():
	csv_file=open('ocr_info.csv','w+')
	csv_writer=csv.writer(csv_file)
	out_list=['Operation Successfull',]
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	# ap.add_argument("-i", "--image", required=True,
	# 	help="path to input image to be OCR'd")
	counter=1
	out_list.append('No of images found:'+str(len(os.listdir('/home/steve/Desktop/steve/internship/tesseract-python/images/'))))
	ap.add_argument("-p", "--preprocess", type=str, default="thresh",
		help="type of preprocessing to be done")
	args = vars(ap.parse_args())
	for img in os.listdir('/home/steve/Desktop/steve/internship/tesseract-python/images/'):
		print(str(counter)+ ': ' + img)

		image_loc=img

		# load the example image and convert it to grayscale
		image = cv2.imread('/home/steve/Desktop/steve/internship/tesseract-python/images/'+img)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# cv2.imshow("Image", gray)

		# check to see if we should apply thresholding to preprocess the
		# image
		if args["preprocess"] == "thresh":
			gray = cv2.threshold(gray, 0, 255,
				cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

		# make a check to see if median blurring should be done to remove
		# noise
		elif args["preprocess"] == "blur":
			gray = cv2.medianBlur(gray, 3)

		# write the grayscale image to disk as a temporary file so we can
		# apply OCR to it
		filename = "{}.png".format(os.getpid())
		cv2.imwrite(filename, gray)

		# load the image as a PIL/Pillow image, apply OCR, and then delete
		# the temporary file
		text = pytesseract.image_to_string(Image.open(filename))
		os.remove(filename)
		csv_writer.writerow([image_loc, text])
		counter=counter+1

	# OUTPUT WINDOW
	root = Tk()
	scrollbar = Scrollbar(root)
	scrollbar.pack( side = RIGHT, fill = Y )
	mylist = Listbox(root, yscrollcommand = scrollbar.set )
	for line in out_list:
	   mylist.insert(END, str(line))
	mylist.pack( side = LEFT, fill = BOTH )
	scrollbar.config( command = mylist.yview )
	mainloop()

r=tk.Tk()
r.title('ocr')
button=tk.Button(r, text='Start', width=25, command=ocr_pro)
button.pack()
button_2=tk.Button(r, text='Exit', width=25, command=r.destroy)
button_2.pack()
r.mainloop()
