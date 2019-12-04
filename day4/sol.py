def add(el, di):
    if el in di:
        di[el] += 1
    else:
        di[el] = 1    

def is_valid(n):
    counts = {}
    for i in range(len(n)-1):
        if int(n[i]) > int(n[i+1]):
            return False
        add(int(n[i]), counts)
    add(int(n[-1]), counts)    

    for val in counts.values():
        if val == 2:
            return True
    return False

def test():
    print(is_valid(str(112233)))
    print(is_valid(str(123444)))
    print(is_valid(str(111122)))

def solve():
    tot = 0
    for n in range(240920,789857+1):
        if is_valid(str(n)):
            tot += 1
    print(tot)

if __name__=="__main__":
    solve()