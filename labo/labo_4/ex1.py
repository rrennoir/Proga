import datetime
import random


class Fight:
    def __init__(self, team1, team2):
        self._participants = (team1, team2)
        self._date = datetime.date.today
        self._winner = None

        team1.nb_fights += 1
        team2.nb_fights += 1

    @property
    def participants(self):
        return self._participants

    @property
    def date(self):
        return self._date

    @property
    def winner(self):
        return self._winner

    def start(self):
        for team in self.participants:
            if len(team.active_characters) == 0:
                print(f"L'équipe {team.name} n'a aucun personnage actif")
                return None

        for team in self.participants:
            team.show_details()

        print("--- C'est parti ! ---")
        turn = 0
        current_team = random.choice((0, 1))

        while len(self.participants[current_team].active_characters) > 0:
            indice = (turn // 2) % len(self.participants[current_team].active_characters)
            current_player = self.participants[current_team]\
                .active_characters[indice]
            current_player.play_turn(self.participants[(current_team + 1) % 2].active_characters) 

            turn += 1
            current_team = (current_team + 1) % 2

        if len(self.participants[0].active_characters) == 0:
            self._winner = self.participants[1]

        else:
            self._winner = self.participants[0]

        print(f"victoire de l'équipe {self._winner.name}")
        self._winner.nb_victories += 1
        return self._winner


class Team:
    def __init__(self, name):
        self.name = name
        self.nb_fights = 0
        self.nb_victories = 0
        self.active_characters = []
        self.reserve_characters = []

    @property
    def nb_loses(self):
        return self.nb_fights - self.nb_victories

    def add_active_character(self, player):
        if len(self.active_characters) < 5:
            self.active_characters.append(player)

        else:
            self.add_reserve_character(player)

    def add_reserve_character(self, player):
        self.reserve_characters.append(player)

    def show_details(self):
        description_active = ""
        for active_player in self.active_characters:
            description_active += f"\n- {active_player}"

        description_inactive = ""
        for inactive_player in self.reserve_characters:
            description_inactive += f"\n- {inactive_player}"
        print(
            f"""
            ***Equipe {self.name} ({self.nb_victories} / {self.nb_fights})***
            Joueurs actifs:
            {description_active}
            Joueurs inactifs:
            {description_inactive}
            """)


class Character:
    def __init__(self, name, team, strength, life, armor):
        self._name = name
        self._team = team
        self._strength = strength
        self._life = life
        self._armor = armor

        team.add_reserve_character(self)

    @property
    def name(self):
        return self._name

    @property
    def team(self):
        return self._team

    @property
    def strength(self):
        return self._strength

    @property
    def life(self):
        return self._life

    @property
    def armor(self):
        return self._armor

    @property
    def is_active(self):
        return self in self.team.active_characters

    def __str__(self):
        return f"{self.name} ({self.life}-{self.strength}-{self.armor})"

    def get_heal(self, health):
        self._life += health

    def get_hit(self, damage):
        damage_left = damage - self.armor
        if damage_left >= 0:
            self._armor = 0
            self._life += damage_left

            if self._life <= 0:
                self.change_status()

        else:
            self._armor -= damage

    def hit(self, character):
        character.get_hit(self.strength)

    def change_status(self):
        if self.is_active:
            self.team.active_characters.remove(self)
            self.team.add_reserve_character(self)

        else:
            self.team.reserve_characters.remove(self)
            self.team.add_active_character(self)

    def play_turn(self, oponents):
        victim = random.choice(oponents)
        print(f"{self.name} attaque {victim.name}")
        self.hit(victim)


class Wizard(Character):
    def __init__(self, name, team, strength, life, armor, mana=5):
        super().__init__(name, team, strength, life, armor)
        self._mana = mana

    def regeneration(self):
        self._mana += 2

    def heal(self, character):
        if self._mana > 0:
            character.get_heal(character, self._mana // 2)
            self._mana - 1

    def magic_hit(self, character):
        if self._mana > 0:
            character.get_hit(self._mana)
            self._mana //= 2

    def __str__(self):
        return f"Wizard {super().__str__()} [{self._mana}]"


class Warrior(Character):
    def __init__(self, name, team, strength, life, armor):
        super().__init__(name, team, strength, life, armor)
        self._rage = 0

    def fury_hit(self, character):
        character.get_hit(self.strength * (self._rage // 2))
        self._rage = 0

    def get_hit(self, damage):
        damage_left = damage - self.armor
        if damage_left >= 0:
            self._armor = 0
            self._life += damage_left

            if damage_left > 0:
                self._rage += 1

            if self.life <= 0:
                self.change_status()

        else:
            self._armor -= damage

    def __str__(self):
        return f"Warrior {super().__str__()} [{self._rage}]"


class Animal(Character):
    def __init__(self, name, team, strength, life):
        super().__init__(name, team, strength, life, 0)
        self._owner = None

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        self._owner = owner

    def __str__(self):
        if self._owner:
            text = f"Animal {super().__str__()} owned by {self.owner.name}"
        else:
            text = f"Animal {super().__str__()}"

        return text


class Hunter(Character):
    def __init__(self, name, team, strength, life, armor):
        super().__init__(name, team, strength, life, armor)
        self._pet = None

    @property
    def pet(self):
        return self._pet

    @pet.setter
    def pet(self, pet):
        if self.team == pet.team:
            self._pet = pet
            pet.owner = self

    def hit(self, character):
        if self.pet:
            character.get_hit(self.strength + self._pet.strength)

        else:
            character.get_hit(self.strength)

    def __str__(self):
        if self.pet:
            text = f"Hunter {super().__str__()} with {self._pet.name}"

        else:
            text = f"Hunter {super().__str__()}"

        return text


if __name__ == "__main__":
    prof = Team("Les Prof")
    war1 = Warrior("Andhrien", prof, 3, 12, 3)
    ani1 = Animal("Pixel", prof, 6, 10)
    hun1 = Hunter("Valendi", prof, 2, 10, 3)
    ani2 = Animal("Pong", prof, 4, 8)
    hun1.pet = ani2
    wiz1 = Wizard("Hans", prof, 4, 10, 2)
    ani3 = Animal("Tesla", prof, 4, 6)

    war1.change_status()
    ani1.change_status()
    hun1.change_status()
    ani2.change_status()
    wiz1.change_status()
    ani3.change_status()

    prof.show_details()

    stu = Team("Les Etudiants")
    c1 = Warrior("Toto", stu, 12, 3, 3)
    c2 = Animal("Toutou", stu, 10, 8)
    c3 = Warrior("Bob", stu, 10, 2, 3)
    c4 = Animal("Chouchou", stu, 8, 4)
    c5 = Wizard("Nostradamus", stu, 10, 3, 2)
    c1.change_status()
    c2.change_status()
    c3.change_status()
    c4.change_status()
    c5.change_status()

    stu.show_details()

    fight = Fight(stu, prof)
    fight.start()
