import hashlib
import random
from PIL import Image
import numpy as np


def create_alf(prealf):
    alf = []
    for r in enumerate(prealf):
        for g in enumerate(prealf):
            for b in enumerate(prealf):
                alf.append(r[1] + g[1] + b[1])
    r = []
    v = 0
    while len(r) < len(alf) + 1:
        a = chr(v)
        try:
            with open('readable_alphabet.txt', 'w', encoding='utf-8') as f:
                print(a, file=f)
        except UnicodeEncodeError:
            v += 1
            continue
        if len(a) == 1 and a != '\n' and a != "'" and a != '\\' and a != ' ':
            r.append(a)
        v += 1
    random.shuffle(r)
    with open('readable_alphabet.txt', 'w', encoding='utf-8') as f:
        print(r, file=f)
    return alf, alf


def parse_int(num, alf):
    b = []
    while num:
        b.append(alf[num % len(alf)])
        num //= len(alf)
    b.reverse()
    b = '|'.join(b)
    return b


def mod(a, b):
    return ((a % b) + b) % b


def get_hash(a):
    return int(hashlib.sha512(a.encode()).hexdigest()[7], 16)


def pad(s, size):
    s.ljust(size, '0')
    return s


class Babel:
    def __init__(self):
        self.seed = 13
        self.prealf = '0123456789abcdefghijklmnopqrstuv'  # неьзя использовать '-'
        self.number_of_colors = len(self.prealf)
        # create_alf(self.prealf)

        with open('alphabet.txt', 'r') as f:
            self.alphabet = self.digs = f.read().split()
        with open('readable_alphabet.txt', 'r', encoding='utf-8') as f:
            self.readable_alphabet = f.read().split("'")
        self.alphabet.insert(0, self.alphabet.pop())
        self.lalf = len(self.alphabet)
        self.lengthOfTitle = 31

        self.width, self.height = 360, 310
        self.lengthOfPage = self.width * self.height

        self.wall = 4
        self.shelf = 5
        self.volume = 32
        self.page = 410

        self.digsIndexes = {}
        self.alfIndexes = {}
        self.readable_alphabetIndexes = {}
        self.create_indexes()
        print(len(self.readable_alphabetIndexes), len(self.alfIndexes))
        # print(self.readable_alphabet)

    def search_by_location(self, hex, wall, shelf, volume, page):
        return self.alphabet[0] * (111600 - len(hex)) + str(hex) + '-' + str(wall) + '-' + str(shelf) + '-' + str(
            int(volume)) + '-' + str(int(page))

    def from_readable_title(self, title):
        new_title = ''
        for i in title:
            new_title += self.alphabet[self.readable_alphabetIndexes[i]]
        return new_title

    def in_readable_title(self, title):
        new_title = ''
        for i in range(0, len(title), 3):
            new_title += self.readable_alphabet[self.alfIndexes[title[i: i + 3]]]
        return new_title

    def create_str(self, path):
        im = Image.open(path)
        width, height = im.size
        if width > self.width and height > self.height:
            im = im.resize((self.width, self.height), Image.NEAREST)
        else:
            width, height = im.size
            if width > self.width:
                im = im.resize((self.width, height), Image.NEAREST)
            width, height = im.size
            if height > self.height:
                im = im.resize((width, self.height), Image.NEAREST)
        pix = im.load()
        width, height = im.size
        st = ''
        for i in range(height):
            for j in range(width):
                r, g, b = pix[j, i]
                r, g, b = r // (256 // self.number_of_colors), \
                          g // (256 // self.number_of_colors), \
                          b // (256 // self.number_of_colors)
                st += self.prealf[r] + self.prealf[g] + self.prealf[b]
        return st, width, height

    def create_im(self, address, name):
        img = Image.new('RGB', (self.width, self.height), 'white')
        pix = img.load()
        m = []
        v = 0
        page = self.get_page(address)
        for i in range(self.height):
            m.append([])
            for j in range(self.width):
                m[-1].append(page[v * 3: v * 3 + 3])
                v += 1
        for i in range(self.height):
            for j in range(self.width):
                pix[j, i] = self.prealf.index(m[i][j][0]) * (256 // self.number_of_colors), \
                            self.prealf.index(m[i][j][1]) * (256 // self.number_of_colors), \
                            self.prealf.index(m[i][j][2]) * (256 // self.number_of_colors)
        img.save('static/img/' + name)

    def rnd(self, mn=1, mx=0):
        m, a, c = 2 ** 32, 22695477, 1
        self.seed = (self.seed * a + c) % m
        return mn + self.seed / m * (mx - mn)

    def create_indexes(self):
        for pos, char in enumerate(self.digs):
            self.digsIndexes[char] = pos
        for pos, char in enumerate(self.alphabet):
            self.alfIndexes[char] = pos
        for pos, char in enumerate(self.readable_alphabet):
            self.readable_alphabetIndexes[char] = pos

    def get_random_im(self, name):
        title = [self.readable_alphabet[random.randrange(0, len(self.digs))] for _ in range(self.lengthOfTitle)]
        address = self.search_title(title) + '-' + str(random.randint(1, self.page))
        self.create_im(address, name)

    def search(self, searchStr, width, height):
        wall = str(int(random.random() * self.wall + 1))
        shelf = str(int(random.random() * self.shelf + 1))
        volume = pad(str(int(random.random() * self.volume + 1)), 2)
        page = pad(str(int(random.random() * self.page + 1)), 3)
        locHash = get_hash(wall + shelf + volume + page)
        hex = ''
        w = random.randint(0, self.width - width)
        h = random.randint(0, self.height - height)
        searchStr = [searchStr[j: j + 3] for j in range(0, len(searchStr), 3) if len(searchStr[j: j + 3]) == 3]
        searchArr = [list(i) for i in np.array(searchStr).reshape(height, width)]
        if w:
            for i in range(height):
                for j in range(w):
                    searchArr[i].insert(0, self.alphabet[int(random.random() * len(self.alphabet))])
        if h:
            for i in range(h):
                searchArr.insert(0, [])
                for j in range(w + width):
                    searchArr[0].append(self.alphabet[int(random.random() * len(self.alphabet))])
        for i in range(self.height - height - h):
            searchArr.append([])
            for j in range(width + w):
                searchArr[-1].append(self.alphabet[int(random.random() * len(self.alphabet))])
        for i in range(self.height):
            for j in range(self.width - width - w):
                searchArr[i].append(self.alphabet[int(random.random() * len(self.alphabet))])
        searchStr = np.array(searchArr).flatten()
        self.seed = locHash
        for i in range(len(searchStr)):
            index = self.alfIndexes[searchStr[i]] or -1
            rand = self.rnd(0, len(self.alphabet))
            newIndex = mod(index + int(rand), len(self.digs))
            newChar = self.digs[newIndex]
            hex += str(newChar)
        return str(hex) + '-' + str(wall) + '-' + str(shelf) + '-' + str(int(volume)) + '-' + str(int(page))

    def search_exactly(self, searchStr, width, height):
        searchStr = [searchStr[j: j + 3] for j in range(0, len(searchStr), 3) if len(searchStr[j: j + 3]) == 3]
        searchArr = [list(i) for i in np.array(searchStr).reshape(height, width)]
        for i in range(self.height - height):
            searchArr.append([])
            for j in range(width):
                searchArr[-1].append(self.alphabet[-1])
        for i in range(self.height):
            for j in range(self.width - width):
                searchArr[i].append(self.alphabet[-1])
        searchStr = ''.join(np.array(searchArr).flatten())
        return self.search(searchStr, self.width, self.height)

    def search_title(self, searchStr):
        searchStr = self.from_readable_title(searchStr)
        wall = str(int(random.random() * self.wall + 1))
        shelf = str(int(random.random() * self.shelf + 1))
        volume = pad(str(int(random.random() * self.volume + 1)), 2)
        locHash = get_hash(str(wall) + str(shelf) + str(volume))
        hex = ''
        searchStr = searchStr[:self.lengthOfTitle * 3]
        # searchStr = searchStr if len(searchStr) == self.lengthOfTitle * 3 else str(searchStr) + '00u' * (
        #         self.lengthOfTitle - len(searchStr) // 3)
        self.seed = locHash
        searchStr = [searchStr[j: j + 3] for j in range(0, len(searchStr), 3)]
        for i in range(len(searchStr)):
            index = self.alfIndexes[searchStr[i]]
            rand = self.rnd(0, len(self.alphabet))
            newIndex = mod(index + int(rand), len(self.digs))
            newChar = self.digs[newIndex]
            hex += newChar
        return str(hex) + '-' + str(wall) + '-' + str(shelf) + '-' + str(int(volume))

    def get_page(self, address):
        addressArray = address.split('-')
        hex = addressArray[0]
        locHash = get_hash(
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
        self.seed = get_hash(result)
        while len(result) < self.lengthOfPage * 3:
            result += self.alphabet[int(self.rnd(0, len(self.alphabet)))]
        return result[len(result) - self.lengthOfPage * 3:]

    def get_title(self, address):
        addressArray = address.split('-')
        hex = addressArray[0]
        hex = [hex[j: j + 3] for j in range(0, len(hex), 3)]
        locHash = get_hash(addressArray[1] + addressArray[2] + str(pad(addressArray[3], 2)))
        result = ''
        self.seed = locHash
        for i in range(len(hex)):
            index = self.digsIndexes[hex[i]]
            rand = self.rnd(0, len(self.digs))
            newIndex = mod(index - int(rand), len(self.alphabet))
            newChar = self.alphabet[newIndex]
            result += newChar
        self.seed = get_hash(result)
        while len(result) < self.lengthOfTitle * 3:
            result += self.alphabet[int(self.rnd(0, len(self.alphabet)))]
        return self.in_readable_title(result[len(result) - self.lengthOfTitle * 3:])


babel = Babel()

# text, width, height = babel.create_str('im1.png')
# address = babel.search(text, width, height)
# babel.create_im(address, 'im.jpg')
# babel.create_im(babel.search_title('print(int(input()))') + '-1')

# babel.get_random_im('random.jpg')
