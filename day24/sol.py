num_levels = 200

def solve():
    with open("input", "r") as f:
        cur = [[el for el in line.strip()] for line in f if line.strip()]

    grid = {}
    for level in range(-num_levels, num_levels+1):
        if level != 0:
            grid[level] = [["." for _ in range(len(cur[0]))] for _ in range(len(cur))]
        else:
            grid[level] = cur

    nxt_grid = {}
    for level in range(-num_levels, num_levels+1):
        nxt_grid[level] = [["." for _ in range(len(cur[0]))] for _ in range(len(cur))]

    phase = 0
    while phase < num_levels:
        for level in range(-num_levels, num_levels+1):
            for j in range(len(grid[level])):
                for i in range(len(grid[level][j])):
                    if i==2 and j==2:
                        continue
                    num_bugs = 0
                    for nbr in get_neighbours(level, i, j):
                        if nbr[0]<-num_levels or nbr[0]>num_levels:
                            continue
                        if grid[nbr[0]][nbr[2]][nbr[1]] == "#":
                            num_bugs += 1
                    if grid[level][j][i]=="#":
                        if num_bugs==1:
                            nxt_grid[level][j][i]="#"
                        else:
                            nxt_grid[level][j][i]="."
                    else:
                        if num_bugs==1 or num_bugs==2:
                            nxt_grid[level][j][i]="#"
                        else:
                            nxt_grid[level][j][i]="."
        nxt_grid,grid=grid,nxt_grid
        phase += 1

    tot_bugs = 0
    for level in range(-num_levels, num_levels+1):
        for j in range(len(grid[level])):
            for i in range(len(grid[level][j])):
                if grid[level][j][i] == '#':
                    tot_bugs += 1
    print(tot_bugs)

def get_neighbours(level, i, j):
    # take the obvious ones
    in_bounds = lambda x, y: x>=0 and y>=0 and x<5 and y<5
    stds = [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]
    nbrs = [(level,x,y) for (x,y) in stds if in_bounds(x,y)]

    # add in any extras from level-1
    if j==0:
        nbrs.append((level-1, 2, 1))
    if j==4:
        nbrs.append((level-1, 2, 3))
    if i==0:
        nbrs.append((level-1, 1, 2))
    if i==4:
        nbrs.append((level-1, 3, 2))

    # add in any extras from level+1
    if i==2 and j==1:
        nbrs += [(level+1, 0, 0), (level+1, 1, 0), (level+1, 2, 0), (level+1, 3, 0), (level+1, 4, 0)]
    if i==2 and j==3:
        nbrs += [(level+1, 0, 4), (level+1, 1, 4), (level+1, 2, 4), (level+1, 3, 4), (level+1, 4, 4)]
    if i==1 and j==2:
        nbrs += [(level+1, 0, 0), (level+1, 0, 1), (level+1, 0, 2), (level+1, 0, 3), (level+1, 0, 4)]
    if i==3 and j==2:
        nbrs += [(level+1, 4, 0), (level+1, 4, 1), (level+1, 4, 2), (level+1, 4, 3), (level+1, 4, 4)]
    return nbrs

solve()