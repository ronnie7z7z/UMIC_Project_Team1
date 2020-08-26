#!/usr/bin/env python

import cv2 as cv
import numpy as np
import sys
import os
import torch
import torchvision
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
from PIL import Image
import nltk
nltk.download('words')
from nltk.corpus import wordnet as wn
from collections import Counter
from torch import nn
from torchvision import models


#Using GPU
if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'
torch.cuda.empty_cache()

lookup = dict()
reverselookup = dict()

count = 0

for j in os.listdir('./Alphabet_dataset/'):
    if not j.startswith('ges'):
        lookup[j] = count
        reverselookup[count] = j
        count += 1


model = models.resnet18(pretrained=True)
n_classes = 26
model.fc = nn.Sequential(
                      nn.Linear(512, 512), 
                      nn.ReLU(), 
                      nn.Linear(512, 512), 
                      nn.ReLU(),
                      nn.Dropout(0.3), 
                      nn.Linear(512, n_classes),                   
                      nn.LogSoftmax(dim=1))


model.load_state_dict(torch.load('./resnet18_weights.pt'))
device = torch.device("cpu")
model.to(device)
model.eval()

#print(model)

#model = torch.load('/content/full_resnet18.pth', map_location=torch.device('cpu'))


image_size = 128

def recognize_letter(img):    
    transform = transforms.Compose([
                transforms.Resize(size=image_size), 
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406],
                                     [0.229, 0.224, 0.225])  # Imagenet standards
                ])
    
    with torch.no_grad():
        img = transform(img)
        img = img.view(1, 3, image_size, image_size)
        #img = img.to(device)#Passing to GPU
        test_out = model(img.float())
        test_pred = torch.argmax(test_out, dim = 1, keepdim=True).numpy()

        test_pred = np.reshape(test_pred, test_pred.shape[0])
        print(reverselookup[test_pred[0]].lower(), end='')
        #print('\n')
        return str(reverselookup[test_pred[0]]).lower()


def decrypt(img): 

    # Encrypted image 
    #img = cv2.imread(filename)  
    width = img.shape[0] 
    height = img.shape[1] 
    
    # img1 and img2 are two blank images 
    img1 = np.zeros((width, height, 3), np.uint8) 
    img2 = np.zeros((width, height, 3), np.uint8) 

    for i in range(width): 

        for j in range(height): 

            for l in range(3): 

                v1 = format(img[i][j][l], '08b') 
                v2 = v1[:5] + '000'
                v3 = v1[5:] + '00000'
                #print('d', v1, v2, v3)

                # Appending data to img1 and img2 
                img1[i][j][l]= int(v2, 2) 
                img2[i][j][l]= int(v3, 2) 
      
    # These are two images produced from 
    # the encrypted image 
    cover = img1
    code = img2
    return code

def detect():
    letters={}
    samples=[]
    for file in os.listdir('/saved_images'):
        image=cv.imread(os.path.join('/saved_images',file))

        #cv.imshow('Image window', image)
        #cv.waitKey(100)
      
        #decrypted = decrypt(image)
        #image = Image.fromarray(decrypted)
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        #cv.imwrite('saved_images1/{}.png'.format(i+1), img)
        #img = cv.imread('saved_images1/{}.png'.format(i+1))
        ret,thresh = cv.threshold(image,20,255,cv.THRESH_BINARY)

        image = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)
        #cv.imshow('Image window', img)
        #cv.waitKey(1000)

        image = Image.fromarray(image)
        image = image.resize((128,128))
        #image.show()

        letter = recognize_letter(image)

        if not letters.get(letter,0):
            letters[letter]=1
        else:
            letters[letter]+=1
    print(letters)
    frequencies=sorted(list(letters.values()))
    mandatory=''
    for letter in list(letters.keys()):
      l=letters[letter]
      if l>=frequencies[-3]:
        mandatory=mandatory+letter
    for letter in list(letters.keys()):
      sample=mandatory+letter
      for letter2 in list(letters.keys()):
        sample=sample+letter2
        samples.append(sample)
        sample=sample[:-1]
    print(samples)
    return samples


def makeword(sample):
	words = nltk.corpus.words.words('en')

	anagrams = nltk.defaultdict(list)
	for word in words:
	    key = ''.join(sorted(word))
	    anagrams[key].append(word)
	passcodes = anagrams[sample]
	updated_passcodes = []
	for w in passcodes:
	    l = Counter([ss.pos() for ss in wn.synsets(w)])
	    if len(l) != 0:
	        updated_passcodes.append(w)
	return updated_passcodes

if __name__ == '__main__':
  detected = detect()
  passwords=[]
  for sample in detected:
    for sampleword in makeword(sample):
      passwords.append(sampleword+" \n")
  try:
    f=open('password.txt',"w")
    f.writelines(passwords)
    f.close()
  except:
    pass
    print("Possible passcodes- ", passwords)