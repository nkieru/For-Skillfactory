from random import randint

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

    def __init__(self, bow, l, orient):
        self.bow = bow
        self.l = l
        self.orient = orient
        self.Life = l

    @property
    def dots(self):
        ship_dots = []
        for dot in range(self.l):
            bow_x = self.bow.x
            bow_y = self.bow.y
            if self.orient == 0:
                bow_x += dot
            if self.orient == 1:
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
        self.count = 7

    def __str__(self):
        board_str = ''
        count = 1
        for dot in range(self.size):
            board_str += f'| {count} '
            count += 1
        board_str = ' ' + ' ' + board_str + '|'
        for i, j in enumerate(self.List_of_dots):
            board_str += f'\n{i + 1} | ' + ' | '.join(j) + ' |'
        if self.hid:
            board_str = board_str.replace('■', '○')
        return board_str

    def add_ship(self, ship):
        for a in ship.dots:
            if self.out(a) or a in self.Changed_dots:
                raise BoardShipExeption()
        for a in ship.dots:
            self.List_of_dots[a.x][a.y] = '■'
            self.Changed_dots.append(a)
        self.List_of_ships.append(ship)
        self.contour(ship)

    def contour(self, ship, outline = False):
        around = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for a in ship.dots:
            for ax, ay in around:
                dots_around = Dot(a.x + ax, a.y + ay)
                if not(self.out(dots_around)) and dots_around not in self.Changed_dots:
                    if outline:
                        self.List_of_dots[dots_around.x][dots_around.y] = '•'
                    self.Changed_dots.append(dots_around)

    def out(self, a):
        return not ((0 <= a.x < self.size) and (0 <= a.y < self.size))

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
                    self.count -= 1
                    self.contour(ship, outline = True)
                    print('Убит')
                    return True
                else:
                    print('Ранен')
                    return True
        self.List_of_dots[a.x][a.y] = 'T'
        print('Мимо')
        return False

    def clean(self):
        self.Changed_dots = []


class Player:

    def __init__(self, board, comp_board):
        self.board = board
        self.comp_board = comp_board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                Ask = self.ask()
                Back = self.comp_board.shot(Ask)
                return Back
            except BoardException as e:
                print(e)


class AI(Player):

    def ask(self):
        return Dot(randint(0, 5), randint(0, 5))


class User(Player):

    def ask(self):
        while True:
            try:
                user_y = int(input('Введите номер столбца: '))
                user_x = int(input('Введите номер строки: '))
            except ValueError:
                print('Введите числа!!!')
                continue
            x = user_x
            y = user_y
            return Dot(x - 1, y - 1)


class Game:

    def __init__(self, size = 6):
        self.size = size
        user = self.game_board()
        comp = self.game_board()
        self.comp_game = AI(comp, user)
        self.user_game = User(user, comp)
        comp.hid = True

    def game_board(self):
        board = None
        while board is None:
            board = self.random_board()
        return board

    def random_board(self):
        random_ships = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        count = 0
        for l in random_ships:
            while True:
                count += 1
                if count > 5000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardShipExeption:
                    pass
        board.clean()
        return board

    def greet(self):
        print('____________________________')
        print('    Приветствуем в игре            ')
        print('____________________________')
        print('        Морской бой        ')
        print('▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬')

    def loop(self):
        num = 0
        while True:
            print('Игрок: ')
            print(self.user_game.board)
            print('Компьютер: ')
            print(self.comp_game.board)
            if num % 2 == 0:
                print('Ход игрока ')
                Back = self.user_game.move()
            else:
               print('Ход компьютера')
               Back = self.comp_game.move()
            if Back:
                num -= 1
            if self.comp_game.board.count == 0:
                print('▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬')
                print('         ИТОГ ИГРЫ: ')
                print('       победил игрок')
                print('▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬')
                print('Игрок: ')
                print(self.user_game.board)
                print('Компьютер: ')
                print(self.comp_game.board)
                break
            if self.user_game.board.count == 0:
                print('▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬')
                print('         ИТОГ ИГРЫ: ')
                print('     победил компьютер')
                print('▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬')
                print('Игрок: ')
                print(self.user_game.board)
                print('Компьютер: ')
                print(self.comp_game.board)
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()