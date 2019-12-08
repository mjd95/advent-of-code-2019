from itertools import product, permutations
from queue import Queue
import threading

def read_opcode(opcode):
    num_prs = 0
    op = opcode%100
    if op==1 or op==2 or op==7 or op==8:
        num_prs=3
    elif op==3 or op==4:
        num_prs=1    
    elif op==5 or op==6:
        num_prs=2
    pr = [int(p) for p in str(opcode//100)[::-1]]
    if len(pr) < num_prs:
        zeros = [0] * (num_prs - len(pr))
        pr += zeros
    return op, pr

def read_mode(code, pr, mode):
    if mode==0:
        ret = code[code[pr]]
    elif mode==1:
        ret =  code[pr]
    else:
        print("rekt")
    return ret        


def process(code, inpts, ins_ptr):
    outs = []
    while True:
        op, modes = read_opcode(code[ins_ptr])
        if op == 1:
            # add
            code[code[ins_ptr+3]] = read_mode(code, ins_ptr+1, modes[0]) + read_mode(code, ins_ptr+2, modes[1])
            ins_ptr += 4
        elif op == 2:
            # multiply
            code[code[ins_ptr+3]] = read_mode(code, ins_ptr+1, modes[0]) * read_mode(code, ins_ptr+2, modes[1])
            ins_ptr += 4
        elif op == 3:
            # accept input
            if len(inpts) > 0:
                inpt = inpts.pop(0)
                code[code[ins_ptr+1]] = inpt    
                ins_ptr += 2
            else:
                return outs, ins_ptr, False
        elif op == 4:
            # emit output
            outs.append(read_mode(code, ins_ptr+1, modes[0]))
            ins_ptr += 2
        elif op == 5:
            # jump if true
            pr = read_mode(code, ins_ptr+1, modes[0])
            if pr != 0:
                ins_ptr = read_mode(code, ins_ptr+2, modes[1])
            else:
                ins_ptr += 3    
        elif op == 6:
            # jump if false
            pr = read_mode(code, ins_ptr+1, modes[0])
            if pr == 0:
                ins_ptr = read_mode(code, ins_ptr+2, modes[1])
            else:
                ins_ptr += 3    
        elif op == 7:
            # less than
            pr1 = read_mode(code, ins_ptr+1, modes[0])
            pr2 = read_mode(code, ins_ptr+2, modes[1])
            if pr1 < pr2:
                code[code[ins_ptr+3]] = 1
            else:
                code[code[ins_ptr+3]] = 0    
            ins_ptr += 4    
        elif op == 8:
            # equals     
            pr1 = read_mode(code, ins_ptr+1, modes[0])
            pr2 = read_mode(code, ins_ptr+2, modes[1])
            if pr1 == pr2:
                code[code[ins_ptr+3]] = 1
            else:
                code[code[ins_ptr+3]] = 0    
            ins_ptr += 4    
        elif op == 99:
            return outs, ins_ptr, True
    return outs, ins_ptr, True

def test():
    orig_code = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    perms = permutations([5,6,7,8,9])
    best = -1
    for phase_settings in perms:
        codes = [[c for c in orig_code] for i in range(5)]
        inpts = [[] for i in range(5)]
        for i in range(5):
            inpts[i].append(phase_settings[i])
        inpts[0].append(0)
        ins_ptrs = [0 for i in range(5)]
        all_done = False
        while not all_done:
            all_done = True
            for i in range(5):
                outs, ins_ptrs[i], done = process(codes[i], inpts[i], ins_ptrs[i])
                inpts[(i+1)%5] += outs
                all_done = done and all_done
        best = max(best, inpts[0][0])
    print(best)

def solve():
    with open("input", "r") as f:
        orig_code = [int(el) for el in f.readline().split(",")]
    perms = permutations([5,6,7,8,9])
    best = -1
    for phase_settings in perms:
        codes = [[c for c in orig_code] for i in range(5)]
        inpts = [[] for i in range(5)]
        for i in range(5):
            inpts[i].append(phase_settings[i])
        inpts[0].append(0)
        ins_ptrs = [0 for i in range(5)]
        all_done = False
        while not all_done:
            all_done = True
            for i in range(5):
                outs, ins_ptrs[i], done = process(codes[i], inpts[i], ins_ptrs[i])
                inpts[(i+1)%5] += outs
                all_done = done and all_done
        best = max(best, inpts[0][0])
    print(best)

if __name__ == "__main__":
   solve()