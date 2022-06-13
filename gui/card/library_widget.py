from PySide6 import QtWidgets, QtCore
from scripts.card.card_editor import Card, LIBRARY
from gui.card.library_model import LibraryModel
from gui.card.library_filter import LibraryFilter

class LibraryWidget ( QtWidgets.QWidget ):

    card_changed = QtCore.Signal( Card )

    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        # Main widget layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins( 0, 0, 0, 0 )
        self.setLayout( main_layout )

        # Text entry to filter the cards in the library
        search_card = QtWidgets.QLineEdit( placeholderText="Search" )
        search_card.textChanged.connect( self.update_pattern )
        main_layout.addWidget( search_card )
        self.search_card = search_card

        # Library model with sort and filter features
        library_model = LibraryModel()
        self.library_model = library_model

        library_filter = LibraryFilter()
        library_filter.setSourceModel( library_model )
        self.library_filter = library_filter

        # List that contains all cards in the library
        cards_list = QtWidgets.QListView()
        cards_list.setModel( library_filter )
        cards_list.selectionModel().currentChanged.connect( self.current_changed )
        main_layout.addWidget( cards_list )
        self.cards_list = cards_list

    def update_pattern ( self, pattern ):
        # Update the text search pattern and filter the cards list
        self.library_filter.setFilterFixedString( pattern )

    def current_changed ( self ):
        # Get the index of the current selected card and emit a signal with it
        current_index = self.cards_list.currentIndex()
        source_index = self.library_filter.mapToSource( current_index )
        card_target = LIBRARY[ source_index.row() ]
        self.card_changed.emit( card_target )
