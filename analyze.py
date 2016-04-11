#####################################################################
#
# CAS CS 320, Fall 2015
# Midterm (skeleton code)
# analyze.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #3. ***************
#  ****************************************************************
#

exec(open('parse.py').read())

Node = dict
Leaf = str

def typeExpression(env, e):
    if type(e) == Leaf:
        if e == "True":
            return "TyBoolean"
        elif e == "False":
            return "TyBoolean"        
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                return 'TyNumber'

            elif label == 'Variable':
                x = children[0]
                value = env[x]
                return value
            
            elif label == 'Element':
                [xTree, e] = e[label]
                x = xTree["Variable"][0]
                if x in env and env[x] == "TyArray" and typeExpression(env, e) == "TyNumber":
                    return "TyNumber"               

            elif label == 'Plus':
                [e1, e2] = e[label]
                t1 = typeExpression(env, e1)
                t2 = typeExpression(env, e2)
                if e1 == "TyNumber" and e2 == "TyNumber":
                    return "TyNumber"

def typeProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return 'TyVoid'
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                [e, p] = s[label]
                t1 = typeExpression(env, e)
                t2 = typeExpression(env, p)
                if (t1 == "TyNumber" or t1 == "TyBoolean") and t2 == "TyVoid":
                    return "TyVoid"
            if label == 'Assign':
                [xTree, e0, e1, e2, p] = s[label]
                x = xTree['Variable'][0]
                t1 = typeExpression(env, e0)
                t2 = typeExpression(env, e1)
                t3 = typeExpression(env, e2)
                env[x] = "TyArray"
                t4 = typeProgram(env, p)
                if t1 == "TyNumber" and t2 == "TyNumber" and t3 == "TyNumber" and t4 == "TyVoid":
                    return "TyVoid"    
            if label == 'Loop':
                [xTree, nTree, p1, p2] = s[label]
                x = xTree['Variable'][0]
                n = nTree['Number'][0]
                t1 = typeExpression(env, nTree)
                env[x] = "TyNumber"
                t2 = typeProgram(env, p1)
                env[x] = "TyNumber"
                t3 = typeProgram(env, p2)
                if t1 == "TyNumber" and t2 == "TyVoid" and t3 =="TyVoid":
                    return "TyVoid"
                

#eof
