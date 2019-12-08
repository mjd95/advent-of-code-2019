def solve():
    with open("input", "r") as f:
        image = f.readline().strip()
    width = 25
    height = 6
    
#    image = "0222112222120000"
#    width = 2
#    height = 2

    layers = len(image)//(width*height)
    rendered = [[2 for i in range(width)] for i in range(height)]
    for layer in range(layers):
        for i in range(height):
            for j in range(width):
                el = int(image[j+ i*width + layer*(width*height)])  
                if rendered[i][j] == 2:
                    rendered[i][j] = el

    for i in range(height):
        pic = ""
        for j in range(width):
            if rendered[i][j] == 2:
                # transparent
                pic += " "
            elif rendered[i][j] == 1:
                # white
                pic += u"\u2588"
            elif rendered[i][j] == 0:
                # black
                pic += u"\u2598"
        print(pic)
    
if __name__=="__main__":
    solve()