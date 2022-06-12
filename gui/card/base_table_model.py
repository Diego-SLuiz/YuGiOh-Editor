from PySide6 import QtCore
from gui.utilities.library_model import LibraryModel

class BaseTableModel ( QtCore.QAbstractTableModel ):

    def __init__ ( self, source_data, header_label, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.library_model = LibraryModel()
        self.library_model.modelReset.connect( self.reset_model )
        self.source_data = source_data
        self.header_label = header_label

    def reset_model ( self ):
        # Reset this model whenever the library model resets
        self.beginResetModel()
        self.endResetModel()

    def change_source ( self, source_data ):
        # Change the source data for this model
        self.source_data = source_data
        self.beginResetModel()
        self.endResetModel()

    def rowCount ( self, parent ):
        # Return the number of objects in the source_data
        return len( self.source_data )

    def columnCount ( self, parent ):
        # Return the number of objects in the first row of source_data
        return len( self.source_data[0] if self.source_data else [] )

    def data ( self, index, role ):
        # Return the data related to that index in the library model
        if not index.isValid():
            return

        target_id = self.source_data[ index.row() ][ index.column() ] - 1
        library_model = self.library_model
        parent_index = QtCore.QModelIndex()
        source_index = library_model.index( target_id, 0, parent_index )

        return library_model.data( source_index, role )

    def headerData ( self, section, orientation, role ):
        # Return the header label for horizontal orientation
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.header_label[ section ]

        return super().headerData( section, orientation, role )
