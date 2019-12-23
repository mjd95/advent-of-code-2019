max_int = 10000000000000000000000000000000
max_levels = 100

def on_bounds(screen, pos):
    return pos[0]==0 or pos[1]==0 or pos[0]==len(screen[0])-1 or pos[1]==len(screen)-1

def solve():
    with open("input", "r") as f:
        lines = [list(line.strip("\n")) for line in f if line.strip("\n")]

    # go along rows and write all portals onto the dots
    outers = {}
    inners = {}
    start = None
    end = None
    for j in range(len(lines)):
        for i in range(len(lines[j])):
            if i>1:
                if lines[j][i] == "." and lines[j][i-1].isalnum() and lines[j][i-2].isalnum():
                    label = lines[j][i-2] + lines[j][i-1]
                    if label == "AA":
                        start = (i,j)
                    elif label == "ZZ":
                        end = (i,j)
                    else:
                        if on_bounds(lines, (i-2, j)):
                            outers[(i,j)] = label
                        else:
                            inners[(i,j)] = label
                    lines[j][i-2] = " "
                    lines[j][i-1] = " "
                    lines[j][i] = "@"
            if i<len(lines[j])-2:
                if lines[j][i] == "." and lines[j][i+1].isalnum() and lines[j][i+2].isalnum():
                    label = lines[j][i+1] + lines[j][i+2]
                    if label == "AA":
                        start = (i,j)
                    elif label == "ZZ":
                        end = (i,j)
                    else:
                        if on_bounds(lines, (i+2,j)):
                            outers[(i,j)] = label
                        else:
                            inners[(i,j)] = label
                    lines[j][i] = "@"
                    lines[j][i+1] = " "
                    lines[j][i+2] = " "
            if j>1:
                if lines[j][i] == "." and lines[j-1][i].isalnum() and lines[j-2][i].isalnum():
                    label = lines[j-2][i] + lines[j-1][i]
                    if label == "AA":
                        start = (i,j)
                    elif label == "ZZ":
                        end = (i,j)
                    else:
                        if on_bounds(lines, (i, j-2)):
                            outers[(i,j)] = label
                        else:
                            inners[(i,j)] = label
                    lines[j-2][i] = " "
                    lines[j-1][i] = " "
                    lines[j][i] = "@"
            if j<len(lines)-2:
                if lines[j][i] == "." and lines[j+1][i].isalnum() and lines[j+2][i].isalnum():
                    label = lines[j+1][i] + lines[j+2][i]
                    if label == "AA":
                        start = (i,j)
                    elif label == "ZZ":
                        end = (i,j)
                    else:
                        if on_bounds(lines, (i, j+2)):
                            outers[(i,j)] = label
                        else:
                            inners[(i,j)] = label
                    lines[j][i] = "@"
                    lines[j+1][i] = " "
                    lines[j+2][i] = " "

    for line in lines:
        print("".join(line))

    # start at the start, aim for the end, do dijkstra and lookup the teleportal whenever we hit one
    dists = dijkstra(lines, outers, inners, start, end)

    for k, v in dists.items():
        if k[2]==0:
            lines[k[1]][k[0]] = str(v)

#    for line in lines:
#        for i in range(len(line)):
#            if len(line[i]) == 1:
#                line[i] = line[i] + "  "
#            elif len(line[i]) == 2:
#                line[i] = line[i] + " "
#        print("".join(line))

    print(dists[(end[0], end[1], 0)])

def dijkstra(screen, outers, inners, start, end):
    dists = {}
    visited = {}
    for j in range(len(screen)):
        for i in range(len(screen[j])):
            for l in range(max_levels):
                if screen[j][i] == "." or screen[j][i] == "@":
                    dists[(i,j,l)] = max_int
                    visited[(i,j,l)] = False
    dists[(start[0], start[1], 0)] = 0
    to_visit = [(start[0], start[1], 0)]
    while len(to_visit) > 0:
        cur = to_visit.pop(0)
        for p in neighbours(screen, cur, inners, outers, start, end):
            # update the distance
            dists[p] = min(dists[p], dists[cur]+1)

            # add to the to_visit if not already visited
            if not visited[p]:
                to_visit.append(p)

        visited[cur] = True
        if cur==end:
            break

    return dists
    
def neighbours(screen, cur, inners, outers, start, end):
    ret = []
    ns = [(cur[0]-1,cur[1]), (cur[0]+1, cur[1]), (cur[0], cur[1]-1), (cur[0], cur[1]+1)]
    for n in ns:
        if screen[n[1]][n[0]]==".":
            ret.append((n[0], n[1], cur[2]))
        elif screen[n[1]][n[0]]=="@":
            if cur[2]==0:
                # only start, end and inners are allowed
                if n==start or n==end or n in inners:
                    ret.append((n[0], n[1], cur[2]))
            else:
                # all are allowed except start and end
                if not n==start and not n==end:
                    ret.append((n[0], n[1], cur[2]))
        
    if (cur[0], cur[1]) in outers:
        lbl = outers[(cur[0], cur[1])]
        for k, v in inners.items():
            if v==lbl:
                ret.append((k[0], k[1], cur[2]-1))
                break
    if (cur[0], cur[1]) in inners and cur[2]<max_levels-1:
        lbl = inners[(cur[0], cur[1])]
        for k, v in outers.items():
            if v==lbl:
                ret.append((k[0], k[1], cur[2]+1))
                break
    
    return ret

solve()