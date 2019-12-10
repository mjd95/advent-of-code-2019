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

def read_mode(code, pos, mode, relative_base):
    if mode==0:
        ret = code[code[pos]]
    elif mode==1:
        ret = code[pos]
    elif mode==2:
        ret = code[relative_base+code[pos]]    
    else:
        print("rekt")
    return ret        

def pos_mode(code, pos, mode, relative_base):
    if mode==0:
        pos = code[pos]
    elif mode==1:
        pos = pos
    elif mode==2:
        pos = relative_base + code[pos]
    else:
        print("rekt")
    return pos


def process(code, inpts, ins_ptr, relative_base):
    outs = []
    while True:
        op, modes = read_opcode(code[ins_ptr])
        if op == 1:
            # add
            code[pos_mode(code, ins_ptr+3, modes[2], relative_base)] = read_mode(code, ins_ptr+1, modes[0], relative_base) + read_mode(code, ins_ptr+2, modes[1], relative_base)
            ins_ptr += 4
        elif op == 2:
            # multiply
            code[pos_mode(code, ins_ptr+3, modes[2], relative_base)] = read_mode(code, ins_ptr+1, modes[0], relative_base) * read_mode(code, ins_ptr+2, modes[1], relative_base)
            ins_ptr += 4
        elif op == 3:
            # accept input
            if len(inpts) > 0:
                inpt = inpts.pop(0)
                code[pos_mode(code, ins_ptr+1, modes[0], relative_base)] = inpt    
                ins_ptr += 2
            else:
                print("expected an input")
        elif op == 4:
            # emit output
            outs.append(read_mode(code, ins_ptr+1, modes[0], relative_base))
            ins_ptr += 2
            return outs, False, ins_ptr, relative_base
        elif op == 5:
            # jump if true
            pr = read_mode(code, ins_ptr+1, modes[0], relative_base)
            if pr != 0:
                ins_ptr = read_mode(code, ins_ptr+2, modes[1], relative_base)
            else:
                ins_ptr += 3
        elif op == 6:
            # jump if false
            pr = read_mode(code, ins_ptr+1, modes[0], relative_base)
            if pr == 0:
                ins_ptr = read_mode(code, ins_ptr+2, modes[1], relative_base)
            else:
                ins_ptr += 3    
        elif op == 7:
            # less than
            pr1 = read_mode(code, ins_ptr+1, modes[0], relative_base)
            pr2 = read_mode(code, ins_ptr+2, modes[1], relative_base)
            if pr1 < pr2:
                code[pos_mode(code, ins_ptr+3, modes[2], relative_base)] = 1
            else:
                code[pos_mode(code, ins_ptr+3, modes[2], relative_base)] = 0    
            ins_ptr += 4    
        elif op == 8:
            # equals     
            pr1 = read_mode(code, ins_ptr+1, modes[0], relative_base)
            pr2 = read_mode(code, ins_ptr+2, modes[1], relative_base)
            if pr1 == pr2:
                code[pos_mode(code, ins_ptr+3, modes[2], relative_base)] = 1
            else:
                code[pos_mode(code, ins_ptr+3, modes[2], relative_base)] = 0
            ins_ptr += 4    
        elif op == 9:
            # shift relative base
            pr1 = read_mode(code, ins_ptr+1, modes[0], relative_base)
            relative_base += pr1
            ins_ptr += 2
        elif op == 99:
            return outs, True, ins_ptr, relative_base
    return outs, True, ins_ptr, relative_base

def solve():
    with open("input", "r") as f:
       orig_code = [int(el) for el in f.readline().split(",")]
    for _ in range(1000):
        orig_code.append(0)
    done = False
    ins_ptr, rel_base = 0, 0
    ins = [1]
    painted = {}
    pos = (0,0)
    dr_pos = 0
    drs = ['N', 'E', 'S', 'W']
    while True:
        outs, done, ins_ptr, rel_base = process(orig_code, ins, ins_ptr, rel_base)
        if done: break
        painted[pos] = outs[0]
        ins = outs

        outs, done, ins_ptr, rel_base = process(orig_code, ins, ins_ptr, rel_base)
        if done: break
        turn_dr = outs[0]
        if turn_dr == 0:
            dr_pos = (dr_pos-1)%4
        elif turn_dr == 1:
            dr_pos = (dr_pos+1)%4
        
        # advance
        if drs[dr_pos] == 'N':
            pos = (pos[0], pos[1] + 1)
        elif drs[dr_pos] == 'E':
            pos = (pos[0]+1, pos[1])
        elif drs[dr_pos] == 'S':
            pos = (pos[0], pos[1] - 1)
        elif drs[dr_pos] == 'W':
            pos = (pos[0]-1, pos[1])

        # find new input
        inpt = painted[pos] if pos in painted else 0        
        ins = [inpt]
    
    # draw the output
    arr = [['.' for _ in range(100)] for _ in range(100)]
    for k, v in painted.items():
        if v == 1:
            arr[50-k[1]][50+k[0]] = '#'

    for i in range(100):
        print(''.join(arr[i]))


if __name__=="__main__":
    solve()