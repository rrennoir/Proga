class Player:

    nb_players = 0

    def __init__(self, name, pseudo, county):
        self.name = name
        self.pseudo = pseudo
        self.country = county

        Player.nb_players += 1

    def __str__(self):
        return f"Name: {self.pseudo}\nPseudo: {self.pseudo}\nCountry: {self.country.name}"

    @staticmethod
    def Play():
        nb = int(input("Enter a number. "))

        while not 1 <= nb <= 10:
            nb = int(input("Enter a number. "))


class Country:

    def __init__(self, name, capital_city, citizen=None):
        self.name = name
        self.capital_city = capital_city
        self.citizen = citizen or []

    def show_details(self):
        print(f"{self.name} (capital city: {self.capital_city})")

        for player in self.citizen:
            print(f" - {player.pseudo}")

    def add_player(self, player):
        if player.country != self:
            index = player.country.citizen.index(player)
            del player.country.citizen[index]
            player.country = self

        self.citizen.append(player)


if __name__ == "__main__":
    usa = Country("United_State", "Washington")
    bel = Country("Belgium", "Bruxelles")

    billy = Player("Billy", "Billy6240", bel)
    bob = Player("Bob", "WaffleSlayer", bel)
    bel.citizen.append(billy)
    bel.citizen.append(bob)

    kevin = Player("Kevin", "Trump2020", usa)
    bryan = Player("Bryan", "noobmaster69", usa)
    usa.citizen.append(kevin)
    usa.citizen.append(bryan)

    usa.show_details()
    bel.show_details()

    obama = Player("Obama", "ChuckNoris42", usa)
    usa.add_player(obama)

    bel.add_player(obama)
    bel.show_details()
    usa.show_details()

    print(Player.nb_players)

    billy.Play()
