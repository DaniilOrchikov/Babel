import base64
import hashlib
import io
import random
from PIL import Image
import numpy as np


def create_alf(used_symbols):
    alphabet = []
    for r in enumerate(used_symbols):
        for g in enumerate(used_symbols):
            for b in enumerate(used_symbols):
                alphabet.append(r[1] + g[1] + b[1])
    r = []
    v = 0
    while len(r) < len(alphabet):
        a = chr(v)
        try:
            with open('readable_alphabet1.txt', 'w', encoding='utf-8') as f:
                print(a, file=f)
        except UnicodeEncodeError:
            v += 1
            continue
        if len(a) == 1 and a != '\n' and a != "'" and a != '\\' and a != ' ' and a not in '/┫' and a.isprintable():
            r.append(a)
        v += 1
    random.shuffle(r)
    with open('readable_alphabet1.txt', 'w', encoding='utf-8') as f:
        print(r, file=f)


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
        self.used_symbols = '0123456789abcdefghijklmnopqrstuv'  # нельзя использовать '-'
        self.number_of_colors = len(self.used_symbols)
        # create_alf(self.used_symbols) # не забывать вставлять пробельный символ

        with open('static/txt/alphabet.txt', 'r') as f:
            self.alphabet = self.digs = f.read().split()
        with open('static/txt/readable_alphabet.txt', 'r', encoding='utf-8') as f:
            self.readable_alphabet = f.read().split("'")
        self.alphabet.insert(0, self.alphabet.pop())
        self.alphabet_len = len(self.alphabet)
        self.lengthOfTitle = 31

        self.width, self.height = 240, 160
        self.lengthOfPage = self.width * self.height

        self.wall = 4
        self.shelf = 20
        self.volume = 32
        self.page = 410

        self.number_of_pages = len(str(self.alphabet_len ** (self.width * self.height)))

        self.digsIndexes = {}
        self.alphabetIndexes = {}
        self.readable_alphabetIndexes = {}
        self.create_indexes()
        print(len(self.readable_alphabetIndexes), len(self.alphabetIndexes))
        # print(self.readable_alphabet)

    def search_by_location(self, hex, wall, shelf, volume, page):
        return self.alphabet[0] * (111600 - len(hex)) + str(hex) + '-' + str(wall) + '-' + str(shelf) + '-' + str(
            int(volume)) + '-' + str(int(page))

    def from_readable_title(self, title):
        title += ' ' * (self.lengthOfTitle - len(title))
        new_title = ''
        for i in title:
            new_title += self.alphabet[self.readable_alphabetIndexes[i]]
        return new_title

    def in_readable_title(self, title):
        new_title = ''
        for i in range(0, len(title), 3):
            new_title += self.readable_alphabet[self.alphabetIndexes[title[i: i + 3]]]
        return new_title

    def create_str(self, image):
        im = Image.open(io.BytesIO(image))
        width, height = im.size
        if width > self.width and height > self.height:
            if width / self.width > height / self.height:
                im = im.resize((self.width, int(self.width / width * height)), Image.NEAREST)
            else:
                im = im.resize((int(self.height / height * width), self.height), Image.NEAREST)
        elif width > self.width:
            im = im.resize((self.width, int(self.width / width * height)), Image.NEAREST)
        elif height > self.height:
            im = im.resize((int(self.height / height * width), self.height), Image.NEAREST)
        pix = im.load()
        width, height = im.size
        st = ''
        for i in range(height):
            for j in range(width):
                if not str(pix[j, i]).isdigit():
                    if len(pix[j, i]) == 3:
                        r, g, b = pix[j, i]
                        r, g, b = r // (256 // self.number_of_colors), \
                                  g // (256 // self.number_of_colors), \
                                  b // (256 // self.number_of_colors)
                    else:
                        r, g, b, h = pix[j, i]
                        r, g, b = r // (256 // self.number_of_colors), \
                                  g // (256 // self.number_of_colors), \
                                  b // (256 // self.number_of_colors)
                else:
                    return 'wrong_pixel', None, None
                st += self.used_symbols[r] + self.used_symbols[g] + self.used_symbols[b]
        return st, width, height

    def create_im(self, address):
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
                pix[j, i] = self.used_symbols.index(m[i][j][0]) * (256 // self.number_of_colors), \
                            self.used_symbols.index(m[i][j][1]) * (256 // self.number_of_colors), \
                            self.used_symbols.index(m[i][j][2]) * (256 // self.number_of_colors)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return base64.b64encode(img_byte_arr)

    def rnd(self, mn=1, mx=0):
        m, a, c = 2 ** 32, 22695477, 1
        self.seed = (self.seed * a + c) % m
        return mn + self.seed / m * (mx - mn)

    def create_indexes(self):
        for pos, char in enumerate(self.digs):
            self.digsIndexes[char] = pos
        for pos, char in enumerate(self.alphabet):
            self.alphabetIndexes[char] = pos
        for pos, char in enumerate(self.readable_alphabet):
            self.readable_alphabetIndexes[char] = pos

    def get_random(self):
        title = [self.readable_alphabet[random.randrange(0, len(self.digs))] for _ in range(self.lengthOfTitle)]
        address = self.search_title(title) + '-' + str(random.randint(1, self.page))
        return address

    def search(self, search_str, width, height):
        wall = str(int(random.random() * self.wall + 1))
        shelf = str(int(random.random() * self.shelf + 1))
        volume = pad(str(int(random.random() * self.volume + 1)), 2)
        page = pad(str(int(random.random() * self.page + 1)), 3)
        locHash = get_hash(wall + shelf + volume + page)
        hex = ''
        w = random.randint(0, self.width - width)
        h = random.randint(0, self.height - height)
        search_str = [search_str[j: j + 3] for j in range(0, len(search_str), 3) if len(search_str[j: j + 3]) == 3]
        searchArr = [list(i) for i in np.array(search_str).reshape(height, width)]
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
        search_str = np.array(searchArr).flatten()
        self.seed = locHash
        for i in range(len(search_str)):
            index = self.alphabetIndexes[search_str[i]] or -1
            rand = self.rnd(0, len(self.alphabet))
            newIndex = mod(index + int(rand), len(self.digs))
            newChar = self.digs[newIndex]
            hex += str(newChar)
        return str(hex) + '-' + str(wall) + '-' + str(shelf) + '-' + str(int(volume)) + '-' + str(int(page))

    def search_exactly(self, search_str, width, height):
        w = random.randint(0, self.width - width)
        h = random.randint(0, self.height - height)
        search_str = [search_str[j: j + 3] for j in range(0, len(search_str), 3) if len(search_str[j: j + 3]) == 3]
        searchArr = [list(i) for i in np.array(search_str).reshape(height, width)]
        if w:
            for i in range(height):
                for j in range(w):
                    searchArr[i].insert(0, self.alphabet[-1])
        if h:
            for i in range(h):
                searchArr.insert(0, [])
                for j in range(w + width):
                    searchArr[0].append(self.alphabet[-1])
        for i in range(self.height - height - h):
            searchArr.append([])
            for j in range(width + w):
                searchArr[-1].append(self.alphabet[-1])
        for i in range(self.height):
            for j in range(self.width - width - w):
                searchArr[i].append(self.alphabet[-1])
        search_str = ''.join(np.array(searchArr).flatten())
        return self.search(search_str, self.width, self.height)

    def search_title(self, search_str):
        search_str = self.from_readable_title(search_str)
        wall = str(int(random.random() * self.wall + 1))
        shelf = str(int(random.random() * self.shelf + 1))
        volume = pad(str(int(random.random() * self.volume + 1)), 2)
        locHash = get_hash(str(wall) + str(shelf) + str(volume))
        hex = ''
        search_str = search_str[:self.lengthOfTitle * 3]
        # searchStr = searchStr if len(searchStr) == self.lengthOfTitle * 3 else str(searchStr) + '00u' * (
        #         self.lengthOfTitle - len(searchStr) // 3)
        self.seed = locHash
        search_str = [search_str[j: j + 3] for j in range(0, len(search_str), 3)]
        for i in range(len(search_str)):
            index = self.alphabetIndexes[search_str[i]]
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
