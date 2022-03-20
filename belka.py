from PIL import Image
import hashlib


def create_alf():
    alf = []
    for r in prealf:
        for g in prealf:
            for b in prealf:
                alf.append(r + g + b)
    return alf


prealf = '0123456789abcdef'

alf = create_alf()
lalf = len(alf)

width = 208
height = 320

l = ((len(prealf) ** 3 * 2) ** (width * height)) - 1

room = str(301**465)
rack = hashlib.sha512('3'.encode()).hexdigest()
shelf = hashlib.sha512('2'.encode()).hexdigest()
book = hashlib.sha512('7'.encode()).hexdigest()
page = hashlib.sha512('1'.encode()).hexdigest()

num = int(room) ** 400 * int(rack, 16) ** 200 * int(shelf, 16) ** 200 * int(book, 16) ** 200 * int(page, 16) ** 200
print(len(str(num)))

# b = []
# while num:
#     b.append(alf[num % lalf])
#     num //= lalf
# b = b[:width * height]
# b.reverse()
# v = 0
# m = []
# img = Image.new('RGBA', (width, height), 'white')
#
# pix = img.load()
# for i in range(height):
#     m.append([])
#     for j in range(width):
#         m[-1].append(b[v])
#         v += 1
# for i in range(height):
#     for j in range(width):
#         pix[j, i] = prealf.index(m[i][j][0]) * 8, prealf.index(m[i][j][1]) * 8, prealf.index(m[i][j][2]) * 8
# img.save('im.png')
# # print(*m, sep='\n')
