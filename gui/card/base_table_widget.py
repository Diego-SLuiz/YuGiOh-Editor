from PySide6 import QtWidgets
from gui.card.base_table_model import BaseTableModel
from gui.card.base_table_filter import BaseTableFilter

class BaseTableWidget ( QtWidgets.QWidget ):

    def __init__ ( self, header_label, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.header_label = header_label
        self.create_widgets()

    def create_widgets ( self ):
        # Main widget layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins( 0, 0, 0, 0 )
        self.setLayout( main_layout )

        # Card table model with filter features
        table_model = BaseTableModel( [], self.header_label )
        self.table_model = table_model

        table_filter = BaseTableFilter()
        table_filter.setSourceModel( table_model )
        self.table_filter = table_filter

        # Text entry to filter the table with cards
        search_entry = QtWidgets.QLineEdit( placeholderText="Search" )
        search_entry.textChanged.connect( self.update_text_pattern )
        main_layout.addWidget( search_entry )

        # Table view that shows the cards
        cards_table = QtWidgets.QTableView()
        cards_table.setModel( table_filter )
        cards_table.horizontalHeader().setSectionResizeMode( QtWidgets.QHeaderView.ResizeMode.Stretch )
        main_layout.addWidget( cards_table )

    def update_text_pattern ( self, pattern ):
        # Update the search pattern when filtering the table
        self.table_filter.setFilterFixedString( pattern )

    def update_source_data ( self, source_data ):
        # Change the source of data for the table
        self.table_model.change_source( source_data )
