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
from nltk.corpus import wordnet as wn
from collections import Counter
import rospy
from std_msgs.msg import String
import time

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

model = torch.load('./full_resnet18.pth')

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
        img = img.to(device)#Passing to GPU
        test_out = model(img.float()).cpu()
        test_pred = torch.argmax(test_out, dim = 1, keepdim=True).cpu().numpy()
        test_pred = np.reshape(test_pred, test_pred.shape[0])
        #print(reverselookup[test_pred[0]].lower(), end='')
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

  letters = []
  for i in range(5):
      image = cv.imread('./images/encrypted' + str(i+1) + '.png')
      decrypted = decrypt(image) # to be hashed out ?
      image = Image.fromarray(decrypted) # to be hashed out ?
      #image = Image.fromarray(image) # possible ?
      letters.append(recognize_letter(image))
      
  sample = ''.join(sorted(letters))
  return sample


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
  passwords = makeword(detected)
  #print(passwords)
  #NEW UNCERTAIN CODE BELOW
  #assuming that passwords is a singleton set of possible passcodes
  rospy.init_node('pwd_generator',anonymous=True)
  sub=rospy.Subscriber("/validity_of_detection",String,cb)
  pub=rospy.Publisher("possible_passcode",String,queue_size=10)
  def cb(msg):
    if msg=='exit':
      print("exit sign detected, publishing password")
      pub.publish(passwords)
      time.sleep(10.0)
      os.system(' rosnode kill --all ')

    else:
      print('exit not detected or incorrectly detected before maze')
