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

    print(f"after time 0, positions {positions}, velocities {velocities}")

    seen = {tuple(tuple(p) for p in positions+velocities)}
    ts = 0
    while True:
       # apply gravity
        for i in range(len(velocities)):
            velocities[i][0] = get_velocity(i, 0, velocities[i][0], positions)
            velocities[i][1] = get_velocity(i, 1, velocities[i][1], positions)
            velocities[i][2] = get_velocity(i, 2, velocities[i][2], positions)
    
        # apply velocities
        for i in range(len(positions)):
            for j in range(3):
                positions[i][j] += velocities[i][j]
        ts += 1 
        cur = tuple(tuple(p) for p in positions+velocities)
        if cur in seen:
            print(f"found a repeat!  ts={ts}")
            return

    print(positions)
    print(velocities)
    tot = 0
    for i in range(len(positions)):
        pot = 0
        kin = 0
        for j in range(3):
            pot += abs(positions[i][j])
            kin += abs(velocities[i][j])
        tot += pot*kin
    print(tot)

if __name__=="__main__":
    solve()