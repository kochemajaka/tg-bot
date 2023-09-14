N = int(input())
mass=[]
for i in range(N):
    str = list(map(int,input().split()))
    mass+=[str]
mass.sort()
s_polz = mass[0][0] + mass[1][0] + mass[2][0] + mass[3][0]
for i in range(4):
    mass.pop(0)
mass.sort(key=lambda x: x[1])
s_nap = mass[0][1]+mass[1][1]
print(s_nap+s_polz)
