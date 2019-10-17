import threading
import random

random.seed()
def weightedrand(weights):
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
    #print(numlist)
    it= numlist[rand]    
    #print(it)
    return it
        


def axigen(axioms, rules):
     newaxi=''
     strn = ""
     print (rules)

     for i in rules:
         nurules = {}
         temp = rules[i]
         print(i)
         print(rules[i])
         for it in temp:
             weights = []
             ntemp = it
             weights.append(ntemp[0])
             strn += ntemp[1]
             strn += "~"
         print(strn)    
         strn = strn[:-1] 
         print(strn)
         nurules[i] = strn
         print(nurules)
             
     for axiom in axioms:
        print(axiom)
        print(axioms)
        print(nurules)
        
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

     axioms = newaxi   
     return axioms

def axigenq(axioms, rules):
     newaxi=''
     weights = []
     nurules = {}
     strn = ""
     #print (rules)

     for i in rules:
         weights = []
         strn= ""
         temp = rules[i]
         print(i)
         print(temp)
         for it in temp:
             ntemp = it
             weights.append(ntemp[0])
             strn += ntemp[1]
             strn += "~"
         print(strn)    
         strn = strn[:-1] 
         print(strn)
         nurules[i] = strn
         print(nurules)
    
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
    '''
    Takes in an axiom set of rules and number of iterations and generates the new string
    '''
    for _ in range(it):
   
        if (len(axioms)>1):
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
    
    return axioms

rules = {}
rules["F"]= [[.6,"F-f+"],[.4,"F-F"]]
rules["H"]= [[.5,"H+h"],[.5,"H-H"]]
print(rules)
#weights = [.4,.2,.4]
print(lgen("FH", rules, 10))

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