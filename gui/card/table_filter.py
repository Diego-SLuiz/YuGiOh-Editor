from PySide6 import QtCore

class TableFilter ( QtCore.QSortFilterProxyModel ):

    def filterAcceptsRow ( self, source_row, source_parent ):
        # Accepts any row that any column data match pattern
        display_role = QtCore.Qt.ItemDataRole.DisplayRole
        text_pattern = self.filterRegularExpression()
        source_model = self.sourceModel()

        column_count = source_model.columnCount( source_parent )
        column_data = [ source_model.data( source_model.index( source_row, i, source_parent ), display_role ) for i in range( column_count ) ]
        has_match = any( [ text_pattern.match( x ).hasMatch() for x in column_data ] )

        if has_match:
            return True

        return False
