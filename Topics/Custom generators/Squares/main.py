n = int(input())


def squares():
    for i in range(1,n+1):
        yield i*i


# Don't forget to print out the first n numbers one by one here
for j in squares():
    print(j)