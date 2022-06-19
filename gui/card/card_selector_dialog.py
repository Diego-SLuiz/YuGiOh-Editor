from PySide6 import QtWidgets, QtCore
from gui.card.card_dropdown_widget import CardDropdownWidget
from gui.card.card_enums import TypesFilter
from gui.utilities.card_preview_widget import CardPreviewWidget

class SelectCard ( QtWidgets.QGroupBox ):

    def __init__ ( self, types_filter, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.types_filter = types_filter
        self.create_widgets()

    def create_widgets ( self ):
        # Main widget layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout( layout )

        # Card dropdown widget
        select_card = CardDropdownWidget()
        select_card.change_types_filter( self.types_filter )
        layout.addWidget( select_card, alignment=QtCore.Qt.AlignmentFlag.AlignTop )

        # Card preview widget
        card_preview = CardPreviewWidget()
        card_preview.setSizePolicy( QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding )
        card_preview.setAlignment( QtCore.Qt.AlignmentFlag.AlignCenter )
        select_card.card_selected.connect( card_preview.create_preview_image )
        layout.addWidget( card_preview )

class CardSelectorDialog ( QtWidgets.QDialog ):

    def __init__ (
        self,
        selector_headers=[ "Default" ],
        selector_filters=[ TypesFilter.DEFAULT ],
        *args,
        **kwargs
    ):
        super().__init__( *args, **kwargs )
        self.selector_headers = selector_headers
        self.selector_filters = selector_filters
        self.create_widgets()

    def create_widgets ( self ):
        # Main widget layout
        layout = QtWidgets.QGridLayout()
        self.setLayout( layout )

        # Create dropdown fields to select a card
        for index in range( len( self.selector_headers ) ):
            select_card = SelectCard( self.selector_filters[ index ], self.selector_headers[ index ] )
            layout.addWidget( select_card, 0, index )

        # Buttons actions group
        buttons_group = QtWidgets.QGroupBox()
        buttons_group.setSizePolicy( QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum )
        layout.addWidget( buttons_group, 1, 0, 1, index + 1 )

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_group.setLayout( buttons_layout )

        confirm_button = QtWidgets.QPushButton( "Confirm" )
        confirm_button.clicked.connect( self.accept )
        buttons_layout.addWidget( confirm_button )

        cancel_button = QtWidgets.QPushButton( "Cancel" )
        cancel_button.clicked.connect( self.reject )
        buttons_layout.addWidget( cancel_button )
