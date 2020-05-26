import random
import datetime

# TODO Enemies AI


def clamp(value, min_value, max_value):

    if value > max_value:
        value = max_value

    elif value < min_value:
        value = min_value

    return value


class Entity:

    def __init__(self, position):
        self._position = position
        self._previous_position = position

    @property
    def position(self):
        return self._position

    @property
    def previous_position(self):
        return self._previous_position

    def move(self, move_vector, board_size):

        new_position = (self._position[0] + move_vector[0],
                        self._position[1] + move_vector[1])

        if new_position[0] < 0:
            new_position = (board_size - 1, new_position[1])

        elif new_position[0] > board_size - 1:
            new_position = (0, new_position[1])

        if new_position[1] < 0:
            new_position = (new_position[0], board_size - 1)

        elif new_position[1] > board_size - 1:
            new_position = (new_position[0], 0)

        if self._previous_position != new_position:
            self._previous_position = self._position
            self._position = new_position


class Player(Entity):

    keyboard_key = {'z': (-1, 0),
                    'q': (0, -1),
                    's': (1, 0),
                    'd': (0, 1),
                    'p': None,
                    'r': None,
                    'quit': None}

    def __init__(self, name, start=(0, 0)):

        super().__init__(start)

        self._name = name
        self._points = 0
        self._tail = []
        self._lock_tail = False
        self._has_paused = False
        self._has_quit = False
        self._is_catch = False

    @property
    def name(self):
        return self._name

    @property
    def points(self):
        return self._points

    @property
    def tail(self):
        return self._tail

    @property
    def lock_tail(self):
        return self._lock_tail

    @property
    def has_paused(self):
        return self._has_paused

    @property
    def has_quit(self):
        return self._has_quit

    @property
    def is_catch(self):
        return self._is_catch

    @is_catch.setter
    def is_catch(self, is_catch):
        self._is_catch = is_catch

    def get_input(self, board_size):
        text = "Pause: p | Resume: r\nQuit: quit\nMouvement (z,q,s,d): "

        key = input(text)
        while key not in Player.keyboard_key.keys():
            key = input(text)

        if Player.keyboard_key[key]:
            move = Player.keyboard_key[key]

            self.move(move, board_size)

        elif key == "quit":
            self._has_quit = True

        elif key == "p":
            self._has_paused = True

        elif key == 'r':
            self._has_paused = False

    def bite_tail(self):
        return self.position in self.tail

    def add_points(self, points):
        self._points += points
        self.grow_tail()

    def grow_tail(self):
        self._tail.insert(0, self.previous_position)
        self._lock_tail = True

    def move_tail(self):
        if not self._lock_tail:
            self._tail.insert(0, self.previous_position)
            self._tail.pop()

        else:
            self._lock_tail = False


class Enemy(Entity):

    Direction = ((1, 0),
                 (0, 1),
                 (-1, 0),
                 (0, -1))

    def __init__(self, position):
        super().__init__(position)

    # Déplace l'enemi
    def chasse_player(self, board_size):
        self.move(random.choice(Enemy.Direction), board_size)


class Game:

    mode = {"Peacefull": {"spawn": 0, "multi": 1, "time": (5, 0)},
            "Esay": {"spawn": 10, "multi": 2, "time": (3, 30)},
            "Medium": {"spawn": 20, "multi": 4, "time": (2, 0)},
            "Hard": {"spawn": 50, "multi": 10, "time": (1, 30)}}

    def __init__(self, player, level, size=10):
        self._player = player
        self._level = level
        self._board_size = size
        self._enemies = []
        self._candies = []
        self._candiesBonus = (-1, 1, 2, 3)
        self._time_end = None

    @property
    def player(self):
        return self._player

    @property
    def level(self):
        return self._level

    @property
    def board_size(self):
        return self._board_size

    @property
    def enemies(self):
        return self._enemies

    @property
    def candies(self):
        return self._candies

    @property
    def candiesBonus(self):
        return self._candiesBonus

    @property
    def time_end(self):
        return self._time_end

    # Dessine le plateau
    def draw(self, time_now):
        time_left = self.time_end - time_now

        minute_left = time_left.seconds // 60
        seconds_left = time_left.seconds - 60 * minute_left
        tenth_left = clamp(time_left.microseconds // 100_000, 0, 9)

        print(f"Time left: {minute_left}:{seconds_left}.{tenth_left}")
        print(f"Score {self.player.points}")

        for line in range(self.board_size):
            for col in range(self.board_size):
                if (line, col) in self.candies:
                    print("*", end=" ")

                elif (line, col) in self.enemies_position():
                    print("x", end=" ")

                elif (line, col) == self.player.position:
                    print("O", end=" ")

                elif (line, col) in self.player.tail:
                    print("o", end=" ")

                else:
                    print(".", end=" ")
            print()

        print("\n--------------------------")

    # Fait apparaitre un ou plusieurs bonbon
    def pop_candy(self, to_pop=1):

        for i in range(to_pop):
            new_candy = (random.choice(range(self.board_size)),
                         random.choice(range(self.board_size)))

            if new_candy not in self.candies:
                self._candies.append(new_candy)

    # Regarde s'il y a un bonbon à prendre (et le prend)
    def check_candy(self):

        if self.player.position in self.candies:
            points = random.choice(self.candiesBonus)
            self.player.add_points(points * Game.mode[self.level]["multi"])
            self.candies.remove(self.player.position)

            if random.randint(0, 100) <= 15:
                self.pop_candy(to_pop=random.randint(1, 3))

    # Spawn un enemie
    def spawn_enemy(self):

        new_enemy = (random.choice(range(self.board_size)),
                     random.choice(range(self.board_size)))

        if new_enemy != self.player.position:
            self._enemies.append(Enemy(new_enemy))

    # Donne la list de position des enemies
    def enemies_position(self):

        positions = []
        for enemy in self.enemies:
            positions.append(enemy.position)

        return positions

    # Regarde si un enemie a attraper le serpent
    def check_catch(self):
        self.player.is_catch = self.player.position in self.enemies_position()

    # Joue une partie complète
    def play(self):

        self._time_end = Game.end_time(*Game.mode[self.level]["time"])
        time_now = datetime.datetime.today()

        print("--- Début de la partie ---\n")
        self.draw(time_now)

        while (time_now < self._time_end and not self.player.has_quit
               and not self.player.bite_tail() and not self.player.is_catch):

            self.player.get_input(self.board_size)

            if not self.player.has_paused:
                self.check_candy()

                if random.randint(1, 3) == 1:
                    self.pop_candy()

                if (random.randint(1, 100) < Game.mode[self.level]["spawn"]):
                    self.spawn_enemy()

                self.player.move_tail()
                print(self.player.position)
                print(self.player.tail)

                for enemy in self.enemies:
                    enemy.chasse_player(self.board_size)

                self.check_catch()

                self.draw(time_now)

                time_now = datetime.datetime.today()

            else:
                time_left = self._time_end - time_now
                minute_left = time_left.seconds // 60
                second_left = time_left.seconds - minute_left * 60
                self._time_end = Game.end_time(minute_left, second_left)

        print("----- Terminé -----")
        if self.player.bite_tail():
            print("Tu as mordu ta queue !")

        elif self.player.is_catch:
            print("Tu as été attraper !")

        print("Vous avez", self.player.points, "points")

        self.save_result()

    def save_result(self):

        try:
            with open("scoreboard.txt", "r+") as scoreboard:
                player_records = scoreboard.readlines()

                records = []
                for player_record in player_records:
                    records.append(player_record[:-1].split(":"))

                index = 0
                while (index < len(records) and
                       int(records[index][1]) > self.player.points):
                    index += 1

                records.insert(index, (self.player.name, self.player.points))

                scoreboard.seek(0, 0)
                i = 0
                while i < 3 and i < len(records):
                    scoreboard.write(f"{records[i][0]}:{records[i][1]}\n")
                    i += 1

        except FileNotFoundError:
            with open("scoreboard.txt", "w") as scoreboard:
                scoreboard.write(f"{self.player.name}:{self.player.points}\n")

    @staticmethod
    # retourne le moment où le jeu est censé être fini
    def end_time(delta_minute, delta_second):

        delta = datetime.timedelta(minutes=delta_minute, seconds=delta_second)
        end = datetime.datetime.today() + delta
        return end


if __name__ == "__main__":

    player = Player("Moi")
    g = Game(player, "Esay")
    g.play()
