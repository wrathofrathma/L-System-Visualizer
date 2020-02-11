import rbnf.zero as ze
from rbnf.easy import build_parser


def con_sens(gram):
    str = ""
    for con in gram:
        if con == 'p':
            str += '+'
        elif con == 'm':
            str += '-'
        elif con == 'l':
            str += '['
        elif con == 'r':
            str += ']'
        else:
            str += str(con)
    return str



if __name__ == "__main__":
    ze_exp = ze.compile('import L-System-Visulizar/lsystem/contextsensative.[*]')
    parser = build_parser(ze_exp.lang, opt=True)
    #str = 'Fp{FF}'
    #print(str)
    #res = parser(str)
    #print(res.result)
    #fin = rbnf_to_lsys(res.result)
    #print(fin)

    #print("\n\n\n")

    #str = '{FF}FF'
    #print(str)
    #res = parser(str)
    #print(q)
    #print(res.result)
    #print(rbnf_to_lsys(res.result));

    #print("\n\n\n")

    #str = 'FF{FF}FF'
    #print(str)
    #res = parser(str)
    #print(res.result)
    #print(rbnf_to_lsys(res.result))
