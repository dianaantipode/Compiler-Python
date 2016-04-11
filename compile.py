#####################################################################
#
# CAS CS 320, Fall 2015
# Midterm (skeleton code)
# compile.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #4. ***************
#  ****************************************************************
#

from random import randint
exec(open('analyze.py').read())
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('optimize.py').read())
exec(open('machine.py').read())

Leaf = str
Node = dict

def freshStr():
    return str(randint(0,10000000))

def compileExpression(env, e, heap):
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                n = children[0]
                heap = heap + 1
                return (['set ' + str(heap) + ' ' + str(n)], heap, heap)
            elif label == "Plus":
                (inst1, addr1, heap1) = compileExpression(env, children[0], heap)
                (inst2, addr2, heap2) = compileExpression(env, children[1], heap1)
                heapPlus = heap2 + 1
                instPlus = \
                      copy(addr1, 1) + \
                      copy(addr2, 2) + [\
                          "add"] + \
                          copy(0, heapPlus)
                return (inst1 + inst2 + instPlus, heapPlus, heapPlus)
            elif label == "Element":
                (instx, addrx, heapx) = compileExpression(env, children[0], heap)
                (inst1, addr1, heap1) = compileExpression(env, children[1], heapx)
                heapVal = heapx + 1
                instElement = \
                         copy(addr1, 1) + [\
                             "set 2 " + str(addrx),\
                             "add"] + \
                             copy(0,3) + [\
                             "set 4 " + str(heapVal), \
                             "copy"]
                return (instx + inst1 + instElement, heapVal, heapVal)
            elif label == "Variable":
                x = children[0]
                if x in env:
                    return ([], env[x], heap)
                else:
                    print(x+ " is unbounded.")
                    
    if type(e) == Leaf:
        if e == "True":
            heap += 1
            return(['set '+str(heap)+' 1'],heap,heap)
        if e == "False":
            heap += 1
            return(['set '+str(heap)+' 0'],heap,heap)

    pass # Complete 'True', 'False', 'Variable', 'Element', and 'Plus' cases for Problem #4.

def compileProgram(env, s, heap = 8): # Set initial heap default address.
    if type(s) == Leaf:
        if s == 'End':
            return (env, [], heap)

    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                [e, p] = children
                (inste, addr, heap) = compileExpression(env, e, heap)
                (env, instp, heap) = compileProgram(env, p, heap)
                return (env, inste + copy(addr, 5) + instp, heap)
            elif label == "Assign":
                x = children[0]["Variable"][0]
                heapStart = heap + 1
                heapEnd = heapStart + 3
                (inst1, addr1, heap1) = compileExpression(env, children[1], heapEnd)
                (inst2, addr2, heap2) = compileExpression(env, children[2], heap1)
                (inst3, addr3, heap3) = compileExpression(env, children[3], heap2)
                p = children[4]
                env[x] = heapStart
                instAssign = copy(addr1, heapStart) + \
                             copy(addr2, heapStart + 1) +\
                             copy(addr3, heapStart + 2)
                (envp, instp, heapp) = compileProgram(env, p, heap3)
                return (envp, inst1 + inst2 + inst3 + instAssign + instp, heapp)
            elif label == "Loop":
                x = children[0]["Variable"][0]
                inst = ["label loopStart"]
                (instN, addrN, heapN) = compileExpression(env, children[1], heap)
                inst.append(instN)
                inst.append(["brach LoopEnd"])
                (envP1, instP1, heapP1) = compileProgram(env, children[2], heapN)
                inst.append(instP1)

                inst.append(["goto LoopStart"])
                inst.append(["label LoopEnd"])
                (envP2, instP2, heapP2) = compileProgram(envP1, children[3], heapP1)
                return (envP2, inst, heapN)


def compile(s):
    p = tokenizeAndParse(s)
    if not typeProgram({}, p) is None:
        o = foldConstant(p)
        o = eliminateDeadCode(o)

        (env, insts, heap) = compileProgram({}, p)
        return insts

def compileAndSimulate(s):
    return simulate(compile(s))

#eof
