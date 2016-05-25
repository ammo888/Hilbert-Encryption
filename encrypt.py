import sys
from time import time
import math
from random import randint
from PIL import Image

def setup():
	global txt, txtbytes, key, keybytes, n, img, imgMap

	txt = open(sys.argv[1],'r').read()
	#txtbytes = txt.encode()
	key = sys.argv[2]
	keybytes = key.encode()
	# Length of image side has to be a power of 2 for hilbert mapping
	n = 2**5
	# Output image
	img = Image.new('RGB', (n, n),'black')
	imgMap = img.load()

def encrypt():
	global txt, vig

	# Columnar Substitution Cipher

	# Pad message with random alphabet characters
	while len(txt) < n*n:
		txt += chr(randint(97,122))
	# Useful Constants
	l = len(txt)
	w = len(key)
	h = math.ceil(l / w)
	# Write in txt values into an matrix as dictated by the cipher
	arr = [[txt[w*i + j] if w*i + j < l else '' for i in range(h)] for j in range(w)]
	# Sort rows by alphabetic order of key characters and store appropriate row number
	keyMap = sorted([(key[i], i) for i in range(w)])
	arrArranged = [arr[keyMap[i][1]] for i in range(w)]
	# Concatenate matrix into string
	sub = ''.join([''.join(r) for r in arrArranged])

	# Viginere Cipher

	vig = bytearray()
	for i in range(len(sub)):
		# Key character ASCII int
		k = ord(key[i % w])
		# Cipher character ASCII int
		c = ord(sub[i].encode())
		# Vigenere ASCII int
		b = (k+c) % 256
		# Add byte to array
		vig.append(b)

def hilbert():
	global img

	# Map bytes to image using Hilbert mapping
	for d in range(len(vig)):
		x, y = d2xy(n,d)
		imgMap[x,y] = (vig[d], vig[d], vig[d])
	# Use keysum to determine orientation of hilbert mapping
	keysum = sum(keybytes) if len(key) > 0 else 0
	orient = keysum % 4
	# Orient image appropriately
	img = img.rotate(90*orient)
	# Save image as .png
	img.save('encrypted.png')

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

time_start = time()
setup()
encrypt()
hilbert()
time_elapsed = time() - time_start
print(str(round(time_elapsed, 6)) + ' seconds to Hilbert encrypt')


