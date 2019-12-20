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

    def run(self):
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

def solve():
    with open("input", "r") as f:
       orig_code = [int(el) for el in f.readline().split(",")]
    for _ in range(10000):
        orig_code.append(0)

    code = [c for c in orig_code]
    machine = OpcodeMachine(code)
    machine.run()

    screen = []
    row = []
    for o in machine.outputs:
        if o==35:
            row.append("#")
        elif o==46:
            row.append('.')
        elif o==10:
            screen.append(row)
            row = []
        else:
            row.append("^")

    screen.pop(-1)

    for row in screen:
        print("".join(row))



    # ignore the intcode stuff and just find the path
    d = "L"
    path = ["L"]
    num_steps = 0
    pos = (20, 20)
    print(len(screen[0]), len(screen))
    print(len(screen[-1]))
    while True:
        # try to take a step
        did_step = False
        if d == "L":
            if in_bounds((pos[0]-1, pos[1]), screen) and screen[pos[1]][pos[0]-1]== "#":
                pos = (pos[0]-1, pos[1])
                did_step = True
        elif d == "R":
            if in_bounds((pos[0]+1, pos[1]), screen) and screen[pos[1]][pos[0]+1]== "#":
                pos = (pos[0]+1, pos[1])
                did_step = True
        elif d == "U":
            if in_bounds((pos[0], pos[1]-1), screen) and screen[pos[1]-1][pos[0]]== "#":
                pos = (pos[0], pos[1]-1)
                did_step = True
        elif d == "D":
            if in_bounds((pos[0], pos[1]+1), screen) and screen[pos[1]+1][pos[0]]== "#":
                pos = (pos[0], pos[1]+1)
                did_step = True
        if did_step:
            num_steps += 1
        else:
            path.append(str(num_steps))
            num_steps = 0
            did_turn = False
            if d == "L":
                if in_bounds((pos[0], pos[1]-1), screen) and screen[pos[1]-1][pos[0]] == "#":
                    path.append("R")
                    d = "U"
                    did_turn = True
                elif in_bounds((pos[0], pos[1]+1), screen) and screen[pos[1]+1][pos[0]] == "#":
                    path.append("L")
                    d = "D"
                    did_turn = True
            elif d == "R":
                if in_bounds((pos[0], pos[1]-1), screen) and screen[pos[1]-1][pos[0]] == "#":
                    path.append("L")
                    d = "U"
                    did_turn = True
                elif in_bounds((pos[0], pos[1]+1), screen) and screen[pos[1]+1][pos[0]] == "#":
                    path.append("R")
                    d = "D"
                    did_turn = True
            elif d == "U":
                if in_bounds((pos[0]-1, pos[1]), screen) and screen[pos[1]][pos[0]-1] == "#":
                    path.append("L")
                    d = "L"
                    did_turn = True
                elif in_bounds((pos[0]+1, pos[1]), screen) and screen[pos[1]][pos[0]+1] == "#":
                    path.append("R")
                    d = "R"
                    did_turn = True
            elif d == "D":
                if in_bounds((pos[0]-1, pos[1]), screen) and screen[pos[1]][pos[0]-1] == "#":
                    path.append("R")
                    d = "L"
                    did_turn = True
                elif in_bounds((pos[0]+1, pos[1]), screen) and screen[pos[1]][pos[0]+1] == "#":
                    path.append("L")
                    d = "R"
                    did_turn = True
            if not did_turn:
                break
    print(path)

    """
>>> all.replace('L,10,L,6,R,10', 'A').replace('R,6,R,8,R,8,L,6,R,8', 'B').replace('L,10,R,8,R,8,L,10', 'C')
'A,B,A,C,B,C,B,A,C,B'
    """
    code = [c for c in orig_code]
    code[0] = 2
    machine = OpcodeMachine(code)
    fn = [65, 44, 66, 44, 65, 44, 67, 44, 66, 44, 67, 44, 66, 44, 65, 44, 67, 44, 66, 10]
    fnA = [76, 44, 49, 48, 44, 76, 44, 54, 44, 82, 44, 49, 48, 10]
    fnB = [82, 44, 54, 44, 82, 44, 56, 44, 82, 44, 56, 44, 76, 44, 54, 44, 82, 44, 56, 10]
    fnC = [76, 44, 49, 48, 44, 82, 44, 56, 44, 82, 44, 56, 44, 76, 44, 49, 48, 10]
    machine.inputs = fn + fnA + fnB + fnC + [110,10]
    machine.outputs = []
    machine.run()
    print(machine.outputs)

def in_bounds(pos, screen):
    x_in = (pos[0]>=0 and pos[0]<len(screen[0]))
    y_in = (pos[1]>=0 and pos[1]<len(screen))
    return x_in and y_in

solve()