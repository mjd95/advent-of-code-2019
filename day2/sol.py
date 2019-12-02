from itertools import product

def solve():
    with open("input", "r") as f:
        orig_code = [int(el) for el in f.readline().split(",")]

    for (noun, verb) in product(range(1000), range(1000)):
        code = [c for c in orig_code]
        code[1] = noun
        code[2] = verb

        ins_ptr = 0
        while True:
            if code[ins_ptr] == 1:
                if code[ins_ptr+3] < len(code) and code[ins_ptr+2] < len(code) and code[ins_ptr+1] < len(code):
                    code[code[ins_ptr+3]] = code[code[ins_ptr+1]] + code[code[ins_ptr+2]]
                else:
                    break    
            elif code[ins_ptr] == 2:
                if code[ins_ptr+3] < len(code) and code[ins_ptr+2] < len(code) and code[ins_ptr+1] < len(code):
                    code[code[ins_ptr+3]] = code[code[ins_ptr+1]] * code[code[ins_ptr+2]]
                else:
                    break    
            elif code[ins_ptr] == 99:
                if code[0] == 19690720:
                    print(100*noun + verb)
                    return
                else:
                    break    
            ins_ptr += 4



if __name__ == "__main__":
    solve()