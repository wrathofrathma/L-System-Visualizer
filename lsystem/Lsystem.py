import threading
import random
import copy
random.seed()

def weightedrand(weights):
  numlist = []
  if sum(weights) != 1:
    print("Does not sum to 1")
  rand = random.randint(0,99)
  it = 0
  for weight in weights:
    wei = weight * 100
    num = int(wei)
    for i in range(num):
      numlist.append(it)

    it= it+1
  it= numlist[rand]
  return it


def stringParse(strings, prods):
  newstr=''
  strn = ""
  newprods = {}
  for i in prods.keys():
    temp = prods[i]
    weights = []
    strn =""
    for it in temp:
      ntemp = it
      weights.append(ntemp[0])
      strn += ntemp[1]
      strn += "~"
    strn = strn[:-1]
    newprods[i] = strn
  """
  str_temp is the current string
  it will be used to keep track of what parts of the string still need proccessing
  Context free implimentation idea:
  1. sort the keys from longest to shortest
  2. say the key is length n, if the first n letters of the string match the key, add rule[key] to the new string
  3a.if the first n letters ever match a key remove the first n letters of the string
  3b.default rule: a letter goes to itself
 """
  str_temp = copy.deepcopy(strings)
  maxKeyLength = max(prods.keys())
  prods =copy.deepcopy(list(prods.keys()))
  #sort the keys from longest to shortest
  for j in range(len(prods)):
    m = j
    for i in range(j+1,len(prods)):
      if len(prods[m])<len(prods[i]):
        m = i
    temp = prods[j]
    prods[j]=prods[m]
    prods[m] = temp
  while len(str_temp)>0:
    found = 0
    for rule in prods:
      if rule == str_temp[:len(rule)]:
        temp = newprods[rule]
        if '~' in temp:
          ar = temp.split('~')
          rand=weightedrand(weights)
          newstr += ar[rand]
        else:
          newstr+=temp
        str_temp = str_temp[len(rule):]
        found = 1
        break;
      #default rule is a letter goes to itself
    if found == 0:
      newstr+=str_temp[0]
      str_temp=str_temp[1:]
  return newstr

def multiStringParse(strings, prods):

  newstr=''
  weights = []
  newprods = {}
  strn = ""

  for i in prods:
    weights = []
    strn= ""
    temp = prods[i]
    for it in temp:
      ntemp = it
      weights.append(ntemp[0])
      strn += ntemp[1]
      strn += "~"
    strn = strn[:-1]
    newprods[i] = strn

  for char in strings[0]:
    if char in newprods:
      temp = newprods[char]
      if '~' in temp:
        ar = temp.split('~')
        rand=weightedrand(weights)
        newstr += ar[rand]
      else:
        newstr += temp
    else:
      newstr += axiom
  strings[0] = newstr

def lThread(strings, prods, it):
  '''
  Takes in an axiom set of prods and number of iterations and generates the new string
  '''
  if max(list(prods.keys()))==1:
    context_free = 1
  else:
    context_free=0
  for _ in range(it):
    if (len(strings)>1) and context_free:
      str1, str2 = [''], ['']
      str1[0], str2[0] = strings[:int(len(strings)/2)], strings[int(len(strings)/2):]

      thread1 = threading.Thread(target=multiStringParse, args=(str1,prods))
      thread2 = threading.Thread(target=multiStringParse, args=(str2,prods))

      thread1.start()
      thread2.start()

      thread1.join()
      thread2.join()
      strings=str1[0]+str2[0]

    else:
      strings=stringParse(strings, prods)
  return strings


if __name__ == "__main__":
  prods = {"F":"F+F--F+F"}
  print(lgen('F',prods,5))
  val = stackgen(prods)
  print(val.pop())
