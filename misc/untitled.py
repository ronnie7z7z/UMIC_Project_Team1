
# 1ST CASE
# This code should be used when out image detection code
# is somewhat faulty and misses out few pictures(letters). So only 3 or 4
# ligitimate pictures are detected out of 5. for eg; Apple (ALE), Ronit (ONIT), ROTOR(RO)

def makewordrep(sample):
  #exactly 5 images have been recognized in which case it is assumed that they can directly be rearranged
  if len(sample)==5:
    return makeword(sample)
  
  #if 4 distinct letters are received then the 5th letter is taken as another alphabet and then tested for an existing word
  elif len(sample)==4:
      updated=[]
      for alphabet in list(string.ascii_lowercase):
        sample2=sample+alphabet
        sample2=''.join(sorted(sample2))
        pwd=makeword(sample2)
        for word in pwd:
          updated.append(word)
      return updated

#If 3 distinct letters are received then the 4th and 5th letters are taken as ONE OF THE alphabets and then tested for an existing word
  elif len(sample)==3:
            updated=[]
            for alpha in list(string.ascii_lowercase):
                  sample2 = sample + alphabet
                  sample2=''.join(sorted(sample2))
                  for beta in list(string.ascii_lowercase):
                        sample3 = sample2 + alphabet
                        sample3=''.join(sorted(sample3))
                        pwd=makeword(sample3)
            for word in pwd:
                  updated.append(word)
            return updated


# 2ND CASE
# This code should be used when our image detection code 
# works perfectly (captures every pic) and 4 or 3 letters
# only are detected. for eg; Apple(APLE), Rotor(ROT)


def makewordrep(sample):
      #exactly 5 images have been recognized in which case it is assumed that they can directly be rearranged
      if len(sample)==5:
            return makeword(sample)

      #if 4 distinct letters are received then the 5th letter is taken as ONE OF THE alphabets and then tested for an existing word
      elif len(sample)==4:
            updated=[]
            for alphabet in sample:
                  sample2 = sample + alphabet
                  sample2=''.join(sorted(sample2))
                  pwd=makeword(sample2)
            for word in pwd:
                    updated.append(word)
            return updated

      #If 3 distinct letters are received then the 4th and 5th letters are taken as ONE OF THE alphabets and then tested for an existing word
      elif len(sample)==3:
            updated=[]
            for alpha in sample:
                  sample2 = sample + alphabet
                  sample2=''.join(sorted(sample2))
                  for beta in sample:
                        sample3 = sample2 + alphabet
                        sample3=''.join(sorted(sample3))
                        pwd=makeword(sample3)
            for word in pwd:
                  updated.append(word)
            return updated

#RECURSIVE FUNCTIONS FOR THE ABOVE, NEEDED TESTING
      
# 1ST CASE
      
def makewordrep(sample, n):
      # Exactly 5 images have been recognized in which case it is assumed that they can directly be rearranged
      if n==5:
            return makeword(sample)
      # Sends the word with an additional ascii alphabet down in the loop 
      # increasing the n value by 1, until it reaches 5 and above statement is carried out
      else:
            for alphabet in list(string.ascii_lowercase):
                  samplex = sample + alphabet
                  samplex=''.join(sorted(samplex))
                  makewordrep(samplex, n+1)

# 2ND CASE

def makewordrep(sample, n):
      # Exactly 5 images have been recognized in which case it is assumed that they can directly be rearranged
      if n==5:
            return makeword(sample)
      # Sends the word with an additional word alphabet down in the loop 
      # increasing the n value by 1, until it reaches 5 and above statement is carried out
      else:
            for alphabet in sample:
                  samplex = sample + alphabet
                  samplex=''.join(sorted(samplex))
                  makewordrep(samplex, n+1)
                        

        
        
    
    
    
