#alternative for detect()
import cv2

def prep():
  letters={}
  samples=[]
  for file in os.listdir('./mybot_ws(Project)/src/mybot_navigation/src/saved_images1'):
    image=cv2.imread(file)
    image=Image.fromarray(image)
    letter=recognize_letter(image)
    if not letters.get(letters[letter],0):
      letters[letter]=1
    else:
      letters[letter]+=1
  samples.append(''.join(sorted(list(letters.keys()))))
  letters1=letters
  avoided=[]
  for i in range(3):
    avoidable=[]
    #the three most infrequent letters (infrequent=less than 3 occurences)are taken one by one and a sample is constructed without it
    min_freq=min(list(letters1.values()))
    for letter in letters1:
      if letters1[letter]==min_freq and min_freq<3:
        avoidable.append(letter)
        avoided.append(letter)
        break
    letters1=list(set(letters1)-set(avoidable))
    samples.append(''.join(sorted(letters1)))
    letters2=letters1+list(set(avoided)-set(avoidable))
    samples.append(''.join(sorted(letters2)))