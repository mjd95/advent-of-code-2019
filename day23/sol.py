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


    machines = []
    input_queues = []
    idles = []
    for i in range(50):
        # create the machine of address i
        machines.append(OpcodeMachine([c for c in orig_code]))
        input_queues.append([i])
        idles.append(False)

    nat_x, nat_y = None, None
    i = 0
    while True:
        inpts = input_queues[i%50]
        input_queues[i%50] = []

        idle = False
        if len(inpts)==0:
            idle = True
            inpts = [-1]

        machines[i%50].inputs = inpts
        machines[i%50].process()
        outs = machines[i%50].outputs

        if len(outs)==0:
            idle = idle and True
        idles[i%50] = idle

        machines[i%50].outputs = []

        for j in range(0, len(outs), 3):
            if outs[j]==255:
                nat_x, nat_y = outs[j+1], outs[j+2]
            else:
                input_queues[outs[j]].append(outs[j+1])
                input_queues[outs[j]].append(outs[j+2])

        # check if everything is idle
        if i%50==0:
            all_idle = True
            for b in idles:
                all_idle = all_idle and b
            if all_idle:
                print(f"all are idle, sending {nat_x}, {nat_y}")
                input_queues[0].append(nat_x)
                input_queues[0].append(nat_y)

        i += 1


solve()