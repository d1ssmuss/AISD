import sys


def main():
    n = list(map(int, input("Введите числа: ").split()))
    n.sort()
    x,y,z = 0,0,0
    # переменная которая берёт произведение последних 3-х чисел
    proz_pos = n[-1] * n[-2] * n[-3]
    proz_min = 0
    if (n[0] * n[1]) > 0 and (n[0] * n[1] * n[-1]) > (proz_pos):
        x,y,z = n[-1], n[1], n[0]
    else:
        x,y,z = n[-1], n[-2], n[-3]
    print(x,y,z)


if __name__ == '__main__':
    main()
