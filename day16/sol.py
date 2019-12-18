from math import gcd
from itertools import repeat

def solve():
    inpt = [int(i) for i in list("59790132880344516900093091154955597199863490073342910249565395038806135885706290664499164028251508292041959926849162473699550018653393834944216172810195882161876866188294352485183178740261279280213486011018791012560046012995409807741782162189252951939029564062935408459914894373210511494699108265315264830173403743547300700976944780004513514866386570658448247527151658945604790687693036691590606045331434271899594734825392560698221510565391059565109571638751133487824774572142934078485772422422132834305704887084146829228294925039109858598295988853017494057928948890390543290199918610303090142501490713145935617325806587528883833726972378426243439037")]
    num_phases = 100
    phase = 0
    base_pattern = [0, 1, 0, -1]
    while phase < num_phases:
        outdigits = []
        out_pos = 1
        while out_pos < len(inpt)+1:
            # don't think this is right, the repeats in the output aren't necessary with the same frequency as the repeats in the input
            outdigit = 0
            # inpt has length 650
            # pattern, built out of base_pattern, has length dependent on out_pos
            # so after lcm(650, out_pos*len(base_pattern)-1) we're just doing the same thing
            len_pattern = out_pos*len(base_pattern)
            lcm = int(abs(len(inpt)*len_pattern) / gcd(len(inpt), len_pattern))
            if lcm%10 != 0:
                # get the base one in
                outdigit += sum([inpt[i%len(inpt)]*base_pattern[((i+1)//out_pos)%len(base_pattern)] for i in range(lcm)])
                # multiply up to take care of most of it
                outdigit *= 10000*len(inpt) // lcm
            # and now get the remainder
            outdigit += sum([inpt[i%len(inpt)]*base_pattern[((i+1)//out_pos)%len(base_pattern)] for i in range(0, (10000*len(inpt))%lcm)])
            outdigits.append(abs(outdigit)%10)
            out_pos += 1
        print(f"completed phase {phase}, got {''.join(outdigits)}")
        phase += 1
        inpt = outdigits
    print(''.join([str(i) for i in inpt[4058021:][:10]]))

solve()