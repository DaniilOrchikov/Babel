def create_alf():
    alf = []
    for r in prealf:
        for g in prealf:
            for b in prealf:
                alf.append(r + g + b)
    return alf


def lcg():
    a = 474748
    c = l
    m = 32768 ** 196608
    global seed
    seed = (a * seed + c) % m
    return seed


prealf = '0123456789abcdefghijklmnopqrstuv'

alf = create_alf()
lalf = len(alf)

width = 72
height = 128

l = (len(prealf) ** 3 * 2) ** (width * height)

room = '19832835253283383535385258533323232532'
rack = '17877887877878786675645332456768654323454677889876544678987867543456778765435678987654678'
shelf = '1432342343443232232423324'
book = '1432432343443342344'
page = '143242334243432243'

seed = int(room + rack + shelf + book + page)

num = lcg()
b = []
while num:
    b.append(alf[num % lalf])
    num //= lalf
b = b[:9216]
b.reverse()
v = 0
m = []
for i in range(height):
    m.append([])
    for j in range(width):
        m[-1].append(b[v])
        v += 1
print(*m, sep='\n')
