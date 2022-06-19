from enum import Enum

class TypesFilter ( Enum ):
    DEFAULT = None, None
    MONSTER_ONLY = None, [ "spell", "equip", "trap", "ritual" ]
    MAGIC_ONLY = [ "spell", "equip", "trap", "ritual" ], None
    DRAGON = [ "dragon" ], None
    SPELLCASTER = [ "spellcaster" ], None
    ZOMBIE = [ "zombie" ], None
    WARRIOR = [ "warrior" ], None
    BESATWARRIOR = [ "beastwarrior" ], None
    BEAST = [ "beast" ], None
    WINDGEDBEAST = [ "wingedbeast" ], None
    FIEND = [ "fiend" ], None
    FAIRY = [ "fairy" ], None
    INSECT = [ "insect" ], None
    DINOSAUR = [ "dinosaur" ], None
    REPTILE = [ "reptile" ], None
    FISH = [ "fish" ], None
    SEASERPENT = [ "seaserpent" ], None
    MACHINE = [ "machine" ], None
    THUNDER = [ "thunder" ], None
    AQUA = [ "aqua" ], None
    PYRO = [ "pyro" ], None
    ROCK = [ "rock" ], None
    PLANT = [ "plant" ], None
    SPELL = [ "spell" ], None
    TRAP = [ "trap" ], None
    RITUAL = [ "ritual" ], None
    EQUIP = [ "equip" ], None
