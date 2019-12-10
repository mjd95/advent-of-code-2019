def solve():
    with open("input", "r") as f:
        arr = [[el for el in line.strip()] for line in f if line.strip()]

    asteriod_locs = []
    for y in range(len(arr)):
        for x in range(len(arr[y])):
            if arr[y][x]=='#':
                asteriod_locs.append((x, y))

    best = 0
    best_pos = None
    for first in asteriod_locs:
        above = {}
        below = {}
        right = False
        left = False
        tot = 0
        for second in asteriod_locs:
            dx = second[0] - first[0]
            dy = second[1] - first[1]
            if dy > 0:
                if dx/dy not in above:
                    tot += 1
                    above[dx/dy] = True
            elif dy < 0:
                if dx/dy not in below:
                    tot += 1
                    below[dx/dy] = True
            else:
                if dx > 0:
                    if not right:
                        tot += 1
                        right = True
                elif dx < 0:
                    if not left:
                        tot += 1
                        left = True
        if tot > best:
            best = tot
            best_pos = first

    print(best_pos, best)

    first = best_pos

    n = []
    ne = {}
    e = []
    se = {}
    s = []
    sw = {}
    w = []
    nw = {}
    for second in asteriod_locs:
        dx = second[0] - first[0]
        dy = second[1] - first[1]
        if dx==0 and dy<0:
            n.append(second)
        elif dx > 0 and dy<0:
            if dx/dy not in ne:
                ne[dx/dy] = [second]
            else:
                ne[dx/dy].append(second)
        elif dx > 0 and dy==0:
            e.append(second)
        elif dx>0 and dy>0:
            if dx/dy not in se:
                se[dx/dy] = [second]
            else:
                se[dx/dy].append(second)
        elif dx==0 and dy>0:
            s.append(second)
        elif dx<0 and dy>0:
            if dx/dy not in sw:
                sw[dx/dy] = [second]
            else:
                sw[dx/dy].append(second)
        elif dx<0 and dy==0:
            w.append(second)
        elif dx<0 and dy<0:
            if dx/dy not in nw:
                nw[dx/dy] = [second]
            else:
                nw[dx/dy].append(second)
    for compass in [n, e, s, w]:
        compass.sort(key=lambda el: (el[0]-first[0])**2 + (el[1]-first[1])**2)
    for quad in [ne, se, sw, nw]:
        print(len(quad.keys()))
    for quad in [ne, se, sw, nw]: 
        for _, v in quad.items():
            v.sort(key=lambda el: (el[0]-first[0])**2 + (el[1]-first[1])**2)

    destroyed = 0
    while destroyed < 200:
        print(f"going to try to destroy something form {n}")
        if len(n)>0:
            d = n.pop(0)
            destroyed += 1
            print(f"destruction {destroyed} was item {d}")
        print(f"going to try to destroy something from ne={ne}")
        ks = sorted(list(ne.keys()), reverse=True) 
        for k in ks:
            d = ne[k].pop(0)
            destroyed += 1
            print(f"destruction {destroyed} was item {d}")
            if len(ne[k])==0:
                del(ne[k])
        print(f"going to try to destroy something from {e}")
        if len(e)>0:
            d = e.pop(0)
            destroyed += 1
            print(f"destruction {destroyed} was item {d}")
        print(f"going to try to destroy something from se={se}")
        ks = sorted(list(se.keys()), reverse=True) 
        for k in ks:
            d = se[k].pop(0)
            destroyed += 1
            print(f"destruction {destroyed} was item {d}")
            if len(se[k])==0:
                del(se[k])
        print(f"going to try to detroy something from {s}")
        if len(s)>0:
            d = s.pop(0)
            destroyed += 1
            print(f"destruction {destroyed} was item {d}")
        print(f"going to try to destory something from sw={sw}")
        ks = sorted(list(sw.keys()), reverse=True) # x=-1,y=-500 (1/500) is first; x=-500,y=-1 (500) is last
        for k in ks:
            d = sw[k].pop(0)
            destroyed += 1
            print(f"destruction {destroyed} was item {d}")
            if len(sw[k])==0:
                del(sw[k])
        print(f"going to try to destroy something from {w}")
        if len(w)>0:
            d = w.pop(0)
            destroyed += 1
            print(f"destruction {destroyed} was item {d}")
        print(f"going to try to destory something from nw={nw}")
        ks = sorted(list(nw.keys()), reverse=True) # x=-500, y=1 (-500) is first; x=-1,y=500 (-1/500) is last
        for k in ks:
            d = nw[k].pop(0)
            destroyed += 1
            print(f"destruction {destroyed} was item {d}")
            if len(nw[k])==0:
                del(nw[k])

if __name__=="__main__":
    solve()