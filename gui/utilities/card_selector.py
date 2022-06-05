from PySide6 import QtWidgets, QtCore
from scripts.card.card_editor import LIBRARY, Card
from gui.utilities.library_model import LibraryModel

class CardSelector ( QtWidgets.QWidget ):

    card_selected = QtCore.Signal( Card )

    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        # Main layout
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins( 0, 8, 0, 1 )
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
        select_card.currentIndexChanged.connect( self.get_target )
        select_card.setIconSize( QtCore.QSize( 40, 32 ) )
        select_card.setEditable( True )
        select_card.setCompleter( card_completer )
        select_card.setModel( LibraryModel() )
        select_card.setCurrentIndex( 0 )
        layout.addWidget( select_card )

    def get_target ( self, index ):
        card = LIBRARY[index]
        self.card_selected.emit( card )
