from PySide6 import QtCore, QtGui
from PIL.ImageQt import ImageQt
from scripts.card.card_editor import LIBRARY

class LibraryModel ( QtCore.QAbstractListModel ):

    INSTANCES = []

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.source_data = LIBRARY
        self.INSTANCES.append( self )

    @classmethod
    def reset_all_models ( cls ):
        # Reset any model instance of this class
        for model in cls.INSTANCES:
            model.beginResetModel()
            model.endResetModel()

    def rowCount ( self, parent ):
        # Return the number of cards in the library
        return len( self.source_data )

    def data ( self, index, role ):
        # Return the name and the miniature of a card
        if not index.isValid(): return

        card = self.source_data[index.row()]

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return f"{card.number + 1:03d} - {card.name}"

        elif role == QtCore.Qt.ItemDataRole.DecorationRole:
            return QtGui.QPixmap.fromImage( ImageQt( card.miniature_image ) )
