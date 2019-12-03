def traverse(wire):
    path = [(0, 0)]
    cur = (0, 0)
    for s in wire:
        if s[0]=="R":
            for _ in range(0, int(s[1:])):
                cur = (cur[0]+1, cur[1])
                path += [cur]
        elif s[0]=="L":
            for _ in range(0, int(s[1:])):
                cur = (cur[0]-1, cur[1])
                path += [cur]
        elif s[0]=="U":
            for _ in range(0, int(s[1:])):
                cur = (cur[0], cur[1]+1)
                path += [cur]
        elif s[0]=="D":
            for _ in range(0, int(s[1:])):
                cur = (cur[0], cur[1]-1)
                path += [cur]
    return path

def solve():
    with open("input", "r") as f:
        wires = [line.split(",") for line in f if line.strip()]
    wire1 = wires[0]
    wire2 = wires[1]

    path1 = traverse(wire1)
    path2 = traverse(wire2)

    intersections = list({s for s in set(path1) if s!=(0,0)} & {s for s in set(path2) if s!=(0,0)})

    smallest = path1.index(intersections[0]) + path2.index(intersections[0])
    for intersection in intersections[1:]:
        smallest = min(smallest, path1.index(intersection) + path2.index(intersection))

    print(smallest)


if __name__=="__main__":
    solve()