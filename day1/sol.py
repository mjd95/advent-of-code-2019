def solve():
    with open("input", "r") as f:
        masses = [int(line.strip()) for line in f if line.strip()]

    total_fuel = 0
    for mass in masses:
        module_mass = mass/3 - 2
        if module_mass <= 0:
            continue

        total_fuel += module_mass
        cur = module_mass
        while True:
            cur = cur/3 - 2
            if cur<= 0:
                break
            total_fuel += cur

    print(total_fuel)    
        

if __name__=="__main__":
    solve()
