def generator():
    yield from input().split()
for g in generator():
    print(g)
