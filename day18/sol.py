import random

# first try a reasonable but incorrect algorithm - always walk to the nearest available key
def solve():
    with open("input", "r") as f:
        orig_screen = [list(line.strip()) for line in f if line.strip()]

    # find starting position
    orig_initial_pos = None
    for j in range(len(orig_screen)):
        for i in range(len(orig_screen[j])):
            if orig_screen[j][i] == "@":
                orig_initial_pos = (i, j)
                break

    orig_screen[orig_initial_pos[1]][orig_initial_pos[0]] = "#"
    orig_screen[orig_initial_pos[1]-1][orig_initial_pos[0]] = "#"
    orig_screen[orig_initial_pos[1]+1][orig_initial_pos[0]] = "#"
    orig_screen[orig_initial_pos[1]][orig_initial_pos[0]-1] = "#"
    orig_screen[orig_initial_pos[1]][orig_initial_pos[0]+1] = "#"

    starting_positions = [(orig_initial_pos[0]-1, orig_initial_pos[1]-1), (orig_initial_pos[0]-1,orig_initial_pos[1]+1), (orig_initial_pos[0]+1, orig_initial_pos[1]-1), (orig_initial_pos[0]+1, orig_initial_pos[1]+1)]
    for sp in starting_positions:
        orig_screen[sp[1]][sp[0]] = "@"

    # get a map whose keys are quadrant enums, vals are all the keys in that quadrant
    # so if a robot encounters a door whose key is _not_ in its own quadrant, it will just assume that another robot has already opened it
    # if a solution exists, then we can always sequence robots s.t. above assumption is valid
    tot = 0
    for i in range(0, 4):
        sp = starting_positions[i]
        keys_in_quadrant = find_reachable_keys(sp, [], orig_screen, [])
        dist = distance_to_collect_remaining_keys(sp, [], orig_screen, {}, keys_in_quadrant)
        print(f"sp={sp}, keys_in_quadrant={keys_in_quadrant.keys()}, dist={dist}")
        tot += dist
    print(tot)

def find_reachable_keys(initial_pos, collected_keys, screen, keys_in_quadrant):
    to_visit = [initial_pos]
    discovered = {initial_pos: True}
    parent = {}
    keys = {}
    while len(to_visit) > 0:
        pos = to_visit.pop(0)
        for p in neighbours(pos, screen):
            if screen[p[1]][p[0]] == "#":
                # wall loc
                pass
            elif screen[p[1]][p[0]].islower():
                if screen[p[1]][p[0]] not in collected_keys:
                    keys[screen[p[1]][p[0]]] = p
                if p not in discovered:
                    discovered[p] = True
                    to_visit.append(p)
                    parent[p] = pos
            elif screen[p[1]][p[0]].isupper():
                if (screen[p[1]][p[0]].lower() in collected_keys) or (not screen[p[1]][p[0]].lower() in keys_in_quadrant):
                    if p not in discovered:
                        discovered[p] = True
                        to_visit.append(p)
                        parent[p] = pos
            else:
                if p not in discovered:
                    discovered[p] = True
                    to_visit.append(p)
                    parent[p] = pos
 
    keys_with_dist = {}
    for k in keys.keys():
        l = 1
        p = keys[k]
        while parent[p] != initial_pos:
            l += 1
            p = parent[p]
        keys_with_dist[k] = (keys[k], l)

    return keys_with_dist

def distance_to_collect_remaining_keys(pos, collected_keys, screen, cache, keys_in_quadrant):
    cache_key = (pos, tuple(sorted(collected_keys)))
    if cache_key in cache:
        return cache[cache_key]

    reachable = find_reachable_keys(pos, collected_keys, screen, keys_in_quadrant) 

    if len(reachable.keys()) == 0:
        return 0

    min_dist = 1000000000000000000000
    for key, (new_pos, dist) in reachable.items():
        collected_keys.append(key)
        d = dist + distance_to_collect_remaining_keys(new_pos, collected_keys, screen, cache, keys_in_quadrant)
        collected_keys.pop()
        min_dist = min(min_dist, d)

    cache[cache_key] = min_dist

    return min_dist

def neighbours(pos, screen):
    neighbours = []
    if pos[0]>0:
        neighbours.append((pos[0]-1, pos[1]))
    if pos[0]<len(screen[0])-1:
        neighbours.append((pos[0]+1, pos[1]))
    if pos[1]>0:
        neighbours.append((pos[0], pos[1]-1))
    if pos[1]<len(screen[1])-1:
        neighbours.append((pos[0], pos[1]+1))
    return neighbours

solve()
