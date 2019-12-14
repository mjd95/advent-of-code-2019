with open("input", "r") as f:
    lines = [line.strip() for line in f if line.strip()]
lookup = {}    
for line in lines:
    ins, outs = line.split("=>")
    p = outs.strip().split(" ")
    outs = (int(p[0]), p[1])
    ins = ins.split(",")
    for i in range(len(ins)):
        p = ins[i].strip().split(" ")
        ins[i] = (int(p[0]), p[1])
    lookup[outs[1]] = [outs] + ins
# e.g. lookup{'FUEL': [(1, 'FUEL'), (7, 'A'), (1, 'E')]}    

def ore_amount(fuel_amount):
    required = {'FUEL': fuel_amount} # keeps track of requirements we've seen
    excesses = {}
    while True:
        # find something we are still required to produce
        amount, el = None, None
        for k, v in required.items():
            if k == 'ORE' or v == 0:
                continue
            else:
                el, amount = k, v
                break
        if el==None: break
        
        # take what we can from excesses 
        if k in excesses:
            amount -= min(excesses[k], amount)
            excesses[k] -= min(excesses[k], amount)
        
        if amount > 0:
            # still require some more, so do a reaction
            react_from(required, excesses, el, amount)
        del required[el]

    return required['ORE']
 
def react_from(required, excesses, el, amount):
    d = lookup[el]
    m = amount//d[0][0] if amount%d[0][0]==0 else amount//d[0][0] + 1
    for i in range(1, len(d)):
        if d[i][1] in required:
            required[d[i][1]] += d[i][0]*m
        else:
            required[d[i][1]] = d[i][0]*m
    if d[0][0] in excesses:
        excesses[d[0][1]] += d[0][0]*m-amount
    else:
        excesses[d[0][1]] = d[0][0]*m-amount

target = 1000000000000
low, low_ore = 1000000, 844444850768
high, high_ore = 1250000, 1055555903122
while low < high:
    print(f"low_fuel={low}, low_ore={low_ore}")
    print(f"high_fuel={high}, high_ore={high_ore}")
    mid = (low+high)//2
    mid_ore = ore_amount(mid)
    if (target-low_ore) < (high_ore-target):
        high, high_ore = mid, mid_ore
    else:
        low, low_ore = mid, mid_ore
