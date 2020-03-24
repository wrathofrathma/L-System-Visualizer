'''This file performs all of the parsing'''
import random
import copy
import multiprocessing
import textwrap


def nd_choice(prods):
    '''Randomly selects the rule in nondeterminism'''
    prods_temp = copy.deepcopy(prods)
    rand = random.random()  # generate a random number in [0,1]
    for i, prod in enumerate(prods_temp):
        if rand > prod[0]:
            prods_temp[i + 1][0] += prod[0]
        else:
            return prod[1]

def string_parse(strings, prod_rules):
    """
    NOTE: Context sensitive reads left to right, with longest key getting priority

    str_temp is the current string
    it will be used to keep track of what parts of the string still need proccessing
    Context free implimentation idea:
    1. sort the keys from longest to shortest
    2. say the key is length n, if the first n letters of the string match the key, 
    add prod[key] to the new string
    3a.if the first n letters ever match a key remove the first n letters of the string
    3b.default rule: a letter goes to itself
    """
    newstr = ""
    str_temp = copy.deepcopy(strings)
    while len(str_temp) > 0:
        found = 0
        for key in sorted(prod_rules, key=len, reverse=True):
            if key == str_temp[: len(key)]:
                newstr += nd_choice(prod_rules[key])
                str_temp = str_temp[len(key) :]
                found = 1
                break
        # default prod is a letter goes to itself
        if found == 0:
            newstr += str_temp[0]
            str_temp = str_temp[1:]
    return newstr


def parsed_thread(strings, prods, iters):
    """
    Takes in an axiom set of prods and number of iterations and generates the new string
    """
    if max(list(prods.keys())) == 1:
        context_free = 1
    else:
        context_free = 0
    count = 0
    while count < iters:

        if (len(strings) > 1) and context_free:
            strs = textwrap.wrap(strings, int(len(strings) / cpus) + 1)
            strings = ""
            tmp = []
            cpus = multiprocessing.cpu_count()
            for i in range(cpus - 1):
                tmp[i] = multiprocessing.Process(
                    target=lambda x, arg1: x.put(
                        string_parse(arg1), args=(newstr1, strs[i], prods)
                    )
                )
                tmp[i].start()
            for i in range(cpus - 1):
                tmp[i].join()
                strings += newstr1.get()
        else:
            strings = string_parse(strings, prods)
        count += 1
    return strings


if __name__ == "__main__":
    TEST = [[0.2, "X"], [0.2, "Y"], [0.6, "Z"]]
    print(nd_choice(TEST))
