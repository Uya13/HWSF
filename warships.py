from typing import List
import random


class Dot:

    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, another_object) -> bool:

        if not isinstance(another_object, Dot):
            raise TypeError("Операнд справа должен иметь тип Dot")
 
        sc_x = another_object.x
        sc_y = another_object.y
        return self.x == sc_x and self.y == sc_y
        
    
class Ship:

    width: int
    dot_of_bow: Dot
    vertical_direction: bool
    count_of_life: int

    def __init__(self, width: int, dot_of_bow: Dot, vertical_direction: bool):
        self.width = width
        self.dot_of_bow = dot_of_bow
        self.vertical_direction = vertical_direction
        self.count_of_life = width

    def get_dots(self) -> List[Dot]:
        x = self.dot_of_bow.x
        y = self.dot_of_bow.y
        array: List[Dot] = []
        for i in range(0, self.width):
            array.append(Dot(x, y-i) if self.vertical_direction else Dot(x-i, y))
        array.reverse()
        return array


class Board:

    empty_dot_symbol = '○'
    not_empty_dot_symbol = '■'
    shot_symbol = 'X'
    miss_symbol = 'T'

    board_size = 6
    number_of_living_ships = 7
    board = []
    ships: List[Ship] = []
    shot_dots: List[Dot] = []

    hid: bool

    def __init__(self, hid: bool):
        
        self.board = []
        self.ships = []
        self.shot_dots = []
        self.hid = hid

        for i in range(0, self.board_size):
            self.board.append([])
            for _ in range(0, self.board_size):
                self.board[i].append(self.empty_dot_symbol)

    def out(self, dot: Dot) -> bool:
        if dot.x < 0 or dot.x > self.board_size - 1 or dot.y < 0 or dot.y > self.board_size - 1:
            return True
        else:
            return False

    @staticmethod
    def contour(ship: Ship) -> List[Dot]:
        contour: List[Dot] = []
        for dot in ship.get_dots():

            x = dot.x
            y = dot.y

            for i in range(x-1, x+1 + 1):
                for j in range(y-1, y+1 + 1):
                    new_dot = Dot(i, j)
                    if new_dot not in contour:
                        contour.append(new_dot)

        return contour

    def add_ship(self, ship: Ship):
        ship_dots = ship.get_dots()
        try:                
            for dot in ship_dots:
                if self.out(dot):
                    raise TypeError()

            ships_contour: List[Dot] = []
            for s in self.ships:
                ship_contour = self.contour(s)
                for contour_dot in ship_contour:
                    if contour_dot in ships_contour:
                        continue
                    else:
                        ships_contour.append(contour_dot)

            for dot in ship_dots:
                if dot in ships_contour:
                    raise TypeError()

            self.ships.append(ship)

        except Exception:
            raise TypeError()

    def shot(self, dot: Dot):
        try:
            if self.out(dot):
                raise TypeError("\nВыстрел за границу поля")
            
            if dot in self.shot_dots:
                raise TypeError("\nВыстрел в точку, в которую ранее уже была произведена попытка выстрела")
            
            for ship in self.ships:
                if dot in ship.get_dots():
                    ship.count_of_life -= 1

            self.shot_dots.append(dot)

        except Exception as e:
            raise TypeError(e)

    def print_board(self):

        top_str = '  | '
        for number_of_row in range(0, len(self.board)):
            top_str += str(number_of_row + 1) + ' | '
        print(top_str)

        for i, row in enumerate(self.board):

            column_str = str(i + 1) + ' | '

            for y, _ in enumerate(row):

                another_is_set = False

                if not self.hid:
                    for ship in self.ships:
                        if Dot(y, i) in ship.get_dots():
                            column_str += self.not_empty_dot_symbol + ' | '
                            another_is_set = True

                for shot in self.shot_dots:
                    dot = Dot(y, i)
                    if dot == shot:
                        is_ship_shot = False
                        for ship in self.ships:
                            if dot in ship.get_dots():
                                if not self.hid:
                                    new_str = self.shot_symbol + ' | '
                                    column_str = column_str[:len(column_str) - len(new_str)] + new_str
                                else:
                                    column_str += self.shot_symbol + ' | '
                                is_ship_shot = True

                        if not is_ship_shot:
                            column_str += self.miss_symbol + ' | '

                        another_is_set = True

                if not another_is_set:
                    column_str += self.empty_dot_symbol + ' | '

            print(column_str)


class Player:
    
    board: Board
    enemyBoard: Board

    def __init__(self):
        self.board = Board(False)

    def ask(self):
        pass

    def move(self):
        self.ask()


class AI(Player):

    def ask(self):
        dot = Dot(random.randint(0, self.board.board_size), random.randint(0, self.board.board_size))
        # noinspection PyBroadException
        try:
            self.enemyBoard.shot(dot)
        except Exception:
            self.ask()


class User(Player):

    def ask(self):
        try: 
            x = int(input('\nВведите координату X для выстрела: '))
            y = int(input('Введите координату Y для выстрела: '))

            dot = Dot(x-1, y-1)

            self.enemyBoard.shot(dot)
        except Exception as e:
            print(e)
            self.ask()


class Game:

    user: User
    ai: AI

    def __init__(self):
        self.user = User()
        self.ai = AI()
        self.user.enemyBoard = self.ai.board
        self.user.enemyBoard.hid = True
        self.ai.enemyBoard = self.user.board

    def random_board(self):
        self.random_board_for_user()
        self.random_board_for_ai()

    def random_board_for_user(self):

        count_of_ships = 0
        count_of_iterations = 0

        while True:

            count_of_iterations += 1

            x = random.randint(0, self.user.board.board_size)
            y = random.randint(0, self.user.board.board_size)
            dot_of_bow = Dot(x, y)
            vertical_direction = random.randint(0, 1)
            ship: Ship

            if count_of_ships == 0:
                ship = Ship(3, dot_of_bow, True if vertical_direction == 1 else False)
            elif 1 <= count_of_ships <= 2:
                ship = Ship(2, dot_of_bow, True if vertical_direction == 1 else False)
            elif 3 <= count_of_ships <= 7:
                ship = Ship(1, dot_of_bow, True if vertical_direction == 1 else False)
            else:
                ship = Ship(0, dot_of_bow, True)

            # noinspection PyBroadException
            try:
                self.user.board.add_ship(ship)
                count_of_ships += 1
            except Exception:
                continue
        
            if count_of_ships == 7:
                break

            if count_of_iterations > 3000:
                self.user.board = Board(False)
                self.random_board_for_user()
                return
            
    def random_board_for_ai(self):

        count_of_ships = 0
        count_of_iterations = 0

        while True:

            count_of_iterations += 1

            x = random.randint(0, self.ai.board.board_size)
            y = random.randint(0, self.ai.board.board_size)
            dot_of_bow = Dot(x, y)
            vertical_direction = random.randint(0, 1)
            ship: Ship

            if count_of_ships == 0:
                ship = Ship(3, dot_of_bow, True if vertical_direction == 1 else False)
            elif 1 <= count_of_ships <= 2:
                ship = Ship(2, dot_of_bow, True if vertical_direction == 1 else False)
            elif 3 <= count_of_ships <= 7:
                ship = Ship(1, dot_of_bow, True if vertical_direction == 1 else False)
            else:
                ship = Ship(0, dot_of_bow, True)

            # noinspection PyBroadException
            try:
                self.ai.board.add_ship(ship)
                count_of_ships += 1
            except Exception:
                continue
        
            if count_of_ships == 7:
                break

            if count_of_iterations > 3000:
                self.ai.board = Board(False)
                self.random_board_for_user()
                return

    @staticmethod
    def greet():
        print('\nПривет!')
        print('Это морской бой. Попробуй обыграть AI вводя координаты X и Y, куда хотите выстрелить')

    def print_boards(self):
        print('\nДоска AI')
        self.ai.board.print_board()
        print('\nДоска пользователя')
        self.user.board.print_board()

    def loop(self):

        self.print_boards()

        is_user_turn = True

        while True:

            if is_user_turn:
                self.user.move()
                print('\nДоска AI')
                self.user.enemyBoard.print_board()
            else:
                self.ai.move()
                print('\nДоска пользователя')
                self.ai.enemyBoard.print_board()

            is_user_win = True
            for ship in self.user.enemyBoard.ships:
                if ship.count_of_life != 0:
                    is_user_win = False
                    break
            if is_user_win:
                print('\nПобеда пользователя!')
                return
            
            is_ai_win = True
            for ship in self.ai.enemyBoard.ships:
                if ship.count_of_life != 0:
                    is_ai_win = False
                    break
            if is_ai_win:
                print('\nПобеда AI!')
                return      

            is_user_turn = False if is_user_turn else True

    def start(self):
        self.random_board()
        self.greet()
        self.loop()


game = Game()
game.start()
