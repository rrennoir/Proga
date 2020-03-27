class Animal:
    def __init__(self, name, bd, ship_nb, size):
        self.name = name
        self.birthday = bd
        self.ship_nb = ship_nb
        self.size = size

    def sleep(self):
        print(self.name, ": ZzzzzzzzzZzz...")

    def eat(self):
        print(self.name, ": *Crounch*")


class Rabbit(Animal):
    def __init__(self, name, bd, ship_nb, size, ear_size):
        super().__init__(name, bd, ship_nb, size)
        self.ear_size = ear_size

    def jump(self):
        print(self.name, ": *Bwing*")


class Dog(Animal):
    def bark(self):
        print(self.name, ": WOOOUF !")


class Cat(Animal):
    def meow(self):
        print(self.name, ": Meow !")

    def purr(self):
        print(self.name, ": purr !")

    def eat(self):
        self.purr()
        print(self.name, ": *Crounch*")


if __name__ == "__main__":
    c = Cat("Tesla", "1/04/2017", 12568743, 35)
    d = Dog("Pixel", "16/10/2019", 58963217, 70)
    r = Rabbit("Pong", "11/02/2010", 25874136, 20, 15)
    c.eat()
    d.eat()
    r.eat()
    c.sleep()
    d.sleep()
    r.sleep()

    d.bark()
    c.meow()
    r.jump()
