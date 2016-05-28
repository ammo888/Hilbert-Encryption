# Hilbert-Encryption
Minh Nguyen and Arjun Rajan

A CSC 490 Project for encrypting messages in a 2D grayscale image.

An ASCII txt file containing the message if first encrypted by columnar transposition with the key.
Then, the Vigenere cipher is applied with the same key.
Then, the encrypted bytes are written into a square image by Hilbert mapping and image is rotated appropriately (for 'extra' security).

First, get python installed on your computer: https://www.python.org/downloads/release/python-350/
Then, install Pillow (image library): http://pillow.readthedocs.io/en/3.2.x/installation.html

For n = 2**7 = 256 (total of 65,536 bytes that can be encrypted): 34.128763 seconds to encrypt

Higher values of n are not advised.

Make sure txt file to encrypt is in the same folder as encrypt.py, decrypt.py.

To encrypt txt file: (output saved as hilbert.png)
```sh
$ python encrypt.py filename.txt key
```
To decrypt png file: (output saved as output.txt)
```sh
$ python decrypt.py hilbert.png key
```
