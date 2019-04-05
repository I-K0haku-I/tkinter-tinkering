test = [1,2,3,4]
test2 = ['a','b']

z = zip(test, test2)
z1 = zip(test, test2)
z2 = zip(test, test2)

print(list(z))
print(*z1)
print(list(zip(*z2)))
