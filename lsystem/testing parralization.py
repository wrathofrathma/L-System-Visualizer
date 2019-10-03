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
    newaxi=''
    for axiom in axioms:
        if axiom in rules:
            newaxi += rules[axiom]
        else:
            newaxi += axiom
    que[0]+=newaxi

def lgen(axioms, rules, it):
    '''
    Takes in an axiom set of rules and number of iterations and generates the new string
    '''
    que = [axioms]
    for _ in range(it):
        if (len(axioms)>1):
            axi1,axi2 = que[0][:int(len(que[0])/2)], que[0][int(len(que[0])/2):]
            #if(len(axioms)%2==0):
            #    axi1,axi2 = axioms[:len(axioms)//2], axioms[:len(axioms)//2]
            #else:
            #    axi1,axi2 = axioms[:len(axioms)//2], axioms[:(len(axioms)//2)+1]


            thread1 = threading.Thread(target=axigenq, args=(axi1,rules,que))
            thread2 = threading.Thread(target=axigenq, args=(axi2,rules,que))



            thread1.start()
            thread2.start()


            thread1.join()
            thread2.join()


        else:
            axioms=axigen(axioms, rules)
    print(que[0])
    return que[0]

rules = {"F":"F+F--F+F"}
lgen("FFF", rules, 4)
