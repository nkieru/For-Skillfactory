from random import randint, choice

class BoardException(Exception):
    pass

class BoardShipExeption(BoardException):
    pass

class BoardChangedException(BoardException):
    def __str__(self):
        return f'Точка уже занята'

class BoardOutException(BoardException):
    def __str__(self):
        return f'На доске нет точки с такими координатами'


class BoardShotException(BoardException):
    def __str__(self):
        return f'В эту клетку уже стреляли'

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class Ship:

    def __init__(self, l, bow, orient):
        self.l = l
        self.bow = bow
        self.orient = orient
        self.Life = l

    @property
    def dots(self):
        ship_dots = []
        for dot in range(self.l):
            bow_x = self.bow.x
            bow_y = self.bow.y
            if self.orient == 'По вертикали':
                bow_x += dot
            if self.orient == 'По горизонтали':
                bow_y += dot
            ship_dots.append(Dot(bow_x, bow_y))
        return ship_dots


    def hit(self, Hit):
        return Hit in self.dots

class Board:
    def __init__(self, hid = False, size = 6):
        self.size = size
        self.hid = hid
        self.List_of_dots = [['○'] * size for i in range(size)]
        self.List_of_ships = []
        self.Changed_dots = []
        self.count = 0

    def __str__(self):
        board_str = ''
        count = 1
        for dot in range(self.size):
            board_str += f'| {count} '
            count += 1
        board_str = ' ' + ' ' + board_str + '|'
        print('        Морской бой        ')
        print('▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬')
        for i, j in enumerate(self.List_of_dots):
            board_str += f'\n{i + 1} | ' + ' | '.join(j) + ' |'
        if self.hid:
            board_str = board_str.replace('■', '○')
            board_str = board_str.replace('•', '○')
        return board_str


    def add_ship(self, Ship):
        for a in Ship.dots:
            if self.out(a) or a in self.Changed_dots:
                raise BoardShipExeption()
        for a in Ship.dots:
            self.List_of_dots[a.x][a.y] = '■'
            self.Changed_dots.append(a)
        self.List_of_ships.append(Ship)
        self.contour(Ship)

    def contour(self, Ship, outline = False):
        self.outline = outline
        around = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for a in Ship.dots:
            for ax, ay in around:
                dots_around = Dot(a.x + ax, a.y + ay)
                if dots_around not in self.Changed_dots and self.size > dots_around.x >= 0 and self.size > dots_around.y >= 0:
                    if outline:
                        self.List_of_dots[dots_around.x][dots_around.y] = '•'
                    self.Changed_dots.append(dots_around)

    def out(self, a):
        return self.size <= a.x or a.x < 0 or self.size <= a.y or a.x < 0

    def start(self):
        self.Changed_dots = []

    def shot(self, a):
        if self.out(a):
            raise BoardOutException()
        if a in self.Changed_dots:
            raise BoardChangedException()

        self.Changed_dots.append(a)

        for ship in self.List_of_ships:
            if ship.hit(a):
                ship.Life -= 1
                self.List_of_dots[a.x][a.y] = 'x'
                if ship.Life == 0:
                    self.count += 1
                    self.contour(Ship, outline = True)
                    print('Убит')
                    return True
                else:
                    print('Ранен')
                    return True

        self.List_of_dots[a.x][a.y] = '•'
        print('Мимо')
        return False


class Game:
    def __init__(self, size = 6):
        self.size = size


    def random_board(self):
        random_ships = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        count = 0
        for t in random_ships:
            while True:
                count += 1
                if count > 5000:
                    return 'Превышено количество попыток для создания доски'
                ship = Ship(t, choice(['По вертикали', 'По горизонтали']), Dot(randint(0, self.size), randint(0, self.size)))
                try:
                    board.add_ship(ship)
                    break
                except BoardShipExeption:
                    pass
        board.start()
        return board

# Не создается рандомная доска:
g = Game()
print(g.random_board())

# b = Board()
# print(b)
# s = Ship(3, Dot(1, 1), 'По горизонтали')
# b.add_ship(s)
# print(b)
# #Невозможно выстрелить,тк не облуляется список  self.Changed_dots = []:
# print(b.shot(Dot(1, 1)))



