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
                return outs, ins_ptr, relative_base, False
        elif op == 4:
            # emit output
            outs.append(read_mode(code, ins_ptr+1, modes[0], relative_base))
            ins_ptr += 2
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
            return outs, ins_ptr, relative_base, True
    return outs, ins_ptr, relative_base, True

def solve():
    with open("input", "r") as f:
        orig_code = [int(el) for el in f.readline().split(",")]
    orig_code[0] = 2
    for _ in range(1000):
        orig_code.append(0)

    score = 0
    joystick_pos = 0
    code = orig_code
    frame = 0
    while True:
        frame += 1
        ball_pos, paddle_pos = None, None
        screen = {}
        num_blocks = 0
        outs, ins, rel, done = process(code, [joystick_pos], 0, 0)
        for i in range(0, len(outs), 3):
            pos = (outs[i], outs[i+1])
            
            if pos == (-1, 0):
                score = outs[i+2]
            else:
                if outs[i+2] == 3:
                    paddle_pos = pos
                elif outs[i+2] == 4:
                    ball_pos = pos
                elif outs[i+2] == 2:
                    num_blocks += 1
                screen[pos] = outs[i+2]
            
        if num_blocks == 0:
            break    

        if frame%1000 == 0 :
            print_screen(screen)

        if paddle_pos[0] < ball_pos[0]:
            joystick_pos = -1
        elif paddle_pos[0] > ball_pos[0]:
            joystick_pos = 1
        else:
            joystick_pos = 0
    print(score)                

def print_screen(screen):
    minx, maxx = 0, 0
    miny, maxy = 0, 0
    for k, _ in screen.items():
        minx = min(minx, k[0])
        maxx = max(maxx, k[0])
        miny = min(miny, k[1])
        maxy = max(maxy, k[1])

    for y in range(miny, maxy+1):
        row = ''
        for x in range(minx, maxx+1):
            if not (x,y) in screen:
                row += ' '
            elif screen[(x,y)] == 2:
                row += '#'
            elif screen[(x,y)] == 1:
                row += '+'
            elif screen[(x,y)] == 0:
                row += ' '
            elif screen[(x,y)] == 3:
                row += '_'
            elif screen[(x,y)] == 4:
                row += 'O'
        print(row)

                


if __name__=="__main__":
    solve()