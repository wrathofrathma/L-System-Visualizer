# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 08:31:25 2019

@author: Matt
"""

import threading




def axigen(axioms, rules):
    for axiom in axioms:
        newaxi=''
        if axiom in rules:
            newaxi += rules[axiom]
        else:
            newaxi += axiom
    axioms = newaxi
    return axioms

def axigenq(axioms, rules, que):
    print("hi")
    print(axioms)
    for axiom in axioms:
        print("SUO")
        print(axiom)
        newaxi=''
        if axiom in rules:
            newaxi += rules[axiom]
        else:
            newaxi += axiom
    print("JUST IN")
    print(newaxi)        
    axioms = newaxi
    que.append(axioms)

def lgen(axioms, rules, it):
    '''
    Takes in an axiom set of rules and number of iterations and generates the new string
    '''
    print(axioms)
    for _ in range(it):
        print(axioms)
        if (len(axioms)>1):
            axi1,axi2 = axioms[:len(axioms)//2], axioms[:len(axioms)//2]
            if(len(axioms)%2==0):
                axi1,axi2 = axioms[:len(axioms)//2], axioms[:len(axioms)//2]
            else:
                axi1,axi2 = axioms[:len(axioms)//2], axioms[:(len(axioms)//2)+1]
                
            print (axi1)
            print (axi2)
            que = []
            thread1 = threading.Thread(target=axigenq, args=(axi1,rules,que))
            thread2 = threading.Thread(target=axigenq, args=(axi2,rules,que))
        
            
            
            thread1.start()
            thread2.start()
            
            print(que)
            
            thread1.join()
            axi1=que.pop()
            print(axi1)
           
            thread2.join()
            axi2=que.pop()
            print(axi2)

            axioms = axi1+axi2
            print(axioms)
            
            
        else:
            axioms=axigen(axioms, rules)
            
        
    return axioms

rules = {"F":"F+F--F+F"}
lgen("FFF", rules, 3)




