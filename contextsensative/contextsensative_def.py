def rul(rules):
    print("noncontext", rules)
    str = ''
    for rule in rules:
        if rules == 'F':
            str+='FpFF'
        else:
            str+= rules
    return str

def ctx(context, left = None, right = None):
    str = ''
    if left == 'FF' and context == 'FF' and right == 'FF':
        str+= 'FFFfffFFFFF'
    elif left == 'Fp' and context == 'FF':
        str += 'FpFF'
    elif context == 'FF' and right == 'FF':
        str+= 'FpFF'
    else:
        str += context
    return str

if __name__ == "__main__":
    print(rul('F+FF'))
    print(ctx("FF", right ="F"))
