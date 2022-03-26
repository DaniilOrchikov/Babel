with open('readable_alphabet.txt', 'r', encoding='utf-8') as f:
    f = "'".join(list(filter(lambda x: x, ''.join(''.join(f.read().split(',')).split(' ')).split("'"))))
with open('readable_alphabet.txt', 'w', encoding='utf-8') as f1:
    print(f, file=f1)
