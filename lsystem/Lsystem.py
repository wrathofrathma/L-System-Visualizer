import threading
import random
import copy
import decimal

def pickProd(prods):
  prods_temp = copy.deepcopy(prods)
  rand = random.random() # generate a random number in [0,1]
  for i, prod in enumerate(prods_temp):
    if rand <= prod[0]:
      return prod[1]
    else:
      prods_temp[i+1][0]+=prod[0]

def stringParse(strings, prodRules):
  """
  NOTE: Context sensitive reads left to right, with longest key getting priority

  str_temp is the current string
  it will be used to keep track of what parts of the string still need proccessing
  Context free implimentation idea:
  1. sort the keys from longest to shortest
  2. say the key is length n, if the first n letters of the string match the key, add prod[key] to the new string
  3a.if the first n letters ever match a key remove the first n letters of the string
  3b.default rule: a letter goes to itself
  """
  newstr=""
  str_temp = copy.deepcopy(strings)
  while len(str_temp)>0:
    found = 0
    for key in sorted(prodRules, key=len, reverse=True):
      if key == str_temp[:len(key)]:
        newstr += pickProd(prodRules[key])
        str_temp = str_temp[len(key):]
        found = 1
        break;
    #default prod is a letter goes to itself
    if found == 0:
      newstr+=str_temp[0]
      str_temp=str_temp[1:]
  return newstr

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
      str1, str2 = strings[:int(len(strings)/2)], strings[int(len(strings)/2):]
      thread1 = threading.Thread(target=lambda x, arg1: x.put(stringParse(arg1), args=(newstr1,str1,prods)))
      thread2 = threading.Thread(target=lambda y, arg2: y.put(stringParse(arg2), args=(newstr2,str2,prods)))

      thread1.start()
      thread2.start()

      thread1.join()
      thread2.join()
      strings = newstr1.get() + newstr2.get()

    else:
      strings=stringParse(strings, prods)
  return strings


if __name__ == "__main__":
  list = [[.2,"X"],[.2,"Y"],[.6,"Z"]]
  print(pickProd(list))
