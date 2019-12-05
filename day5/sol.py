from itertools import product

def read_opcode(opcode):
    num_prs = 0
    op = opcode%100
    if op==1 or op==2:
        num_prs=3
    elif op==3 or op==4:
        num_prs=1    
    pr = [int(p) for p in str(opcode/100)[::-1]]
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


def process(code, inpt):
    outs = []
    ins_ptr = 0
    while True:
        op, modes = read_opcode(code[ins_ptr])
        if op == 1:
            code[code[ins_ptr+3]] = read_mode(code, ins_ptr+1, modes[0]) + read_mode(code, ins_ptr+2, modes[1])
            ins_ptr += 4
        elif op == 2:
            code[code[ins_ptr+3]] = read_mode(code, ins_ptr+1, modes[0]) * read_mode(code, ins_ptr+2, modes[1])
            ins_ptr += 4
        elif op == 3:
            code[code[ins_ptr+1]] = inpt
            ins_ptr += 2
        elif op == 4:
            outs += [read_mode(code, ins_ptr+1, modes[0])]
            ins_ptr += 2
        elif op == 99:
            print("finished processsing code: ", outs, code)
            return 
    print("finished processing code: ", outs, code)        
    return 


def solve():
    with open("input", "r") as f:
        orig_code = [int(el) for el in f.readline().split(",")]
    print(len(orig_code))
    print(process(orig_code, 1))


if __name__ == "__main__":
    solve()