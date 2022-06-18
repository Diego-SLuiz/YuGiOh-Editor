from PySide6 import QtWidgets, QtCore
from scripts.card.references import TYPES, ATTRIBUTES, GUARDIANS
from gui.card.card_dropdown_widget import CardDropdownWidget
from gui.utilities.card_preview_widget import CardPreviewWidget

class SearchGroup ( QtWidgets.QGroupBox ):

    # Card standard properties
    card_types = [ "None" ] + [ x.capitalize() for x in TYPES ]
    card_attributes = [ "None" ] + [ x.capitalize() for x in ATTRIBUTES ]
    card_guardians = [ "None" ] + [ x.capitalize() for x in GUARDIANS ]

    def __init__ ( self, search_filter, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.search_filter = search_filter
        self.create_widgets()

    def create_widgets ( self ):
        # Main widget layout
        layout = QtWidgets.QFormLayout()
        self.setLayout( layout )

        # Card search search options
        select_card = CardDropdownWidget()
        select_card.change_filter_type( self.search_filter )
        layout.addRow( "Number", select_card )
        self.select_card = select_card

        select_group = QtWidgets.QComboBox()
        select_group.addItems( [ "None", "Unique Fusion", "Ritual Monster", "Female" ] )
        select_group.currentIndexChanged.connect( self.set_group )
        layout.addRow( "Group", select_group )

        select_type = QtWidgets.QComboBox()
        select_type.addItems( self.card_types )
        select_type.currentIndexChanged.connect( self.set_type )
        layout.addRow( "Type", select_type )

        select_attribute = QtWidgets.QComboBox()
        select_attribute.addItems( self.card_attributes )
        select_attribute.currentIndexChanged.connect( self.set_attribute )
        layout.addRow( "Attribute", select_attribute )

        select_guardian = QtWidgets.QComboBox()
        select_guardian.addItems( self.card_guardians )
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

class CardSearchDialog ( QtWidgets.QDialog ):

    def __init__ ( self, search_header, search_filter, target_header, target_filter, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.search_header = search_header
        self.search_filter = search_filter
        self.target_header = target_header
        self.target_filter = target_filter
        self.create_widgets()

    def create_widgets ( self ):
        # Main dialog layout
        layout = QtWidgets.QGridLayout()
        self.setLayout( layout )

        # Search card fields
        for index, search, header in zip( range( len( self.search_filter ) ), self.search_filter, self.search_header or [ "Default" ] ):
            search_group = SearchGroup( search, header )
            layout.addWidget( search_group, 0, index )

        # Card target group
        target_group = QtWidgets.QGroupBox( self.target_header )
        layout.addWidget( target_group, 0, index + 1 )

        target_layout = QtWidgets.QVBoxLayout()
        target_group.setLayout( target_layout )

        select_card = CardDropdownWidget()
        select_card.change_filter_type( self.target_filter )
        target_layout.addWidget( select_card, alignment=QtCore.Qt.AlignmentFlag.AlignTop )

        card_preview = CardPreviewWidget()
        select_card.card_selected.connect( card_preview.create_preview_image )
        target_layout.addWidget( card_preview )

        # Buttons actions group
        buttons_group = QtWidgets.QGroupBox()
        buttons_group.setSizePolicy( QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum )
        layout.addWidget( buttons_group, 1, 0, 1, index + 2 )

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_group.setLayout( buttons_layout )

        confirm_button = QtWidgets.QPushButton( "Confirm" )
        confirm_button.clicked.connect( self.accept )
        buttons_layout.addWidget( confirm_button )

        cancel_button = QtWidgets.QPushButton( "Cancel" )
        cancel_button.clicked.connect( self.reject )
        buttons_layout.addWidget( cancel_button )
