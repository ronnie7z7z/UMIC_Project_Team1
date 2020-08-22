def makeword2(sample):
  if len(sample)==5:
    return makeword(sample)
    #exactly 5 images have been recognized in which case it is assumed that they can directly be rearranged
  else:
    if len(sample)==4:
      updated=[]
      for alphabet in list(string.ascii_lowercase):
        sample2=sample+alphabet
        sample2=''.join(sorted(sample2))
        pwd=makeword(sample2)
        for word in pwd:
          updated.append(word)
      return updated
    elif len(sample)==3:

      #if 4 distinct letters are received then the 5th letter is taken as another alphabet and then tested for an existing word