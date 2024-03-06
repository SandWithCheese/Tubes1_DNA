xp, yp = -100, -100
with open('greedy.out') as f:
    for line in f:
        if "Delta " in line:
            _, a, b = line.split()
            a = int(a)
            b = int(b)
            if abs(xp - a) + abs(yp - b) != 1:
                print("Found error at", a, b)
            xp = a
            yp = b