def game():
    print('')
    print('▬▬▬▬▬▬▬▬▬▬▬▬')
    print('  Крестики-нолики.')
    print('▬▬▬▬▬▬▬▬▬▬▬▬')
    print('')
    print(' ', '|', '0', '|', '1', '|', '2', '|')
    print('.................')
    for i in range(3):
        print(i, '|', field[i][0], '|', field[i][1], '|', field[i][2], '|')
        print('.................')


field = [[' '] * 3 for i in range(3)]


def decision():
    while True:
        try:
            x = int(input('Введите номер строки (0, 1, 2): '))
            y = int(input('Введите номер столбца (0, 1, 2): '))
        except ValueError:
            print('Введите числа!!!')
            continue

        if 0 > x or x > 2 or 0 > y or y > 2:
            print('Недопустимые данные!!!')
            continue

        if field[x][y] != ' ':
            print('Поле уже заполнено!!!')
            continue
        return x, y


def res():
    for i in range(3):
        List = []
        for j in range(3):
            List.append(field[i][j])
        if List == ['x', 'x', 'x']:
            print('Выиграл крестик!')
            return True
        if List == ['0', '0', '0']:
            print('Выиграл нолик!')
            return True

    for i in range(3):
        List = []
        for j in range(3):
            List.append(field[j][i])
        if List == ['x', 'x', 'x']:
            print('Выиграл крестик!')
            return True
        if List == ['0', '0', '0']:
            print('Выиграл нолик!')
            return True

    List = []
    for i in range(3):
        List.append(field[i][i])
    if List == ['x', 'x', 'x']:
        print('Выиграл крестик!')
        return True
    if List == ['0', '0', '0']:
        print('Выиграл нолик!')
        return True

    List = []
    for i in range(3):
        List.append(field[i][2 - i])
    if List == ['x', 'x', 'x']:
        print('Выиграл крестик!')
        return True
    if List == ['0', '0', '0']:
        print('Выиграл нолик!')
        return True



motion = 0
while True:
    motion += 1
    game()

    if motion % 2 != 0:
        print('Ход x: ')
    else:
        print('Ход 0: ')

    x, y = decision()

    if motion % 2 != 0:
        field[x][y] = 'x'
    else:
        field[x][y] = '0'

    if res():
        break

    if motion == 9:
        print('Ничья.')
        break

