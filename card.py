class Card:
    def __init__(self, name, cardtype, type, attribute = None, attack = None, defense = None, level = None):
        self.name = name
        self.cardtype = cardtype
        self.type = type
        self.attribute = attribute
        self.attack = attack
        self.defense = defense
        self.level = level

        if "Tuner" in self.cardtype:
            self.tuner = True
        else:
            self.tuner = False

    def __str__(self) -> str:
        return self.name
        
    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other):
        # We want to check if cards exist in hands by using their names
        return self.name == other

    def __hash__(self) -> int:
        return hash(self.name)