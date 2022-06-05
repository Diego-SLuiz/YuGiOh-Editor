from PySide6 import QtWidgets, QtCore
from gui.utilities.card_preview import CardPreview
from gui.utilities.library_model import LibraryModel
from gui.utilities.card_search import CardSearch
from gui.utilities.card_selector import CardSelector

class FusionSort ( QtCore.QSortFilterProxyModel ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )

    def filterAcceptsRow ( self, source_row, source_parent ):
        pattern = self.filterRegularExpression()
        role = QtCore.Qt.ItemDataRole.DisplayRole
        model = self.sourceModel()
        match = any( [ pattern.match( x ).hasMatch() for x in [ model.data( model.index( source_row, i, source_parent ), role ) for i in range( model.columnCount( source_parent ) ) ] ] )

        if match:
            return True

        return False

class FusionModel ( QtCore.QAbstractTableModel ):

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
        if not index.isValid():
            return

        target_id = self.source_data[index.row()][index.column()] - 1
        parent_index = QtCore.QModelIndex()
        new_index = self.source_model.index( target_id, 0, parent_index )

        return self.source_model.data( new_index, role )

class FusionTable ( QtWidgets.QWidget ):

    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        # Main widget layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout( layout )

        search_card = QtWidgets.QLineEdit( placeholderText="Search" )
        search_card.textChanged.connect( self.search_fusion )
        layout.addWidget( search_card )
        self.search_card = search_card

        table_view = QtWidgets.QTableView()
        table_view.horizontalHeader().setSectionResizeMode( QtWidgets.QHeaderView.ResizeMode.Stretch )
        layout.addWidget( table_view )
        self.table_view = table_view

    def initialize_model ( self, card ):
        table_model = FusionSort()
        table_model.setSourceModel( FusionModel( card.fusions_list ) )
        table_model.setFilterCaseSensitivity( QtCore.Qt.CaseSensitivity.CaseInsensitive )
        self.table_view.setModel( table_model )

    def search_fusion ( self, text ):
        self.table_view.model().setFilterRegularExpression( text )

class FusionFilter ( QtWidgets.QDialog ):

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
        material_1.setSizePolicy( QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding )
        materials_layout.addWidget( material_1 )
        self.material_1 = material_1

        material_2 = CardSearch( "Material #2" )
        material_2.setSizePolicy( QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding )
        materials_layout.addWidget( material_2 )
        self.material_2 = material_2

        result_group = QtWidgets.QGroupBox( "Result" )
        materials_layout.addWidget( result_group )

        result_layout = QtWidgets.QVBoxLayout()
        result_group.setLayout( result_layout )

        card_selector = CardSelector()
        result_layout.addWidget( card_selector )

        card_preview = CardPreview()
        card_preview.setMinimumWidth( 140 )
        card_preview.setMaximumWidth( 280 )
        card_preview.setAlignment( QtCore.Qt.AlignmentFlag.AlignCenter )
        card_preview.setSizePolicy( QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding )
        card_selector.card_selected.connect( card_preview.create_preview_image )
        result_layout.addWidget( card_preview )

        # Buttons group
        buttons_group = QtWidgets.QGroupBox( "Actions" )
        buttons_group.setSizePolicy( QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum )
        layout.addWidget( buttons_group )

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_group.setLayout( buttons_layout )

        confirm_button = QtWidgets.QPushButton( "Confirm" )
        confirm_button.clicked.connect( self.get_filter )
        buttons_layout.addWidget( confirm_button )

        cancel_button = QtWidgets.QPushButton( "Cancel" )
        cancel_button.clicked.connect( self.reject )
        buttons_layout.addWidget( cancel_button )

    def get_filter ( self ):
        self.material_1.search_result()
        self.material_2.search_result()
        self.accept()

class FusionEditor ( QtWidgets.QWidget ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        # Main layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout( layout )

        # Fusions table
        fusions_table = FusionTable()
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
        self.fusions_filter = FusionFilter( self, modal=True )

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
