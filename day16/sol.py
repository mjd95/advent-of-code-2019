from math import gcd
from itertools import repeat

num_phases = 100
base_pattern = [0, 1, 0, -1]

def find_needed(offset, len_inpt):
    needed = [0 for i in range(len_inpt)]
    for i in range(offset+1, offset+9):
        needed[i] = 1
    phase = num_phases
    while phase > 0:
        i = 0
        out_pos = 1
        new_needed = [0 for i in range(len_inpt)]
        while out_pos < len_inpt+1:
            if needed[out_pos-1] == 1:
                for i in range(0, len_inpt):
                    if base_pattern[((i+1)//out_pos)%len(base_pattern)] != 0:
                        new_needed[i] = 1
            out_pos += 1
        needed = new_needed
        phase -= 1
    return needed

def solve():
    base_inpt = [int(i) for i in list("59790132880344516900093091154955597199863490073342910249565395038806135885706290664499164028251508292041959926849162473699550018653393834944216172810195882161876866188294352485183178740261279280213486011018791012560046012995409807741782162189252951939029564062935408459914894373210511494699108265315264830173403743547300700976944780004513514866386570658448247527151658945604790687693036691590606045331434271899594734825392560698221510565391059565109571638751133487824774572142934078485772422422132834305704887084146829228294925039109858598295988853017494057928948890390543290199918610303090142501490713145935617325806587528883833726972378426243439037")]
#    base_inpt = [int(i) for i in list("03081770884921959731165446850517")]
    repeats = 10000
    len_inpt = len(base_inpt)*repeats
    target = 5979013
    message_len = 8
    num_phases = 100

    inpt = []
    for i in range(len_inpt):
        inpt.append(base_inpt[i%len(base_inpt)])

    phase = 0
    while phase < num_phases:
        outdigits = [0 for i in range(len_inpt)]
        out_pos = len_inpt-1
        s = 0
        while out_pos >= target:
            s += inpt[out_pos%len(inpt)]
            outdigits[out_pos] = abs(s)%10
            out_pos -= 1

        phase += 1
        inpt = outdigits
        print(f"completed phase={phase}")
    print(''.join([str(i) for i in inpt[target:target+message_len]]))

solve()