from PySide6 import QtWidgets
from scripts.card.card_editor import Card
from scripts.card.references import *

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
        input_id = QtWidgets.QSpinBox( minimum=0, maximum=722 )
        layout.addRow( "Number", input_id )

        select_type = QtWidgets.QComboBox()
        select_type.addItems( card_types )
        layout.addRow( "Type", select_type )

        select_attribute = QtWidgets.QComboBox()
        select_attribute.addItems( card_attributes )
        layout.addRow( "Attribute", select_attribute )

        select_guardian = QtWidgets.QComboBox()
        select_guardian.addItems( card_guardians )
        layout.addRow( "Guardian", select_guardian )

        select_group = QtWidgets.QComboBox()
        select_group.addItems( ["Unique Fusion", "Ritual Monster"] )
        layout.addRow( "Group", select_group )

        level_range = QtWidgets.QHBoxLayout()
        minimum_level = QtWidgets.QSpinBox( minimum=0, maximum=12 )
        level_range.addWidget( minimum_level )
        maximum_level = QtWidgets.QSpinBox( minimum=0, maximum=12 )
        level_range.addWidget( maximum_level )
        layout.addRow( "Level Range", level_range )

        attack_range = QtWidgets.QHBoxLayout()
        minimum_attack = QtWidgets.QSpinBox( minimum=0, maximum=5000 )
        attack_range.addWidget( minimum_attack )
        maximum_attack = QtWidgets.QSpinBox( minimum=0, maximum=5000 )
        attack_range.addWidget( maximum_attack )
        layout.addRow( "Attack Range", attack_range )

        defense_range = QtWidgets.QHBoxLayout()
        minimum_defense = QtWidgets.QSpinBox( minimum=0, maximum=5000 )
        defense_range.addWidget( minimum_defense )
        maximum_defense = QtWidgets.QSpinBox( minimum=0, maximum=5000 )
        defense_range.addWidget( maximum_defense )
        layout.addRow( "Defense Range", defense_range )
