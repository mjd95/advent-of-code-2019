from random import randint
import sys
sys.setrecursionlimit(50000)
from itertools import product

class OpcodeMachine:
    code = []
    ins_ptr = 0
    relative_base = 0
    halted = False
    inputs = []
    outputs = []

    def __init__(self, code):
        self.code = code
        self.ins_ptr = 0
        self.relative_base = 0
        self.halted = False
        self.inputs = []
        self.outputs = []

    def read_opcode(self, opcode):
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

    def read_mode(self, pos, mode):
        if mode==0:
            ret = self.code[self.code[pos]]
        elif mode==1:
            ret = self.code[pos]
        elif mode==2:
            ret = self.code[self.relative_base+self.code[pos]]    
        return ret        

    def pos_mode(self, pos, mode):
        if mode==0:
            pos = self.code[pos]
        elif mode==1:
            pos = pos
        elif mode==2:
            pos = self.relative_base + self.code[pos]
        return pos

    def process(self):
        while not self.halted:
            op, modes = self.read_opcode(self.code[self.ins_ptr])
            if op == 1:
                # add
                self.code[self.pos_mode(self.ins_ptr+3, modes[2])] = self.read_mode(self.ins_ptr+1, modes[0]) + self.read_mode(self.ins_ptr+2, modes[1])
                self.ins_ptr += 4
            elif op == 2:
                # multiply
                self.code[self.pos_mode(self.ins_ptr+3, modes[2])] = self.read_mode(self.ins_ptr+1, modes[0]) * self.read_mode(self.ins_ptr+2, modes[1])
                self.ins_ptr += 4
            elif op == 3:
                # accept input
                if len(self.inputs) > 0:
                    inpt = self.inputs.pop(0)
                    self.code[self.pos_mode(self.ins_ptr+1, modes[0])] = inpt    
                    self.ins_ptr += 2
                else:
                    return
            elif op == 4:
                # emit output
                self.outputs.append(self.read_mode(self.ins_ptr+1, modes[0]))
                self.ins_ptr += 2
            elif op == 5:
                # jump if true
                pr = self.read_mode(self.ins_ptr+1, modes[0])
                if pr != 0:
                    self.ins_ptr = self.read_mode(self.ins_ptr+2, modes[1])
                else:
                    self.ins_ptr += 3
            elif op == 6:
                # jump if false
                pr = self.read_mode(self.ins_ptr+1, modes[0])
                if pr == 0:
                    self.ins_ptr = self.read_mode(self.ins_ptr+2, modes[1])
                else:
                    self.ins_ptr += 3    
            elif op == 7:
                # less than
                pr1 = self.read_mode(self.ins_ptr+1, modes[0])
                pr2 = self.read_mode(self.ins_ptr+2, modes[1])
                if pr1 < pr2:
                    self.code[self.pos_mode(self.ins_ptr+3, modes[2])] = 1
                else:
                    self.code[self.pos_mode(self.ins_ptr+3, modes[2])] = 0    
                self.ins_ptr += 4    
            elif op == 8:
                # equals     
                pr1 = self.read_mode(self.ins_ptr+1, modes[0])
                pr2 = self.read_mode(self.ins_ptr+2, modes[1])
                if pr1 == pr2:
                    self.code[self.pos_mode(self.ins_ptr+3, modes[2])] = 1
                else:
                    self.code[self.pos_mode(self.ins_ptr+3, modes[2])] = 0
                self.ins_ptr += 4    
            elif op == 9:
                # shift relative base
                pr1 = self.read_mode(self.ins_ptr+1, modes[0])
                self.relative_base += pr1
                self.ins_ptr += 2
            elif op == 99:
                self.halted = True
                return
        self.halted = True
        return

def visit_from(walker, machine, dpath):
    walker.path.append(walker.pos)
    if walker.dist > walker.max_dist:
        walker.max_dist = max(walker.dist, walker.max_dist)
        print(f"at {walker.pos}, distance from start is {walker.dist}")

    backtracks = []
    for d in range(1, 5):
        if d == 1:
            new_pos = (walker.pos[0], walker.pos[1]-1)
        elif d == 2:
            new_pos = (walker.pos[0], walker.pos[1]+1)
        elif d == 3:
            new_pos = (walker.pos[0]-1, walker.pos[1])
        elif d == 4:
            new_pos = (walker.pos[0]+1, walker.pos[1])

        if new_pos in walker.path:
            if new_pos not in walker.fully_explored:
                backtracks.append(new_pos)
            continue

        machine.inputs.append(d)
        machine.process()
        out = machine.outputs.pop(0)

        if out == 0:
            # don't count this one; we could have got an equivalent path without hitting the wall
            pass
        elif out == 1:
            walker.dist += 1
            walker.pos = new_pos
            dpath.append(d)
            visit_from(walker, machine, dpath)
        elif out == 2:
            # this shouldn't happen
            dpath.append(d)
            walker.pos = new_pos
            print(f"got back to the oxygen tank")
            return
    
    walker.fully_explored[walker.pos] = True
    
    i = -2
    while walker.pos in walker.fully_explored:
        new_pos = backtracks.pop(0)
        d = get_direction_for(walker.pos, new_pos)
        machine.inputs.append(d)
        machine.process()
        out = machine.outputs.pop(0)
        walker.pos = new_pos
        if out != 1:
            print(f"out={out}")
        i -= 1
        walker.dist -= 1
    visit_from(walker, machine, dpath)
    
def get_direction_for(a, b):
    if a[0] == b[0]:
        if a[1] == b[1]+1:
            return 1
        elif a[1] == b[1]-1:
            return 2
        else:
            print("emmm")
    elif a[1] == b[1]:
        if a[0] == b[0]+1:
            return 3
        elif a[0] == b[0]-1:
            return 4
        else:
            print("emmm")
    else:
        print("emmmm")


class Walker:
    def __init__(self, pos):
        self.path = []
        self.pos = pos
        self.fully_explored = {}
        self.dist = 0
        self.max_dist = 0

def solve():
    with open("input", "r") as f:
       orig_code = [int(el) for el in f.readline().split(",")]
    for _ in range(1000):
        orig_code.append(0)

    tpath = [2, 2, 2, 2, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 4, 4, 2, 2, 3, 3, 3, 3, 2, 2, 4, 4, 4, 4, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 4, 4, 2, 2, 3, 3, 2, 2, 2, 2, 4, 4, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2, 4, 4, 1, 1, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 2, 2, 4, 4, 1, 1, 1, 1, 1, 1, 3, 3, 2, 2, 3, 3, 1, 1, 1, 1, 4, 4, 1, 1, 1, 1, 3, 3, 2, 2, 3, 3, 1, 1, 1, 1, 3, 3, 3, 3, 1, 1, 3, 3, 1, 1, 4, 4, 1, 1, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 2, 2, 3, 3, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 2, 2, 4, 4, 2, 2, 3, 3]

    longest_path_len = 0
    while True:
        walker = Walker((0, 0))
        code = [c for c in orig_code]
        machine = OpcodeMachine(code)

        # walk to the target
        machine.inputs = [t for t in tpath]
        machine.process()
        machine.outputs = []

        # try and walk far from the target
        dpath = []
        visit_from(walker, machine, dpath)
        outs = machine.outputs
        
        while 0 in outs:
            idx = outs.index(0)
            outs.pop(idx)
            dpath.pop(idx)
        
        if len(dpath) > longest_path_len:
            longest_path_len = len(dpath)
            print(f"new longest path.  {287+len(dpath)}.  {dpath}")

def print_screen(walker):
    m = 50
    screen = [[' ' for _ in range(2*m)] for _ in range(2*m)]
    for wall, _ in walker.wall_locs.items():
        screen[m+wall[1]][m+wall[0]] = '#'
    for p in walker.path:
        screen[m+p[1]][m+p[0]] = '.'
    screen[m+walker.pos[1]][m+walker.pos[0]] = '.'
    screen[m][m] = 'S'
    if len(walker.target) > 0: screen[m+walker.target[1]][m+walker.target[0]] = 'O'
    for row in screen:
        print(''.join(row))


solve()