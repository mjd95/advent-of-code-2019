from itertools import permutations


P = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

def run():
    p = P[:]
    ip = 0
    while True:
        cmd = p[ip]
        op = cmd % 100
        if op == 1:
            a1 = p[ip + 1] if cmd // 100 % 10 == 1 else p[p[ip + 1]]
            a2 = p[ip + 2] if cmd // 1000 % 10 == 1 else p[p[ip + 2]]
            p[p[ip + 3]] = a1 + a2
            ip += 4
        elif op == 2:
            a1 = p[ip + 1] if cmd // 100 % 10 == 1 else p[p[ip + 1]]
            a2 = p[ip + 2] if cmd // 1000 % 10 == 1 else p[p[ip + 2]]
            p[p[ip + 3]] = a1 * a2
            ip += 4
        elif op == 3:
            inpt = yield
            print("received input", inpt)
            p[p[ip+1]] = inpt
            ip += 2
        elif op == 4:
            outpt = p[p[ip+1]]
            print("emitting output", outpt)
            yield outpt
            ip += 2
        elif op == 5:
            a = p[ip + 1] if cmd // 100 % 10 == 1 else p[p[ip + 1]]
            if a != 0:
                ip = p[ip + 2] if cmd // 1000 % 10 == 1 else p[p[ip + 2]]
            else:
                ip += 3
        elif op == 6:
            a = p[ip + 1] if cmd // 100 % 10 == 1 else p[p[ip + 1]]
            if a == 0:
                ip = p[ip + 2] if cmd // 1000 % 10 == 1 else p[p[ip + 2]]
            else:
                ip += 3
        elif op == 7:
            a1 = p[ip + 1] if cmd // 100 % 10 == 1 else p[p[ip + 1]]
            a2 = p[ip + 2] if cmd // 1000 % 10 == 1 else p[p[ip + 2]]
            p[p[ip + 3]] = 1 if a1 < a2 else 0
            ip += 4
        elif op == 8:
            a1 = p[ip + 1] if cmd // 100 % 10 == 1 else p[p[ip + 1]]
            a2 = p[ip + 2] if cmd // 1000 % 10 == 1 else p[p[ip + 2]]
            p[p[ip + 3]] = 1 if a1 == a2 else 0
            ip += 4
        elif op == 99:
            break

x = [9,8,7,6,5]
gs = []
for phase in x:
    g = run()
    next(g)
    g.send(phase)
    gs.append(g)
signal = 0
while True:


    for g in gs:
        signal = g.send(signal)
        print("passing signal", signal)
    try:
        for g in gs:
            next(g)
    except StopIteration:
        break
print(signal)
