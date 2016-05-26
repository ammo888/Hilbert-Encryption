import sys
from time import time
import math
import functools
from PIL import Image

def setup():
	global imgMap, key, keybytes, w, n, l, txtbytes
	img = Image.open(sys.argv[1])
	key = sys.argv[2]
	keybytes = [ord(x) for x in key]
	w = len(key)
	n = img.size[0]
	l = n*n
	txtbytes = []

def dehilbert():
	global img, imgMap, txtbytes
	orient = (sum(keybytes) if w > 0 else 0) % 4
	img = img.rotate(-90*orient)
	imgMap = img.load()
	for d in range(l):
		x, y = d2xy(n, d)
		txtbytes.append(imgMap[x, y][0])

def decrypt():
	txtbytes = [(txtbytes[i]-keybytes[i%w]) % 256 for i in range(l)]


# d2xy and rot copied from Wikipedia
def d2xy(n,d):
	# R^1 -> R^2 Hilbert mapping
	x, y, t = 0, 0, d
	for s in range(0,n-1):
		rx = 1 & t // 2
		ry = 1 & t ^ rx
		x,y = rot(2**s,x,y,rx,ry)
		x += 2**s * rx
		y += 2**s * ry
		t = t // 4
	return x, y

def rot(n,x,y,rx,ry):
	# Hilbert mapping helper function
	if ry == 0:
		if rx == 1:
			x = n-1 - x
			y = n-1 - y
		x, y = y, x
	return x, y
