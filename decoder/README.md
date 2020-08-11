## Image processing in first room for passcode generation
This currently contains the [Passcode_generator](./Passcode_generator.py) which reads the 5 images of detected paintings and uses a steganographic decoder function 
to extract the hidden image of letter. This is followed by using a CNN model to recognize the letter and forming anagrams of the 5 detected letters to generate a list 
of meaningful words from them.

The [`Letter_recognizer.ipynb`](./Letter_recognizer.ipynb) contains the code for the CNN model which is trained on the [Alphabet_dataset](./Alphabet_dataset). The trained weights of the best model are saved in [`full_resnet18.pth`](./full_resnet18.pth) which are later used for prediction.

[Images](./images) contains certain sample cover images and their encrypted counterparts which encode a hidden letter image using steganography.

The [practice notebooks](./practice%20notebooks) folder contains certain trial notebooks with bits and pieces of code which were later integrated in Passcode_generator.

