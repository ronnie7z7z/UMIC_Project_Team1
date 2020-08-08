## Image processing in first room for passcode generation
This currently contains the [passcode generator](./Passcode_generator.py) which reads the 5 images of detected paintings and uses a steganographic decoder function 
to extract the hidden image of letter. This is followed by using a CNN model to recognize the letter and forming anagrams of the 5 detected letters to generate a list 
of meaningful words from them.
