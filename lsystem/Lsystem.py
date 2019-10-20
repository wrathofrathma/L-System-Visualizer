import threading
import random
import copy
random.seed()
def weightedrand(weights):
    #print("weights = ",weights)
    sums = 0
    numlist = []
    for weight in weights:
        sums = sums + weight

    if sums != 1:
        print("error")

    rand = random.randint(0,99)
    #print(rand)
    it = 0
    for weight in weights:
        wei = weight * 100
        num = int(wei)
        for i in range(num):
            numlist.append(it)

        it= it+1
    #print("numlist = ",numlist)
    #print(numlist)
    it= numlist[rand]
    #print(it)

    return it


def axigen(axioms, rules):
    newaxi=''
    strn = ""
    #print (rules)
    newrules = {}
    for i in rules.keys():
        #print("i = ",i)
        temp = rules[i]
        #print("temp = ",temp)
        #print(i)
        #print(rules[i])
        weights = []
        strn =""
        for it in temp:
            #print("ntemp = ",it)
            ntemp = it
            weights.append(ntemp[0])
            strn += ntemp[1]
            strn += "~"
        #print(strn)
        #print("weights in axigen = ",weights)
        strn = strn[:-1]
        #print(strn)
        newrules[i] = strn
        #print(nurules)
    #print("new rules = ",newrules)
    """
    str_temp is the current string
    it will be used to keep track of what parts of the string still need proccessing

    Context free implimentation idea:
    1. sort the keys from longest to shortest
    2. say the key is length n, if the first n letters of the string match the key, add rule[key] to the new string
    3a.if the first n letters ever match a key remove the first n letters of the string
    3b.default rule: a letter goes to itself
    """
    str_temp = copy.deepcopy(axioms)
    maxKeyLength = max(rules.keys())
    rules =copy.deepcopy(list(rules.keys()))
    #sort the keys from longest to shortest
    for j in range(len(rules)):
      m = j
      for i in range(j+1,len(rules)):
          if len(rules[m])<len(rules[i]):
              m = i
      temp = rules[j]
      rules[j]=rules[m]
      rules[m] = temp
    while len(str_temp)>0:
      found = 0
      for rule in rules:
          #print("rule = ",rule)
          if rule == str_temp[:len(rule)]:
              temp = newrules[rule]
              if '~' in temp:
                 ar = temp.split('~')
                 #print(ar)
                 rand=weightedrand(weights)
                 newaxi += ar[rand]
              else:
                newaxi+=temp
              #print("og string = ",str_temp)
              #print("temp = ",temp)
              #print("new axi = ",newaxi)
              str_temp =str_temp[len(rule):]
              #print("new string = ",str_temp)
              found = 1
              break;
      #default rule is a letter goes to itself
      if found == 0:
          newaxi+=str_temp[0]
          str_temp=str_temp[1:]
    """
    for axiom in axioms:
    #print(axiom)
    #print(axioms)
    #print(nurules)

    if axiom in nurules:
        temp = nurules[axiom]
        if '~' in temp:
           ar = temp.split('~')
           #print(ar)
           rand=weightedrand(weights)
           newaxi += ar[rand]
        else:
           newaxi += temp
    else:
        newaxi += axiom
    """
    axioms = newaxi

    return axioms

def axigenq(axioms, rules):

     #print("in axigenq")
     newaxi=''
     weights = []
     nurules = {}
     strn = ""
     #print (rules)

     for i in rules:
         weights = []
         strn= ""
         temp = rules[i]
         #print(i)
         #print(temp)
         for it in temp:
             ntemp = it
             weights.append(ntemp[0])
             strn += ntemp[1]
             strn += "~"
         #print(strn)
         strn = strn[:-1]
         #print(strn)
         #print(nurules)
         nurules[i] = strn


     for axiom in axioms[0]:
        if axiom in nurules:
            temp = nurules[axiom]
            if '~' in temp:
               ar = temp.split('~')
               rand=weightedrand(weights)
               #print(ar[rand])
               newaxi += ar[rand]
            else:
               newaxi += temp
        else:
            newaxi += axiom

     axioms[0] = newaxi

def lgen(axioms, rules, it):
    #print("rules = ",rules)
    '''
    Takes in an axiom set of rules and number of iterations and generates the new string
    '''
    if max(list(rules.keys()))==1:
        context_free = 1
    else:
        context_free=0
    for _ in range(it):

        if (len(axioms)>1) and context_free:
            axi1,axi2=[''],['']
            axi1[0],axi2[0] = axioms[:int(len(axioms)/2)], axioms[int(len(axioms)/2):]
            #if(len(axioms)%2==0):
             #   axi1,axi2 = axioms[:len(axioms)//2], axioms[:len(axioms)//2]
            #else:
             #   axi1,axi2 = axioms[:len(axioms)//2], axioms[:(len(axioms)//2)+1]


            thread1 = threading.Thread(target=axigenq, args=(axi1,rules))
            thread2 = threading.Thread(target=axigenq, args=(axi2,rules))



            thread1.start()
            thread2.start()


            thread1.join()
            thread2.join()
            axioms=axi1[0]+axi2[0]

        else:
            axioms=axigen(axioms, rules)
    print("string = ",axioms)
    return axioms

#rules = {}
#rules["F"]= [[.6,"F-f+"],[.4,"F-F"]]
#rules["H"]= [[.5,"H+h"],[.5,"H-H"]]
#print(rules)
#weights = [.4,.2,.4]
#print(lgen("FH", rules, 10))

'''
def stackgen(axi,rules, it):

    Takes in the generated string and makes it into a stack

    axi= lgen(axi,rules,it)
    stack = []
    it=0
    for _ in range(len(axi)):
        stack.append(axi[it])
        it=it+1
    return stack

if __name__ == "__main__":
    rules = {"F":"F+F--F+F"}
    print(lgen('F',rules,5))
    val = stackgen(rules)
    print(val.pop())
'''
