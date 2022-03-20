import hashlib
import random
from PIL import Image


def create_alf(prealf):
    alf = []
    for r in enumerate(prealf):
        for g in enumerate(prealf):
            for b in enumerate(prealf):
                alf.append(r[1] + g[1] + b[1])
    return alf


def parseInt(num, alf):
    b = []
    while num:
        b.append(alf[num % len(alf)])
        num //= len(alf)
    b.reverse()
    b = '|'.join(b)
    return b


def mod(a, b):
    return ((a % b) + b) % b


def getHash(a):
    return int(hashlib.sha512(a.encode()).hexdigest()[7], 16)


def pad(s, size):
    s.ljust(size, '0')
    return s


class Babel:
    def __init__(self):
        self.seed = 13
        self.prealf = '0123456789abcdef'

        # self.alf = create_alf(prealf)
        self.alphabet = self.digs = create_alf(self.prealf)
        self.lalf = len(self.alphabet)
        self.lengthOfTitle = 66560

        self.lengthOfPage = 39600
        self.width, self.height = 220, 180

        self.wall = 4
        self.shelf = 5
        self.volume = 32
        self.page = 410

        self.digsIndexes = {}
        self.alfIndexes = {}
        self.create_indexes()

    def create_im(self, address):
        img = Image.new('RGBA', (self.width, self.height), 'white')
        pix = img.load()
        m = []
        v = 0
        page = self.getPage(address)
        for i in range(self.height):
            m.append([])
            for j in range(self.width):
                m[-1].append(page[v * 3: v * 3 + 3])
                v += 1
        for i in range(self.height):
            for j in range(self.width):
                pix[j, i] = self.prealf.index(m[i][j][0]) * 16, self.prealf.index(m[i][j][1]) * 16, self.prealf.index(m[i][j][2]) * 16
        img.save('im.png')

    def rnd(self, mn=1, mx=0):
        m, a, c = 2 ** 32, 22695477, 1
        self.seed = (self.seed * a + c) % m
        return mn + self.seed / m * (mx - mn)

    def create_indexes(self):
        for pos, char in enumerate(self.digs):
            self.digsIndexes[char] = pos
        for pos, char in enumerate(self.alphabet):
            self.alfIndexes[char] = pos

    def search(self, searchStr):
        wall = str(int(random.random() * self.wall + 1))
        shelf = str(int(random.random() * self.shelf + 1))
        volume = pad(str(int(random.random() * self.volume + 1)), 2)
        page = pad(str(int(random.random() * self.page + 1)), 3)
        locHash = getHash(wall + shelf + volume + page)
        hex = ''
        depth = int(random.random() * (self.lengthOfPage - len(searchStr) // 3))
        for i in range(depth):
            searchStr = self.alphabet[int(random.random() * len(self.alphabet))] + searchStr
        self.seed = locHash
        searchStr = [searchStr[j: j + 3] for j in range(0, len(searchStr), 3) if len(searchStr[j: j + 3]) == 3]
        for i in range(len(searchStr)):
            index = self.alfIndexes[searchStr[i]] or -1
            rand = self.rnd(0, len(self.alphabet))
            newIndex = mod(index + int(rand), len(self.digs))
            newChar = self.digs[newIndex]
            hex += str(newChar)
        return str(hex) + '-' + str(wall) + '-' + str(shelf) + '-' + str(int(volume)) + '-' + str(int(page))

    def searchExactly(self, text):
        pos = int(random.random() * (self.lengthOfPage - len(text)))
        return self.search(' ' * pos + text + ' ' * (self.lengthOfPage - (pos + len(text))))

    def searchTitle(self, searchStr):
        wall = str(int(random.random() * self.wall + 1))
        shelf = str(int(random.random() * self.shelf + 1))
        volume = pad(str(int(random.random() * self.volume + 1)), 2)
        locHash = getHash(str(wall) + str(shelf) + str(volume))
        hex = ''
        searchStr = searchStr[:self.lengthOfTitle * 3]
        searchStr = searchStr if len(searchStr) == self.lengthOfTitle * 3 else str(searchStr) + '   ' * (
                self.lengthOfTitle - len(searchStr) // 3)
        self.seed = locHash
        searchStr = [searchStr[j: j + 3] for j in range(0, len(searchStr), 3)]
        for i in range(len(searchStr)):
            index = self.alfIndexes[searchStr[i]]
            rand = self.rnd(0, len(self.alphabet))
            newIndex = mod(index + int(rand), len(self.digs))
            newChar = self.digs[newIndex]
            hex += newChar
        return str(hex) + '-' + str(wall) + '-' + str(shelf) + '-' + str(int(volume))

    def getPage(self, address):
        addressArray = address.split('-')
        hex = addressArray[0]
        locHash = getHash(
            addressArray[1] + addressArray[2] + str(pad(addressArray[3], 2)) + str(pad(addressArray[4], 3)))
        result = ''
        self.seed = locHash
        hex = [hex[j: j + 3] for j in range(0, len(hex), 3)]
        for i in range(len(hex)):
            index = self.digsIndexes[hex[i]]
            rand = self.rnd(0, len(self.digs))
            newIndex = mod(index - int(rand), len(self.alphabet))
            newChar = self.alphabet[newIndex]
            result += newChar
        self.seed = getHash(result)
        while len(result) < self.lengthOfPage * 3:
            result += self.alphabet[int(self.rnd(0, len(self.alphabet)))]
        return result[len(result) - self.lengthOfPage * 3:]

    def getTitle(self, address):
        addressArray = address.split('-')
        hex = addressArray[0]
        locHash = getHash(addressArray[1] + addressArray[2] + str(pad(addressArray[3], 2)))
        result = ''
        self.seed = locHash
        for i in range(len(hex)):
            index = self.digsIndexes[hex[i]]
            rand = self.rnd(0, len(self.digs))
            newIndex = mod(index - int(rand), len(self.alphabet))
            newChar = self.alphabet[newIndex]
            result += newChar
        self.seed = getHash(result)
        while len(result) < self.lengthOfTitle * 3:
            result += self.alphabet[int(self.rnd(0, len(self.alphabet)))]
        return result[len(result) - self.lengthOfTitle * 3:]


babel = Babel()
text = '000' * 400
address = babel.search(text)
print(address)
babel.create_im(address)
