from PySide6 import QtWidgets
from scripts.card.references import *
from scripts.card.card_editor import Card
from gui.utilities.card_selector import CardSelector

class CardSearch ( QtWidgets.QGroupBox ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets( self ):
        # Card default properties
        card_types = ["None"] + [x.capitalize() for x in TYPES]
        card_attributes = ["None"] + [x.capitalize() for x in ATTRIBUTES]
        card_guardians = ["None"] + [x.capitalize() for x in GUARDIANS]

        # Main widget layout
        layout = QtWidgets.QFormLayout()
        self.setLayout( layout )

        # Card filter properties
        select_card = CardSelector()
        select_card.card_selected.connect( self.set_card )
        layout.addRow( "Number", select_card )

        select_group = QtWidgets.QComboBox()
        select_group.addItems( ["None", "Unique Fusion", "Ritual Monster"] )
        select_group.currentIndexChanged.connect( self.set_group )
        layout.addRow( "Group", select_group )

        select_type = QtWidgets.QComboBox()
        select_type.addItems( card_types )
        select_type.currentIndexChanged.connect( self.set_type )
        layout.addRow( "Type", select_type )

        select_attribute = QtWidgets.QComboBox()
        select_attribute.addItems( card_attributes )
        select_attribute.currentIndexChanged.connect( self.set_attribute )
        layout.addRow( "Attribute", select_attribute )

        select_guardian = QtWidgets.QComboBox()
        select_guardian.addItems( card_guardians )
        select_guardian.currentIndexChanged.connect( self.set_guardian )
        layout.addRow( "Guardian", select_guardian )

        level_range = QtWidgets.QHBoxLayout()
        minimum_level = QtWidgets.QSpinBox( minimum=0, maximum=12 )
        minimum_level.valueChanged.connect( self.set_level )
        level_range.addWidget( minimum_level )
        maximum_level = QtWidgets.QSpinBox( minimum=0, maximum=12 )
        maximum_level.valueChanged.connect( self.set_level )
        level_range.addWidget( maximum_level )
        layout.addRow( "Level Range", level_range )

        attack_range = QtWidgets.QHBoxLayout()
        minimum_attack = QtWidgets.QSpinBox( minimum=0, maximum=5000 )
        minimum_attack.valueChanged.connect( self.set_attack )
        attack_range.addWidget( minimum_attack )
        maximum_attack = QtWidgets.QSpinBox( minimum=0, maximum=5000 )
        maximum_attack.valueChanged.connect( self.set_attack )
        attack_range.addWidget( maximum_attack )
        layout.addRow( "Attack Range", attack_range )

        defense_range = QtWidgets.QHBoxLayout()
        minimum_defense = QtWidgets.QSpinBox( minimum=0, maximum=5000 )
        minimum_defense.valueChanged.connect( self.set_defense )
        defense_range.addWidget( minimum_defense )
        maximum_defense = QtWidgets.QSpinBox( minimum=0, maximum=5000 )
        maximum_defense.valueChanged.connect( self.set_defense )
        defense_range.addWidget( maximum_defense )
        layout.addRow( "Defense Range", defense_range )

    def set_card ( self, card ):
        print( f"Set {card.name}" )

    def set_group ( self ):
        print( "Set Group" )

    def set_type ( self ):
        print( "Set Type" )

    def set_attribute ( self ):
        print( "Set Attribute" )

    def set_guardian ( self ):
        print( "Set Guardian" )

    def set_level ( self ):
        print( "Set Level Range" )

    def set_attack ( self ):
        print( "Set Attack Range" )

    def set_defense ( self ):
        print( "Set Defense Range" )

    def search_result ( self ):
        print( "Search Result" )
