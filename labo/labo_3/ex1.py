from random import randint
# Q2
import os
# Q2


class Board:
    def __init__(self, player, size=6):
        self._player = player
        self._size = size
        self._walls = []

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, new_player):
        self._player = new_player

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        self._size = new_size

    @property
    def walls(self):
        return self._walls

    @walls.setter
    def walls(self, new_walls):
        self._walls = new_walls

    def draw(self):
        case_empty = '.'
        case_wall = 'X'
        case_player = 'O'

        board = ""

        for line in range(self._size):
            for colum in range(self._size):

                coordinate = (line, colum)
                if coordinate in self._walls:
                    board += case_wall

                elif coordinate == self.player.position:
                    board += case_player

                else:
                    board += case_empty

            board += '\n'

        print(board)

    def pop_wall(self):
        new_wall = (randint(0, self._size - 1), randint(0, self._size - 1))
        if ((new_wall not in self._walls)
                and (new_wall != self.player.position)):
            self._walls.append(new_wall)

    def check_death(self):
        player_pos = self.player.position

        check_x = 0 <= player_pos[0] < self._size
        check_y = 0 <= player_pos[1] < self._size
        check_walls = player_pos not in self._walls

        return not (check_x and check_y and check_walls)

    def check_win(self):
        return self.player.position == (self.size - 1, self.size - 1)

    def play_game(self):
        self.draw()
        while not (self.check_win() or self.check_death()):
            self.player.move()
            self.pop_wall()
            self.draw()

        if self.check_win():
            print("GG")
            print(f"Point: {self.player.point}")

        else:
            self.player.point = 0
            print("Lost")
            print(f"Point: {self.player.point}")

        # Q2
        if os.path.isfile("./scoreboard.txt"):
            with open("./scoreboard.txt", "r+") as score_file:
                record = score_file.read()

                player_score = f"{self.player.name}:{self.player.point}\n"
                if record == "":
                    score_file.write(player_score)

                else:
                    high_score = record.split(":")[1][:-1]
                    if int(high_score) < self.player.point:
                        score_file.seek(0)
                        score_file.write(player_score)

        else:
            with open("./scoreboard.txt", mode="w") as score_file:
                record = f"{self.player.name}:{self.player.point}\n"
                score_file.write(record)
        # Q2


class Player:

    keyboard_key = {
        'z': (-1, 0),
        'q': (0, -1),
        's': (1, 0),
        'd': (0, 1)
    }

    def __init__(self, name):
        self._name = name
        self._position = (0, 0)
        # Q1
        self._point = 30
        # Q1

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, new_point):
        self._point = new_point

    def move(self):
        keys = Player.keyboard_key.keys()

        key_pressed = input("Move: ")
        while key_pressed not in keys:
            key_pressed = input("Move: ")

        direction = Player.keyboard_key[key_pressed]

        player_x = self._position[0] + direction[0]
        player_y = self._position[1] + direction[1]
        self._position = (player_x, player_y)

        # Q1
        self._point -= 1
        # Q1


if __name__ == "__main__":
    p1 = Player("WaffleSlayer")
    board = Board(p1, 10)
    board.play_game()
