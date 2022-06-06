from PySide6 import QtCore, QtGui
from scripts.card.card_editor import LIBRARY

class LibrarySort ( QtCore.QSortFilterProxyModel ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__()
        self.accept_types = None
        self.reject_types = None

    def filterAcceptsRow ( self, source_row, source_parent ):
        card = LIBRARY[source_row]

        if self.accept_types and not card.type in self.accept_types:
            return False

        if self.reject_types and card.type in self.reject_types:
            return False

        pattern = self.filterRegularExpression()
        source_model = self.sourceModel()
        source_index = source_model.index( source_row, 0, source_parent )
        source_data = source_model.data( source_index, QtCore.Qt.ItemDataRole.DisplayRole )

        if not pattern.match( source_data ).hasMatch():
            return False

        return True

    def set_accept_types ( self, types ):
        self.accept_types = types
        self.invalidateFilter()

    def set_reject_types ( self, types ):
        self.reject_types = types
        self.invalidateFilter()
