from PySide6 import QtWidgets, QtCore
from scripts.card.card_editor import LIBRARY
from gui.utilities.library_model import LibraryModel
from gui.utilities.card_preview import CardPreview

class CardSelector ( QtWidgets.QWidget ):

    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        # Main layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout( layout )

        # Card completer
        card_completer = QtWidgets.QCompleter()
        card_completer.setModel( LibraryModel() )
        card_completer.setCompletionColumn( 0 )
        card_completer.setCompletionRole( QtCore.Qt.ItemDataRole.DisplayRole )
        card_completer.setCaseSensitivity( QtCore.Qt.CaseInsensitive )
        card_completer.setFilterMode( QtCore.Qt.MatchFlag.MatchContains )

        # Dropdown with cards
        select_card = QtWidgets.QComboBox()
        select_card.setIconSize( QtCore.QSize( 40, 32 ) )
        select_card.setEditable( True )
        select_card.setCompleter( card_completer )
        select_card.setModel( LibraryModel() )
        layout.addWidget( select_card )

        # Card preview widget
        card_preview = CardPreview()
        select_card.currentIndexChanged.connect( self.update_preview )
        layout.addWidget( card_preview )
        self.card_preview = card_preview

    def update_preview ( self, index ):
        card = LIBRARY[index]
        self.card_preview.create_preview_image( card )
