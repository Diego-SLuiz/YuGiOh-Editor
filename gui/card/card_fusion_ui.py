from PySide6 import QtWidgets
from gui.card.base_table_widget import BaseTableWidget

class FusionEditor ( QtWidgets.QWidget ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        # Main widget layout
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout( main_layout )

        # Table that contains all fusions of the selected card
        fusions_table = BaseTableWidget( [ "Material #1", "Material #2", "Result" ] )
        main_layout.addWidget( fusions_table )
        self.fusions_table = fusions_table

        # Buttons group with the available interactions
        buttons_group = QtWidgets.QGroupBox()
        main_layout.addWidget( buttons_group )

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_group.setLayout( buttons_layout )

        # Buttons to interact with the selected card fusions table
        add_fusion = QtWidgets.QPushButton( "Add Fusion" )
        add_fusion.clicked.connect( self.add_card_fusion )
        buttons_layout.addWidget( add_fusion )

        del_fusion = QtWidgets.QPushButton( "Del Fusion" )
        del_fusion.clicked.connect( self.del_card_fusion )
        buttons_layout.addWidget( del_fusion )

        add_many = QtWidgets.QPushButton( "Add Many" )
        add_many.clicked.connect( self.add_many_fusions )
        buttons_layout.addWidget( add_many )

        del_many = QtWidgets.QPushButton( "Del Many" )
        del_many.clicked.connect( self.del_many_fusions )
        buttons_layout.addWidget( del_many )

        clear_card = QtWidgets.QPushButton( "Clear Card" )
        clear_card.clicked.connect( self.clear_card_fusions )
        buttons_layout.addWidget( clear_card )

    def initialize_fusions_table ( self, card ):
        fusions_list = [ [ card.number + 1, a, b ] for a, b in card.fusions_list ]
        self.fusions_table.update_source_data( fusions_list )

    def add_card_fusion ( self ):
        print( "Add One Fusion" )

    def del_card_fusion ( self ):
        print( "Del One Fusion" )

    def add_many_fusions ( self ):
        print( "Add Many Fusions" )

    def del_many_fusions ( self ):
        print( "Del Many Fusions" )

    def clear_card_fusions ( self ):
        print( "Clear Card Fusions" )
