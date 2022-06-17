from PySide6 import QtWidgets
from gui.card.base_table_widget import BaseTableWidget
from gui.utilities.card_search_dialog import CardSearchDialog

class EquipEditor ( QtWidgets.QWidget ):

    search_header = [
        "Monster",
    ]

    search_filter = [
        [ None, [ "spell", "equip", "trap", "ritual" ] ],
    ]

    target_header = "Equip"
    target_filter = [ [ "equip" ], None ]

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()
        self.card_search = CardSearchDialog( self.search_header, self.search_filter, self.target_header, self.target_filter )

    def create_widgets ( self ):
        # Main widget layout
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout( main_layout )

        # Table that contains all cards compatible with the selected equip
        equips_table = BaseTableWidget( [ "Equip", "Monster" ] )
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

    def initialize_equips_table ( self, card ):
        equips_list = [ [ card.number + 1, x ] for x in card.equips_list ]
        self.equips_table.update_source_data( equips_list )

    def add_card_equip ( self ):
        print( "Add Equip Card" )

    def del_card_equip ( self ):
        print( "Del Equip Card" )

    def add_many_cards ( self ):
        self.card_search.exec()
        print( "Add Many Equips" )

    def del_many_cards ( self ):
        self.card_search.exec()
        print( "Del Many Equips" )

    def clear_card_equips ( self ):
        print( "Clear Card Equips" )
