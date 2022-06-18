from PySide6 import QtWidgets
from gui.card.table_widget import TableWidget
from gui.card.card_search_dialog import CardSearchDialog
from gui.card.card_selector_dialog import CardSelectorDialog

class EditEquipWidget ( QtWidgets.QWidget ):

    # Default properties for searching many equips
    search_header = [
        "Monster",
    ]

    search_filter = [
        [ None, [ "spell", "equip", "trap", "ritual" ] ],
    ]

    target_header = "Equip"
    target_filter = [ [ "equip" ], None ]

    # Default properties to add one specific equip
    select_header = [
        "Monster",
        "Equip",
    ]

    select_filter = [
        [ None, [ "spell", "equip", "trap", "ritual" ] ],
        [ [ "equip" ], None ],
    ]

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()
        self.card_search = CardSearchDialog( self.search_header, self.search_filter, self.target_header, self.target_filter, self )
        self.card_select = CardSelectorDialog( self.select_header, self.select_filter, self )
        self.working_card = None

    def create_widgets ( self ):
        # Main widget layout
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout( main_layout )

        # Table that contains all cards compatible with the selected equip
        equips_table = TableWidget( [ "Equip", "Monster" ] )
        main_layout.addWidget( equips_table )
        self.equips_table = equips_table

        # Buttons group with the available interactions
        buttons_group = QtWidgets.QGroupBox()
        main_layout.addWidget( buttons_group )

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_group.setLayout( buttons_layout )

        # Buttons to interact with the selected card equips table
        add_equip = QtWidgets.QPushButton( "Add Equip" )
        add_equip.clicked.connect( self.add_card_equip )
        buttons_layout.addWidget( add_equip )

        del_equip = QtWidgets.QPushButton( "Del Equip" )
        del_equip.clicked.connect( self.del_card_equip )
        buttons_layout.addWidget( del_equip )

        add_many = QtWidgets.QPushButton( "Add Many" )
        add_many.clicked.connect( self.add_many_cards )
        buttons_layout.addWidget( add_many )

        del_many = QtWidgets.QPushButton( "Del Many" )
        del_many.clicked.connect( self.del_many_cards )
        buttons_layout.addWidget( del_many )

        clear_card = QtWidgets.QPushButton( "Clear Card" )
        clear_card.clicked.connect( self.clear_card_equips )
        buttons_layout.addWidget( clear_card )

    def change_working_card ( self, card ):
        # Update the current working card
        self.working_card = card
        self.initialize_equips_table()

    def initialize_equips_table ( self ):
        # Initialize the table containing the card equips
        card = self.working_card
        equips_list = [ [ card.number + 1, x ] for x in card.equips_list ]
        self.equips_table.update_source_data( equips_list )

    def add_card_equip ( self ):
        self.card_select.exec()
        print( "Add Equip Card" )

    def del_card_equip ( self ):
        self.card_select.exec()
        print( "Del Equip Card" )

    def add_many_cards ( self ):
        self.card_search.exec()
        print( "Add Many Equips" )

    def del_many_cards ( self ):
        self.card_search.exec()
        print( "Del Many Equips" )

    def clear_card_equips ( self ):
        print( "Clear Card Equips" )
