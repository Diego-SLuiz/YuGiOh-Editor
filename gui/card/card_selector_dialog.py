from PySide6 import QtWidgets
from gui.card.card_dropdown_widget import CardDropdownWidget
from gui.utilities.card_preview_widget import CardPreviewWidget

class SelectCard ( QtWidgets.QGroupBox ):

    def __init__ ( self, search_filter, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.search_filter = search_filter
        self.create_widgets()

    def create_widgets ( self ):
        # Main widget layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout( layout )

        # Card dropdown widget
        select_card = CardDropdownWidget()
        select_card.change_filter_type( self.search_filter )
        layout.addWidget( select_card )

        # Card preview widget
        card_preview = CardPreviewWidget()
        select_card.card_selected.connect( card_preview.create_preview_image )
        layout.addWidget( card_preview )

class CardSelectorDialog ( QtWidgets.QDialog ):

    def __init__ ( self, group_header=[ "Default" ], group_filter=[ [ None, None ] ], *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.group_header = group_header
        self.group_filter = group_filter
        self.create_widgets()

    def create_widgets ( self ):
        # Main widget layout
        layout = QtWidgets.QGridLayout()
        self.setLayout( layout )

        # Create dropdown fields to select a card
        for index, header, search in zip( range( len( self.group_header ) ), self.group_header, self.group_filter ):
            select_card = SelectCard( search, header )
            layout.addWidget( select_card, 0, index )

        # Buttons actions group
        buttons_group = QtWidgets.QGroupBox()
        layout.addWidget( buttons_group )

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_group.setLayout( buttons_layout )

        confirm_button = QtWidgets.QPushButton( "Confirm" )
        confirm_button.clicked.connect( self.accept )
        buttons_layout.addWidget( confirm_button )

        cancel_button = QtWidgets.QPushButton( "Cancel" )
        cancel_button.clicked.connect( self.reject )
        buttons_layout.addWidget( cancel_button )
