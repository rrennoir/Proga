# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 12:19:55 2020

@author: annes
"""
import random
from gtijv import Player, Country


class Game:
    # Une partie est un affrontement entre 2 joueurs.
    # Le premier que trouve le nombre entre 1 et 10 a gagné.

    def __init__(self, p1, p2):
        self.players = (p1, p2)
        self.player_turn = 0  # 0 ou 1. Commence à 0
        self.nb_to_find = random.randint(1, 10)

    def next_turn(self):
        self.player_turn = (self.player_turn + 1) % 2

    # Fait jouer un tour de jeu
    # Retourne le gagnant s'il y en a un (sinon, None par défaut)
    def play_turn(self):
        print("Tour du joueur :", self.players[self.player_turn].pseudo)
        nb = Player.play()

        if nb == self.nb_to_find:
            return self.players[self.player_turn]

    # Fait jouer une partie complète
    # Retourne le gagnant
    def play(self):
        print(">>>", self.players[0].pseudo, "VS", self.players[1].pseudo, "<<<")
        winner = None

        while not winner:
        # None équivaut à False quand on le teste comme un booléen --> il est Falsy
        # Un objet équivaut à True quand on le teste comme un booléen --> il est Truthy

        # La boucle va continuer tant que winner contient None.
        # Dès qu'on mettra un objet dans winner, elle s'arretera
            winner = self.play_turn()
            self.next_turn()

        print("Le gagnant est : ", winner)
        return winner


class Tournament:

    def __init__(self):
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    # précondition : il y a au moins 2 joueurs dans self.players
    def play_random_game(self):
        players_copy = self.players.copy()
        player_1 = random.choice(players_copy)
        players_copy.pop(players_copy.index(player_1))
        player_2 = random.choice(players_copy)

        a_game = Game(player_1, player_2)

        winner = a_game.play()

        looser = player_2 if player_1 == winner else player_1
        self.players.remove(looser)

    def play(self):
        if len(self.players) > 0:
            print("QUE LE TOURNOIS COMMENCE !")
            while len(self.players) > 1:
                self.play_random_game()

            print("GRAND GAGNANT DU TOURNOIS :", self.players[0])
        else:
            print("Aucuns inscrits, tournois annulé")


if __name__ == "__main__":

    usa = Country("USA", "Washington")
    bel = Country("Belgique", "Bruxelles")
    p1 = Player("Michel", "MiMi10", bel)
    p2 = Player("Jean", "SuperJ", bel)
    p3 = Player("Bobby", "BB8", usa)
    p4 = Player("James", "007", usa)
    usa.add_player(p3)
    usa.add_player(p4)
    bel.add_player(p1)
    bel.add_player(p2)

    t = Tournament()

    t.add_player(p1)
    t.add_player(p2)
    t.add_player(p3)
    t.add_player(p4)

    t.play()
