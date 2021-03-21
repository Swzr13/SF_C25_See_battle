from random import randint
from Exeption import *

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'

class Ships:
    def __init__(self, bow, length_s, orient):
        self.bow = bow
        self.length_s = length_s
        self.orient = orient
        self.life = length_s

    @property
    def dots(self):
        ship_dots = []
        cur_x = self.bow.x
        cur_y = self.bow.y
        for i in range(self.length_s):
            # 0 - горизонталь, 1 - вертикаль
            if self.orient == 0:
                cur_x += 1
            elif self.orient == 1:
                cur_y += 1
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots



class Board:
    def __init__(self, size = 10, hide = True):
        self.size = size
        self.hide = hide

        self.count = 0
        self.field = [['o'] * size for _ in range(size)]

        self.buzy = []
        self.ships = []

    def out(self, dot_r):
        return not((0 <= dot_r.x < self.size) and (0 <= dot_r.y < self.size))

    def pain_char(self, d, ch):
        self.field[d.x][d.y] = ch

    def contur(self, ship, vef=False):
       near = [
           (-1, -1), (-1, 0), (-1, 1),
           (0, -1), (0, 0), (0, 1),
           (1, -1), (1, 0), (1, 1)
       ]
       for d in ship.dots:
           for dx, dy in near:
               cur = Dot(d.x + dx, d.y + dy)
               if not(self.out(cur)) and not cur in self.buzy:
                   if vef:
                       self.pain_char(cur, '\033[33m*\033[0m')
                       # self.pain_char(cur, '*')
               self.buzy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.buzy:
                raise BoardWrongShipException
        for d in ship.dots:
            self.pain_char(d, '\033[96m■\033[0m')
            # self.pain_char(d, '■')
            self.buzy.append(d)

        self.ships.append(ship)
        self.contur(ship)

    def shot(self, d):
        if self.out(d):
            raise BoarOutException

        if d in self.buzy:
            raise BoardUsedException

        self.buzy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.life -= 1
                self.pain_char(d,'\033[31mX\033[0m')
                # self.pain_char(d,'X')
                if ship.life == 0:
                    self.count += 1
                    self.contur(ship, True)
                    print('Корабль потоплен!!!')
                    return False
                else:
                    print("Ранен")
                    return True
        self.pain_char(d, '.')
        return False

    def begin(self):
        self.buzy = []

    def game_over(self):
        return self.count == 10

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardExeption as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Dot(randint(0, 9), randint(0, 9))
        print(f'Ход компьютера: {d.x+1} {d.y+1}')
        return d

class User(Player):

    def true_coord(self, d_move):
        rez = True
        if len(d_move) != 2 or not(d_move[0].isdigit()) or not(d_move[1].isdigit()):
            print(' Введите 2 числа! x - строка, y - столбец ')
            rez = False
        return rez


    def ask(self):
        while True:
            d_move = input('Введите ход: ').split()

            if not(self.true_coord(d_move)): continue
            x, y = d_move
            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=10):
        self.size = size
        board_player = self.random_board()
        board_AI = self.random_board()

        self.ai = AI(board_AI, board_player)
        self.user = User(board_player, board_AI)

    def print_boards(self):
        board_player = self.user.board
        board_AI = self.ai.board

        s = "   "
        for i in range(self.size):
            s += f'| {i + 1} '
        s += '|  ||  ' + s + '|'
        len_s = len(s)
        s += '\n' + '_' * len_s
        s = "   Доска игрока" + ' '*(len_s//2 - 16) + '||     Доска компьютера\n' + s
        i = 1
        for b_p, b_ai in zip(board_player.field, board_AI.field):
            num_p = '  ' if i < 10 else ' '
            s += f'\n{i}{num_p}| ' + ' | '.join(b_p) + ' |   ||  ' + f'{i}{num_p}| ' + ' | '.join(b_ai).replace("■", "\033[38mo\033[0m") + ' |'
            i += 1
        s += '\n' + '_' * len_s
        print(s)

    def try_board(self):
        line_ship = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        board = Board(size=10)
        count = 0
        for l_ship in line_ship:
            while True:
                count += 1
                if count > 3000:
                    return None
                ship = Ships(Dot(randint(0, self.size),randint(0, self.size)), l_ship,randint(0,1) )
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            if num % 2 == 0:
                self.print_boards()
                print("Ходит пользователь!")
                repeat = self.user.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.game_over():
                print("Пользователь выиграл!")
                break

            if self.user.board.game_over():
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()
