from PySide6 import QtWidgets
from gui.card.base_table_widget import BaseTableWidget

class RitualEditor ( QtWidgets.QWidget ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        # Main widget layout
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout( main_layout )

        # Table that contains all rituals recipes of the selected card
        rituals_table = BaseTableWidget( [ "Ritual", "Tribute #1", "Tribute #2", "Tribute #3", "Result" ] )
        main_layout.addWidget( rituals_table )
        self.rituals_table = rituals_table

        # Buttons group with the available interactions
        buttons_group = QtWidgets.QGroupBox()
        main_layout.addWidget( buttons_group )

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_group.setLayout( buttons_layout )

        # Buttons to interact with the selected card rituals recipes
        add_ritual = QtWidgets.QPushButton( "Add Ritual" )
        add_ritual.clicked.connect( self.add_card_ritual )
        buttons_layout.addWidget( add_ritual )

        del_ritual = QtWidgets.QPushButton( "Del Ritual" )
        del_ritual.clicked.connect( self.del_card_ritual )
        buttons_layout.addWidget( del_ritual )

        clear_card = QtWidgets.QPushButton( "Clear Card" )
        clear_card.clicked.connect( self.clear_card_rituals )
        buttons_layout.addWidget( clear_card )

    def initialize_rituals_table ( self, card ):
        rituals_tributes = [ card.rituals_tributes ]
        self.rituals_table.update_source_data( rituals_tributes )

    def add_card_ritual ( self ):
        print( "Add Card Ritual" )

    def del_card_ritual ( self ):
        print( "Del Card Ritual" )

    def clear_card_rituals ( self ):
        print( "Clear Card Rituals")
