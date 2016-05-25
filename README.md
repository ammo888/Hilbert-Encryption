# Hilbert-Encryption
Minh Nguyen and Arjun Rajan
A CSC 490 Project for encrypting messages in a 2D grayscale image.

An ASCII txt file containing the message if first encrypted by columnar substitution with the key.
Then, the Vigenere cipher is applied with the same key.
Then, the encrypted bytes are written into a square image by Hilbert mapping and image is rotated appropriately (for 'extra' security).

For n = 2**8 = 256 (total of 65,536 bytes that can be encrypted): 34.128763 seconds to Hilbert encrypt

Higher values of n are not advised.
