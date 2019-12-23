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

def solve():
    with open("input", "r") as f:
       orig_code = [int(el) for el in f.readline().split(",")]
    for _ in range(1000):
        orig_code.append(0)

    machine = OpcodeMachine(orig_code)
    machine.process()
    outs = ""
    for a in machine.outputs:
        outs += chr(a)
    machine.outputs = []

    inpt = ""
    with open("code", "r") as f:
        inpt = f.read()
    inpt = list(inpt)

#    done = False
#    inpt = []
#    while not done:
#        t = input()
#        inpt += list(t) + ["\n"]
#        if t=="WALK" or t=="RUN":
#            done = True
#            break

    for i in range(len(inpt)):
        inpt[i] = ord(inpt[i])
    
    machine.inputs = inpt
    machine.process()
    print(machine.outputs)
    output = ""
    for a in machine.outputs:
        output += chr(a)
    print(output)

solve()