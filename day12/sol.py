from math import gcd

def lcm(a, b):
    return abs(a*b) // gcd(a,b)

def get_velocity(idx, coord, cur_vel, positions):
    vel = cur_vel
    for i in range(len(positions)):
        if i == idx:
            continue
        if positions[idx][coord] < positions[i][coord]:
            vel += 1
        elif positions[idx][coord] > positions[i][coord]:
            vel -= 1
    return vel
    

def solve():
    with open("test", "r") as f:
        lines = [l.strip().strip('<').strip('>').split(',') for l in f if l.split()]
        positions = [[int(l.split('=')[1]) for l in line] for line in lines]

    velocities = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

    repeats = []
    for j in range(3):
        seen = {tuple(p[j] for p in positions+velocities)}
        ts = 0
        while True:
        # apply gravity
            for i in range(len(velocities)):
                velocities[i][j] = get_velocity(i, j, velocities[i][j], positions)
        
            # apply velocities
            for i in range(len(positions)):
                positions[i][j] += velocities[i][j]
            ts += 1 
            cur = tuple(p[j] for p in positions+velocities)
            if cur in seen:
                repeats.append(ts)
                break
    print(lcm(lcm(repeats[0], repeats[1]), repeats[2]))

if __name__=="__main__":
    solve()