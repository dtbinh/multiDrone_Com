#!/usr/bin/python
# coding=utf-8
"""
@filename: main.py
@brief:    User interface of the whole project
@author:   Peng Cheng
           Hongliang Shen
           xi Zhang
@version:  0.1
@data:     2015/10/13 14:58
"""

import os
import sys

print "======================================================"
print "******** User inteface of using Quadrators ***********"
print "======================================================"
print "Press '1' and 'enter' to test: 1.py"
print "Press '2' and 'enter' to test: 2.py"
print "Press '3' and 'enter' to test: 3.py"
print "Press '4' and 'enter' to test: 4.py"
print "Press 'x' and 'enter' to quit!"
print "======================================================"

def func_1():
	os.system("python 1.py")

def func_2():
	os.system("python 2.py")

def func_3():
	os.system("python 3.py")

def func_4():
	os.system("python 4.py")

def func_exit():
	print "exit!"
	sys.exit(0)

f_list = {'1': func_1, '2': func_2, '3': func_3, '4': func_4, 'x': func_exit}

while True:
	try:
		'''input number!'''
		ch = raw_input()
		try:
			f_list.get(ch)()
		except Exception, e:
			print e, "\nPlease input number between 1~4!"
	except KeyboardInterrupt:
		break

