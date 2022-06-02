from PySide6 import QtWidgets, QtCore
from gui.utilities.library_model import LibraryModel
from gui.utilities.card_search import CardSearch
from gui.utilities.card_selector import CardSelector

class FusionsModel ( QtCore.QAbstractTableModel ):

    def __init__( self, fusions,  *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.source_data = fusions
        self.source_model = LibraryModel()
        self.header = ["Material #1", "Material #2", "Result"]

    def rowCount( self, parent ):
        return len( self.source_data )

    def columnCount( self, parent ):
        return 3

    def headerData( self, section, orientation, role ):
        if role == QtCore.Qt.ItemDataRole.DisplayRole and orientation == QtCore.Qt.Orientation.Horizontal:
            return self.header[section]

        return super().headerData( section, orientation, role )

    def data( self, index, role ):
        if not index.isValid(): return

        target_id = self.source_data[index.row()][index.column()] - 1
        parent_index = QtCore.QModelIndex()
        new_index = self.source_model.index( target_id, 0, parent_index )

        return self.source_model.data( new_index, role )

class FusionsTable ( QtWidgets.QWidget ):

    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        # Main widget layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout( layout )

        search_card = QtWidgets.QLineEdit( placeholderText="Search" )
        layout.addWidget( search_card )
        self.search_card = search_card

        table_view = QtWidgets.QTableView()
        table_view.horizontalHeader().setSectionResizeMode( QtWidgets.QHeaderView.ResizeMode.Stretch )
        layout.addWidget( table_view )
        self.table_view = table_view

    def initialize_model ( self, card ):
        self.table_view.setModel( FusionsModel( card.fusions_list ) )

    def reset_model ( self ):
        pass

class FusionsFilter ( QtWidgets.QDialog ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()
        self.setWindowTitle( "Filter Fusions" )

    def create_widgets ( self ):
        # Main layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout( layout )

        materials_layout = QtWidgets.QHBoxLayout()
        layout.addLayout( materials_layout )

        material_1 = CardSearch( "Material #1" )
        materials_layout.addWidget( material_1 )

        material_2 = CardSearch( "Material #2" )
        materials_layout.addWidget( material_2 )

        result = CardSelector()
        materials_layout.addWidget( result )

        # Buttons group
        buttons_group = QtWidgets.QGroupBox( "Actions" )
        buttons_group.setSizePolicy( QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum )
        layout.addWidget( buttons_group )

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_group.setLayout( buttons_layout )

        confirm_button = QtWidgets.QPushButton( "Confirm" )
        confirm_button.clicked.connect( self.accept )
        buttons_layout.addWidget( confirm_button )

        cancel_button = QtWidgets.QPushButton( "Cancel" )
        cancel_button.clicked.connect( self.reject )
        buttons_layout.addWidget( cancel_button )

class FusionEditor ( QtWidgets.QWidget ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        # Main layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout( layout )

        # Fusions table
        fusions_table = FusionsTable()
        layout.addWidget( fusions_table )
        self.fusions_table = fusions_table

        # Buttons group
        buttons_group = QtWidgets.QGroupBox( "Actions" )
        layout.addWidget( buttons_group )

        # Buttons layout
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_group.setLayout( buttons_layout )

        # Buttons actions
        add_fusion = QtWidgets.QPushButton( "Add Fusion" )
        add_fusion.clicked.connect( self.add_card_fusion )
        buttons_layout.addWidget( add_fusion )

        del_fusion = QtWidgets.QPushButton( "Del Fusion" )
        del_fusion.clicked.connect( self.del_card_fusion )
        buttons_layout.addWidget( del_fusion )

        add_many = QtWidgets.QPushButton( "Add Many" )
        add_many.clicked.connect( self.add_many_fusions )
        buttons_layout.addWidget( add_many )

        del_many = QtWidgets.QPushButton( "Del Many" )
        del_many.clicked.connect( self.del_many_fusions )
        buttons_layout.addWidget( del_many )

        clear_card = QtWidgets.QPushButton( "Clear Card" )
        clear_card.clicked.connect( self.clear_card_fusions )
        buttons_layout.addWidget( clear_card )

        # Define other widgets
        self.fusions_filter = FusionsFilter( self, modal=True )

    def add_card_fusion ( self ):
        print( "Add One Fusion" )

    def del_card_fusion ( self ):
        print( "Del One Fusion" )

    def add_many_fusions ( self ):
        print( "Add Many Fusions" )
        self.fusions_filter.exec()

    def del_many_fusions ( self ):
        print( "Del Many Fusions" )
        self.fusions_filter.exec()

    def clear_card_fusions ( self ):
        print( "Clear Card Fusions" )
