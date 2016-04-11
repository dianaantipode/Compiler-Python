#####################################################################
#
# CAS CS 320, Fall 2015
# Midterm (skeleton code)
# validate.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #5. ***************
#  ****************************************************************
#

exec(open('analyze.py').read())
exec(open('interpret.py').read())
exec(open('compile.py').read())

def convertValue(v):
    if type(v) == Leaf:
        if v == 'True':
            return 1
        if v == "False":
            return 0
        pass # Complete for Problem #5.
    if type(v) == Node:
        return(v)

# Converts an output (a list of values) from the
# value representation to the machine representation
def convert(o):
    return [convertValue(v) for v in o]

def expressions(n):
    if n <= 0:
        []
    elif n == 1:
        return ['True', 'False'] # Add all base case(s) for Problem #5.
    else:
        es = expressions(n-1)
        esN = []
        esN += [{"Number": [1]}]
        esN += [{"Plus": [e1, e2]} for e1 in es for e2 in es]
        esN += [{"Variable": ['x']}]
        esN += [{"Element": [{"Variable": ['a']}, e]}for e in es]
        return es + esN

def programs(n):
    if n <= 0:
        []
    elif n == 1:
        return ["End"] # Add base case(s) for Problem #5.
    else:
        ps = programs(n-1)
        es = expressions(n-1)
        psN = []
        psN += [{"Assign": [{"Variable": ['a']}, e1, e2, e3, p]} for p in ps for e1 in es for e2 in es for e3 in es]
        psN += [{"Print": [e, p]} for e in es for p in ps]
        psN += [{"Loop":[{"Variable": ['x']}, {"Number": [1]}, p1, p2]} for p1 in ps for p2 in ps]

        pass # Add more nodes to psN for Problem #5.

        return ps + psN
   
# Compute the formula that defines correct behavior for the
# compiler for all program parse trees of depth at most k.
# Any outputs indicate that the behavior of the compiled
# program does not match the behavior of the interpreted
# program.

def exhaustive(k):
    for p in programs(k):
        try:
            if simulate(compileProgram({}, p)[1]) != convert(execProgram({}, p)[1]):
                print('\nIncorrect behavior on: ' + str(p))
        except:
            print('\nError on: ' + str(p))

#eof
