import sys
import time
import os
import functools
import math
from random import randint
from PIL import Image


def setup():
	global txt, txtbytes, key, keybytes, n, img, imgMap
	txt = open(sys.argv[1],'r').read()
	txtbytes = txt.encode()
	key = sys.argv[2]
	keybytes = key.encode()
	n = 2**5
	img = Image.new('RGB', (n, n),'black')
	imgMap = img.load()

def encrypt():
	global txt, vig

	# Columnar Substitution Cipher
	while len(txt) < n*n:
		txt += chr(randint(97,122))
	l = len(txt)
	w = len(key)
	h = math.ceil(l / w)
	arr = [['' for x in range(w)] for y in range(h)]
	keyMap = sorted([(key[i], i) for i in range(len(key))])
	for i in range(h):
		for j in range (w):
			arr[i][j] = txt[w*i + j] if w*i + j < l else ''
	arrTranspose = list(zip(*arr))
	arrArranged = [arrTranspose[keyMap[i][1]] for i in range(w)]
	sub = ''.join([''.join(r) for r in arrArranged])

	# Viginere Cipher
	vig = bytearray()
	for i in range(len(sub)):
		k = ord(key[i % w])
		c = ord(sub[i].encode())
		b = (k+c) % 256
		vig.append(b)

def hilbert():
	keysum = sum(keybytes) if len(key) > 0 else 0
	orient = keysum % 4
	for d in range(len(vig)):
		x, y = d2xy(n,d)
		imgMap[x,y] = (vig[d], vig[d], vig[d])
	img.save('output.png')

def d2xy(n,d):
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
	if ry == 0:
		if rx == 1:
			x = n-1 - x
			y = n-1 - y
		x, y = y, x
	return x, y

setup()
encrypt()
hilbert()


