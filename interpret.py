#####################################################################
#
# CAS CS 320, Fall 2015
# Midterm (skeleton code)
# interpret.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #2. ***************
#  ****************************************************************
#

exec(open('parse.py').read())

Node = dict
Leaf = str

def evalExpression(env, e):
    if type(e) == Leaf:
        if e == 'True':
            return 'True'
        if e == 'False':
            return 'False'
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == "Number":
                return children[0]
            elif label == "Plus":
                e1 = children[0]
                n1 = evalExpression(env, e1)
                e2 = children[1]
                n2 = evalExpression(env, e2)
                return v1 + v2
            elif label == "Variable":
                x = children[0]
                #if x in env:
                    return env[x]
                else:
                    print(x + " is unbounded.")
            elif label == "Element":
                x = evalExpression(env, children[0])
                n = evalExpression(env, children[1])

                return x[n]
        
def execProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return (env, [])
    elif type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                [e,p] = s[label]
                v = evalExpression(env, e)
                (env, o) = execProgram(env, p)
                return (env, [v] + o)
            if label == "Assign":
                x = children[0]["Variable"][0]
                n0 = evalExpression(env, children[1])
                n1 = evalExpression(env, children[2])
                n2 = evalExpression(env, children[3])
                p = children[4]
                env[x] = [n0, n1, n2]
                (env, o) = execProgram(env, p)
                return (env, o)
            elif label == "Loop":
                x = children[0]["Variable"][0]
                n = children[1]["Number"][0]
                p1 = children[2]
                p2 = children[3]
                if n > 0 or n = 0:
                    env[x] = n
                    (env2, o1) = execProgram(env, p1)
                    n = n-1
                    (env3, o2) = execProgram(env2, {"loop":[children[0], children[1], p1, p2])
                    return (env3, o1+o2)

                else:                   
                    (env2, o1) = execProgram(env, p2)                
                    
                    return (env2, o1)

def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s))
    return o

#eof
