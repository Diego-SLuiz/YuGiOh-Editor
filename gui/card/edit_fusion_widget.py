from PySide6 import QtWidgets
from gui.card.table_widget import TableWidget
from gui.card.card_search_dialog import CardSearchDialog
from gui.card.card_selector_dialog import CardSelectorDialog

class EditFusionWidget ( QtWidgets.QWidget ):

    # Default properties for searching many fusions
    search_header = [
        "Material #1",
        "Material #2",
    ]

    search_filter = [
        [ None, None ],
        [ None, None ],
    ]

    target_header = "Result"
    target_filter = [ None, None ]

    # Default properties to add one specific fusion
    select_header = [
        "Material #1",
        "Material #2",
        "Result",
    ]

    select_filter = [
        [ None, None ],
        [ None, None ],
        [ None, None ],
    ]

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()
        self.card_search = CardSearchDialog( self.search_header, self.search_filter, self.target_header, self.target_filter, self )
        self.card_select = CardSelectorDialog( self.select_header, self.select_filter, self )

    def create_widgets ( self ):
        # Main widget layout
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout( main_layout )

        # Table that contains all fusions of the selected card
        fusions_table = TableWidget( [ "Material #1", "Material #2", "Result" ] )
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
        self.card_select.exec()
        print( "Add One Fusion" )

    def del_card_fusion ( self ):
        self.card_select.exec()
        print( "Del One Fusion" )

    def add_many_fusions ( self ):
        self.card_search.exec()
        print( "Add Many Fusions" )

    def del_many_fusions ( self ):
        self.card_search.exec()
        print( "Del Many Fusions" )

    def clear_card_fusions ( self ):
        print( "Clear Card Fusions" )
