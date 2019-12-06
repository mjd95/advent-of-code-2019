def dfs(tree, node, visited, height, total_height):
    visited[node] = True
    total_height[0] += height

    if node not in tree:
        height -= 1
        return
    for i in tree[node]:
        if not i in visited:
            height += 1
            dfs(tree, i, visited, height, total_height)
        height -= 1    


def solve():
    tree = {}
    with open("input", "r") as f:
        for line in [l.strip() for l in f if l.strip()]:
            (parent, child) = line.split(")")
            if parent in tree:
                tree[parent] += [child]
            else:
                tree[parent] = [child]    

    visited = {}
    total_height = [0]
    dfs(tree, "COM", visited, 0, total_height)
    print(total_height[0])

if __name__=="__main__":
    solve()