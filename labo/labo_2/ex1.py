class Person:
    def __init__(self, name, home, properties=None):
        self.name = name
        self.home = home
        self.properties = properties or []

    def __str__(self):
        home_number = self.home.number
        if home_number:
            txt = f"{self.name} ({self.home.building.address}/{home_number})"
        else:
            txt = f"{self.name} ({self.home.building.address})"

        return txt

    def is_owner(self):
        return self.name == self.home.owner.name

    def address(self):
        return self.home.building.address

    def property_details(self):
        for house in self.properties:
            house.show_details()


class Property:
    def __init__(
            self, building, garage=False, owner=None, number=None,
            occupier=None):
        self.garage = garage
        self.building = building
        self.owner = owner
        self.number = number
        self.occupier = occupier or []

    def __str__(self):
        if self.number:
            txt = f"Apartment {self.number}, {self.building.address}"

        else:
            txt = f"House {self.building.address}"

        return txt

    def show_details(self):
        if self.number:
            property_type = "Apartement"

        else:
            property_type = "House"

        occupiers = ""
        for person in self.occupier:
            occupiers += f"\n- {person}"

        if self.garage:
            garage = "YES"

        else:
            garage = "NO"

        nb_apart = self.building.nb_properties()
        if nb_apart > 0:
            apart = f"Nb Apart in Builing: {nb_apart}"

        details = f"""
--- {property_type} {self.building.address} ---
Owner: {self.owner} ({self.owner.address()})
Occupiers: {occupiers}
Garage: {garage}
{apart}
        """

        print(details)

    def sale_to(self, new_owner):
        property_index = self.owner.properties.index(self)
        self.owner.properties.pop(property_index)

        self.owner = new_owner
        self.owner.properties.append(self)


class Building:
    def __init__(self, address, properties=None):
        self.address = address
        self.properties = properties or []

    def __str__(self):
        return f"Building {self.address} ({self.nb_properties()})"

    def nb_properties(self):
        return len(self.properties)

    def add_property(self, property: Property):
        self.properties.append(property)


if __name__ == "__main__":

    # 7
    # a)
    b1 = Building("Commonstreet nb 5")
    b2 = Building("Magicstreet nb 18")

    # b)
    ap1 = Property(b1, True, number=1)
    b1.add_property(ap1)

    # c)
    ap2 = Property(b1, True, number=2)
    ap3 = Property(b1, True, number=3)
    ap4 = Property(b1, True, number=4)
    b1.add_property(ap2)
    b1.add_property(ap3)
    b1.add_property(ap4)

    # d)
    h = Property(b2, True)
    b2.add_property(h)

    # e)
    bob = Person("Bob", h, [h, ap1, ap2])
    alice = Person("Alice", h)
    bobby = Person("Bobby", h)

    # f)
    chris = Person("Chris", ap1)

    # g)
    david = Person("David", ap3, [ap3])

    # h)
    elen = Person("Elen", ap4, [ap4])

    # i)
    h.occupier = [bob, alice, bobby]
    h.owner = bob
    ap1.owner = bob
    ap2.owner = bob
    ap1.occupier = [chris]
    ap3.owner = david
    ap3.occupier = [david]
    ap4.owner = elen
    ap4.occupier = [elen]

    # j)
    print(b1)
    print(b2)
    print(h)
    print(ap2)
    print(bob)
    print(alice)
    print(elen)

    # 8)
    h.show_details()
    ap2.show_details()
    ap3.show_details()

    # 10)
    bob.property_details()

    # 12)
    print("BEFORE")
    for a in bob.properties:
        a.show_details()

    print("AFTER")
    ap2.sale_to(elen)
    for a in bob.properties:
        a.show_details()
