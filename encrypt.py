import sys
import math
import functools
from PIL import Image
from time import time
from random import randint

def setup():
	global txt, txtbytes, key, keybytes, n, img, imgMap
	# Text, key, and the respective ASCII integer lists
	txt = open(sys.argv[1],'r').read()
	txtbytes = [ord(x) for x in txt]
	key = sys.argv[2]
	keybytes = [ord(x) for x in key]
	# Side length of image has to be a power of 2 for Hilbert mapping
	n = 2**7
	# Output image
	img = Image.new('RGB', (n, n),'black')
	imgMap = img.load()

def encrypt():
	global txtbytes, l, w, h

	# Columnar Transposition Cipher

	# Pad message with random alphabet characters
	while len(txtbytes) < n*n: txtbytes.append(randint(97,122))
	# Useful constants
	l = n*n
	w = len(keybytes)
	h = math.ceil(l / w)
	# Write in txt values into an matrix as dictated by the cipher
	arr = [[txtbytes[w*x + y] if w*x + y < l else None for x in range(h)] for y in range(w)]
	# Sort key characters alphabetically and store respective row numbers
	keyMap = sorted([(keybytes[i], i) for i in range(w)])
	# Sort rows by keyMap order
	arrArranged = [arr[keyMap[i][1]] for i in range(w)]
	# Concatenate matrix into string and remove None values
	txtbytes = functools.reduce(lambda a, r: a + arrArranged[r], range(w), [])
	txtbytes = list(filter(None.__ne__, txtbytes))

	# Viginere Cipher
	txtbytes = [(txtbytes[i]+keybytes[i % w]) % 256 for i in range(l)]

def hilbert():
	global img

	# Map bytes to image using Hilbert mapping
	for d in range(l):
		x, y = d2xy(n,d)
		imgMap[x,y] = (txtbytes[d], txtbytes[d], txtbytes[d])
	# Use keysum to determine orientation of hilbert mapping
	keysum = sum(keybytes) if w > 0 else 0
	orient = keysum % 4
	# Orient image appropriately
	img = img.rotate(90*orient)
	# Save image as .png
	img.save('hilbert.png')

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

def main():
	time_start = time()
	setup()
	for i in range(len(key)):
		encrypt()
	hilbert()
	time_elapsed = time() - time_start
	print(str(round(time_elapsed, 6)) + ' seconds to encrypt')

if __name__ == '__main__':
	main()