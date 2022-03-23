# # print(len(str(4096 ** (640 * 416 // 4))))  # 240439
# print(len(str(4096 ** 66560)))
# # количество страниц в книге - 256
# # количество книг на полке - 32
# # количество полок на стеллаже - 8
# # количество стеллажей в комнате - 5
# # название книги - номер комнаты в сс с основанием 16; хэшированный номер стеллажа; хэшированный номер полки; хэшированный номер книги
# # название страницы - название книги; ъэшированный номер страницы
# # m = '111222333'
# # searchStr = [m[j: j + 3] for j in range(0, len(m), 3)]
# # print(searchStr)
# print('a' * 3300)
with open('data/readable_alphabet.txt', 'r', encoding='utf-8') as f:
    f = "'".join(list(filter(lambda x: x, ''.join(''.join(f.read().split(',')).split(' ')).split("'"))))
with open('data/readable_alphabet.txt', 'w', encoding='utf-8') as f1:
    print(f, file=f1)