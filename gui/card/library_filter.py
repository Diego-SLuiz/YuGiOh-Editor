from PySide6 import QtCore
from scripts.card.card_editor import LIBRARY

class LibraryFilter ( QtCore.QSortFilterProxyModel ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.accept_types = None
        self.reject_types = None

    def filterAcceptsRow ( self, source_row, source_parent ):
        # Accept any row where the card in that row satisfy the type requirement and match the search pattern
        card = LIBRARY[ source_row ]
        pattern = self.filterRegularExpression()
        source_model = self.sourceModel()
        source_index = source_model.index( source_row, 0, source_parent )
        source_data = source_model.data( source_index, QtCore.Qt.ItemDataRole.DisplayRole )

        if self.accept_types and not card.type in self.accept_types or self.reject_types and card.type in self.reject_types:
            return False

        if not pattern.match( source_data ).hasMatch():
            return False

        return True

    def change_types_filter ( self, types_filter ):
        # Change the type requirement that cards must have when applying filter
        self.accept_types = types_filter.value[ 0 ]
        self.reject_types = types_filter.value[ 1 ]
        self.invalidateRowsFilter()

    def reset_types_filter ( self ):
        # Invalidate the current filter and display all cards of library
        self.accept_types = None
        self.reject_types = None
        self.invalidateRowsFilter()
