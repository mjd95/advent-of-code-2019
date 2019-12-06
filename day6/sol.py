def find_path(tree, node, visited, path, target):
    visited[node] = True
    path.append(node)
    if node==target:
        print(path)

    if node not in tree:
        return
    for i in tree[node]:
        if not i in visited:
            find_path(tree, i, visited, path, target)    
        path.pop()

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

    visited = {}
    path = []
    find_path(tree, "COM", visited, path, "YOU")
    you_path = ['COM', 'FJH', 'XLG', 'MCK', 'VS2', '6L4', '5XC', '49P', 'ZL4', '4RC', '6J5', 'TYH', '9CD', 'SNF', 'X43', 'SJC', 'DS3', 'QY3', '1M3', '2FY', '99T', 'V1M', 'Q3P', 'HW6', '93R', 'ZVR', 'GCP', 'B9P', '3CQ', 'CVJ', 'CRK', 'WLT', '9SH', 'LYC', 'JRH', 'VK3', 'QKT', 'QT7', 'C7Z', 'BB7', 'X3T', 'QF8', 'RZL', 'NQ5', 'VXP', 'B4R', 'QZL', 'G1M', '2PD', 'RH4', 'LGH', 'WYL', '3HR', 'KN1', 'M2P', 'KXL', 'DTY', 'XZS', 'C94', 'P6L', '4N8', '6K9', 'TB5', 'BRN', 'DQJ', 'SBF', '7CW', 'NHF', 'YQ7', 'SDL', 'SWV', 'KGL', 'W5N', 'J6H', 'SCK', 'ZSK', '92M', 'DJ5', 'GJW', '9MH', 'CMW', '6QY', 'XZG', '7T3', '5N6', '2JQ', 'GC3', '3VP', 'W6Z', 'PXP', 'FJ7', 'HN9', 'T91', '83M', 'F3F', 'Z8X', 'ZV7', 'SR1', '1C3', 'VJP', 'WWT', '8WB', 'YTN', '2Q9', 'LVH', 'XPC', '3H7', 'QLT', 'KC3', 'WQP', 'ZFZ', 'LVD', 'DB4', 'T4N', 'WQB', 'JWH', 'D7Q', 'DRN', 'VLL', 'CBY', 'GS5', '7K9', '5FQ', '3TG', 'TCH', 'D4M', '5TD', 'S1N', '1LG', '4FH', '256', 'WTQ', 'DRX', 'Q93', 'GPP', 'DXC', 'Z6C', '9LK', 'M9T', 'Z3P', 'YYQ', 'X6B', 'MZX', 'Z7X', 'JY5', 'C6Y', 'VKX', 'ZCH', '9YP', 'BJS', 'XCX', 'LR1', '7ZV', '939', 'R1J', '3MP', '1DZ', 'DD2', 'Z21', '3L5', 'DZ4', '5MN', 'NGY', 'QSY', 'SRX', 'PWR', 'GHV', 'KTT', '681', '7FM', 'QX1', '63X', '9GN', 'BKW', 'Y5H', 'RF8', '52F', '7WL', '82P', 'SFW', '4JQ', 'XFX', 'CDC', 'MYT', 'CXJ', 'VHG', '3W4', 'YY3', 'X9P', '1BD', '7WW', '745', 'FYB', 'BHM', 'HJ2', 'X9D', '55W', '3J9', 'XSB', 'K4R', 'YVH', '1LW', 'MQD', 'G37', 'G23', 'BC9', 'M7N', 'L33', '1ZW', 'WGM', 'N88', 'ZR2', 'Z88', '7NP', 'GLP', 'G9H', 'HGC', '7X1', 'P4F', 'QJK', '3K5', '413', 'WS5', 'PXV', '4HV', 'CQR', 'X3C', 'BW5', 'KBJ', 'J5L', 'H9Y', '4SF', 'V52', 'X8F', 'KM8', 'YBG', 'HFM', '81R', '5LN', 'R15', 'M2S', 'PD2', 'RTX', 'ZSP', 'R3L', 'P1Y', '584', '6ZP', 'GHH', 'TBX', 'BNF', 'S11', 'FJF', 'CF2', 'JXV', 'ZG8', '75V', 'D8L', 'T4F', '6VM', 'M58', 'TQ5', 'JR3', 'KFH', 'R7W', 'YOU']
    
    visited = {}
    path = []
    find_path(tree, "COM", visited, path, "SAN")
    san_path = ['COM', 'FJH', 'XLG', 'MCK', 'VS2', '6L4', '5XC', '49P', 'ZL4', '4RC', '6J5', 'TYH', '9CD', 'SNF', 'X43', 'SJC', 'DS3', 'QY3', '1M3', '2FY', '99T', 'V1M', 'Q3P', 'HW6', '93R', 'ZVR', 'GCP', 'B9P', '3CQ', 'CVJ', 'CRK', 'WLT', '9SH', 'LYC', 'JRH', 'VK3', 'QKT', 'QT7', 'C7Z', 'BB7', 'X3T', 'QF8', 'RZL', 'NQ5', 'VXP', 'B4R', 'QZL', 'G1M', '2PD', 'RH4', 'LGH', 'WYL', '3HR', 'KN1', 'M2P', 'KXL', 'DTY', 'XZS', 'C94', 'S4Z', '4WP', 'Q6G', 'LVV', 'BCH', 'VG2', 'CCD', 'ZRN', 'RL3', 'TGN', 'FRK', '5V6', '5R4', 'YVK', 'BJF', 'WKV', 'Y55', 'QFB', 'YLR', 'Q7J', 'N5R', 'ZVF', '49D', 'LTH', 'MB4', 'NX9', 'VCN', '42S', 'YW5', 'KFV', 'T8K', 'SMB', 'T79', 'L93', '7J4', '5YT', 'D3V', 'LG2', 'J6Z', '7ZC', 'SNP', 'MDR', '4ZM', 'G3Q', 'MS6', 'KQH', 'WWN', 'LTX', 'JR4', 'Q11', 'QBW', 'XZ8', 'L92', 'FGK', 'QLH', 'SCR', 'YDY', '7SC', '7C6', 'FHH', 'JKV', 'ZQF', 'WY2', 'BPB', '65P', '4GS', 'YW9', 'R5H', 'K5P', 'PH8', 'Z42', 'BFG', '3TK', '8KS', '2HP', '1BS', '7VS', 'TRT', '783', 'S3S', 'GN3', '769', 'XZM', 'C12', 'Z8N', '6GM', '2Q2', 'DH3', 'P5B', 'GRV', '39S', '517', 'N73', '5KT', 'MF4', 'CRF', 'N44', '89S', 'QQK', 'KJ8', 'VQ8', '8T5', 'G2W', 'T56', '8GW', 'QM5', 'LWQ', '18X', 'CJY', 'RYX', 'PBK', 'N7R', 'DPR', '9TX', 'GBQ', 'JV9', 'J2B', '3V5', 'KJL', '7GW', 'GDM', '44N', '2W3', 'LJC', 'ZQN', '63G', 'CHN', '1J5', 'DHB', 'DVW', '1T7', 'T2J', 'W44', '758', 'F4G', 'GHY', 'PWB', 'QPL', 'HTT', 'TJ9', 'BTV', 'XK8', 'HLJ', '4T9', 'NYW', '7RZ', '4Y3', 'K11', 'KJ6', 'LYD', '3BR', '1D2', 'XNH', 'KPC', '5S8', 'JHS', '821', '1J4', 'TJL', 'H81', 'KB9', '25M', 'QQ4', '6LL', 'NWC', 'JFJ', '6XD', 'X1K', 'V81', '8B7', 'H18', 'ZVM', '6R1', 'VP4', 'K1V', '13J', 'ZVD', 'YTZ', '8R6', 'X6F', '5BG', 'GZZ', 'SDX', '2ZR', 'GGJ', 'FFG', 'T6N', 'BJ4', 'WRZ', '5P1', '5XS', 'SJN', 'G1G', '29X', '4NH', 'DFB', 'PGM', 'DN2', 'VGG', 'L5P', '861', '4QH', 'KGQ', 'D7T', 'TXM', 'K9K', 'YJZ', 'YDW', '9M3', 'PPF', '2MM', 'CHY', '84S', 'FZM', 'M7P', 'R2P', '3C4', 'HNV', '8YG', 'K5R', 'S1W', 'JFT', 'LJP', 'Q1H', '68X', 'LHC', 'KLT', 'PT2', '235', 'D2V', 'SAN']

    print(you_path, san_path)
    i = 0
    while you_path[i] == san_path[i]:
        i += 1

    print(len(you_path) + len(san_path) - 2*i - 2)
    

if __name__=="__main__":
    solve()