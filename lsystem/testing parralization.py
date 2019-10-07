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

def axigenq(axioms, rules):
    newaxi=''
    for axiom in axioms[0]:
        if axiom in rules:
            newaxi += rules[axiom]
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
            #    axi1,axi2 = axioms[:len(axioms)//2], axioms[:len(axioms)//2]
            #else:
            #    axi1,axi2 = axioms[:len(axioms)//2], axioms[:(len(axioms)//2)+1]


            thread1 = threading.Thread(target=axigenq, args=(axi1,rules))
            thread2 = threading.Thread(target=axigenq, args=(axi2,rules))



            thread1.start()
            thread2.start()


            thread1.join()
            thread2.join()
            axioms=axi1[0]+axi2[0]

        else:
            axioms=axigen(axioms, rules)
    print(axioms)
    return axioms

rules = {"F":"F+F--F+F"}
lgen("FFF", rules, 1)
lgen("FFF", rules, 2)