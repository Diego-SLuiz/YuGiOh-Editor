from PIL.ImageQt import ImageQt
from PySide6 import QtCore, QtGui
from scripts.card.card_editor import LIBRARY

class LibraryModel ( QtCore.QAbstractListModel ):

    INSTANCES = []

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.source = LIBRARY
        self.INSTANCES.append( self )

    def rowCount ( self, parent ):
        return len( self.source )

    def data ( self, index, role ):
        if not index.isValid(): return

        card = self.source[index.row()]

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return f"{card.number + 1:03d} - {card.name}"

        elif role == QtCore.Qt.ItemDataRole.DecorationRole:
            return QtGui.QPixmap.fromImage( ImageQt( card.miniature_image ) )

    @classmethod
    def update_library ( cls ):
        for model in cls.INSTANCES:
            model.beginResetModel()
            model.endResetModel()
