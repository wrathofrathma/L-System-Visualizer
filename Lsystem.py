def lgen(axioms, rules, it):
    '''
    Takes in an axiom set of rules and number of iterations and generates the new string
    '''
    
    for _ in range(it):
        newaxi=''
        for axiom in axioms:
            if axiom in rules:
                newaxi += rules[axiom]
            else:
                newaxi += axiom
        axioms = newaxi
    return axioms

rules = {"F":"F+F--F+F"}

print(lgen('F',rules,3))

def stackgen(rules):
    '''
    Takes in the generated string and makes it into a stack
    '''
    axi= lgen('F',rules,2)
    stack = []
    it=0
    for _ in range(len(axi)):
        stack.append(axi[it])
        it=it+1
    return stack

val = stackgen(rules)
print(val.pop())
