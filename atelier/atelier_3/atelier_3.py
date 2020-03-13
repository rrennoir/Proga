import random
import datetime


class Human:

    def __init__(self, name, bd=None):
        self._name = name

        if bd:
            self._birthday = bd

        else:
            self._birthday = datetime.date.today()

        self._gender = random.choice("MF")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def birthday(self):
        return self._birthday

    @property
    def gender(self):
        return _gender

    @gender.setter
    def gender(self, new_gender):
        self._gender = new_gender

    @property
    def age(self):
        today = datetime.date.today()
        age = today.year - self._birthday.year
        if ((today.month < self._birthday.month)
                or (today.month <= self._birthday.month
                    and today.day < self._birthday.day)):
            age -= 1

        return age

    def say(self, message):
        print(self.name, ":", message)


if __name__ == "__main__":
    bd = datetime.date(1999, 8, 11)
    bob = Human("Bob", bd)
    bob.say("I am " + str(bob.age) + " years old")
    bob._birthday = datetime.date(2001, 9, 11)
    bob.say("I am " + str(bob.age) + " years old")
