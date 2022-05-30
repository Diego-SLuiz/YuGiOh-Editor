from PySide6 import QtWidgets, QtGui, QtCore
from PIL.ImageQt import ImageQt
from gui.custom_widgets import CardPreview, ImageDialog
from scripts.card import LIBRARY, Card
from scripts.references import *

class LibraryModel ( QtCore.QAbstractListModel ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.source = LIBRARY

    def rowCount ( self, parent ):
        return len( self.source )

    def data ( self, index, role ):
        if not index.isValid(): return

        card = self.source[index.row()]

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return f"{card.number + 1:03d} - {card.name}"

        elif role == QtCore.Qt.ItemDataRole.DecorationRole:
            return QtGui.QPixmap.fromImage( ImageQt( card.miniature_image ) )

class LibraryList ( QtWidgets.QWidget ):

    card_changed = QtCore.Signal( Card )

    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins( 0, 0, 0, 0 )
        self.setLayout( layout )

        search_card = QtWidgets.QLineEdit( placeholderText="Search" )
        search_card.textChanged.connect( self.filter_cards )
        layout.addWidget( search_card )
        self.search_card = search_card

        library_model = QtCore.QSortFilterProxyModel()
        library_model.setSourceModel( LibraryModel() )
        library_model.setFilterCaseSensitivity( QtCore.Qt.CaseInsensitive.CaseInsensitive )
        library_view = QtWidgets.QListView()
        library_view.setModel( library_model )
        library_view.selectionModel().selectionChanged.connect( self.current_card )

        layout.addWidget( library_view )
        self.library_view = library_view

    def reset_library ( self ):
        self.library_view.model().beginResetModel()
        self.library_view.model().endResetModel()

    def filter_cards ( self ):
        filter_value = self.search_card.text()
        filter_model = self.library_view.model()
        filter_model.setFilterRegularExpression( filter_value )

    def current_card ( self ):
        filter_model = self.library_view.model()
        filter_index = self.library_view.currentIndex()
        source_index = filter_model.mapToSource( filter_index )
        card_target = LIBRARY[source_index.row()]
        self.card_changed.emit( card_target )

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

class DataEditor ( QtWidgets.QWidget ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        # Card default properties
        card_types = ["None"] + [x.capitalize() for x in TYPES]
        card_attributes = ["None"] + [x.capitalize() for x in ATTRIBUTES]
        card_guardians = ["None"] + [x.capitalize() for x in GUARDIANS]

        # Input data widgets
        layout = QtWidgets.QFormLayout()
        self.setLayout( layout )

        search_artwork = QtWidgets.QPushButton( "Select" )
        search_artwork.clicked.connect( self.set_artwork )
        layout.addRow( "Artwork", search_artwork )

        search_miniature = QtWidgets.QPushButton( "Select" )
        search_miniature.clicked.connect( self.set_miniature )
        layout.addRow( "Miniature", search_miniature )

        enter_title = QtWidgets.QLineEdit( placeholderText="Card Title", maxLength=36 )
        enter_title.editingFinished.connect( self.set_title )
        layout.addRow( "Title", enter_title )

        enter_name = QtWidgets.QLineEdit( placeholderText="Card Name", maxLength=36 )
        enter_name.editingFinished.connect( self.set_name )
        layout.addRow( "Name", enter_name )

        enter_info = QtWidgets.QLineEdit( placeholderText="Card Info", maxLength=140 )
        enter_info.editingFinished.connect( self.set_info )
        layout.addRow( "Info", enter_info )

        select_type = QtWidgets.QComboBox()
        select_type.addItems( card_types )
        select_type.currentIndexChanged.connect( self.set_type )
        layout.addRow( "Type", select_type )

        select_attribute = QtWidgets.QComboBox()
        select_attribute.addItems( card_attributes )
        select_attribute.currentIndexChanged.connect( self.set_attribute )
        layout.addRow( "Attribute", select_attribute )

        select_guardian_1 = QtWidgets.QComboBox()
        select_guardian_1.addItems( card_guardians )
        select_guardian_1.currentIndexChanged.connect( self.set_guardian )
        layout.addRow( "Guardian #1", select_guardian_1 )

        select_guardian_2 = QtWidgets.QComboBox()
        select_guardian_2.addItems( card_guardians )
        select_guardian_2.currentIndexChanged.connect( self.set_guardian )
        layout.addRow( "Guardian #2", select_guardian_2 )

        input_level = QtWidgets.QSpinBox( minimum=0, maximum=12 )
        input_level.valueChanged.connect( self.set_level )
        layout.addRow( "Level", input_level )

        input_attack = QtWidgets.QSpinBox( minimum=0, maximum=5000, singleStep=50 )
        input_attack.valueChanged.connect( self.set_attack )
        layout.addRow( "Attack", input_attack )

        input_defense = QtWidgets.QSpinBox( minimum=0, maximum=5000, singleStep=50 )
        input_defense.valueChanged.connect( self.set_defense )
        layout.addRow( "Defense", input_defense )

        input_price = QtWidgets.QSpinBox( minimum=0, maximum=999999, singleStep=100 )
        input_price.valueChanged.connect( self.set_price )
        layout.addRow( "Price", input_price )

        input_password = QtWidgets.QSpinBox( minimum=0, maximum=99999999 )
        layout.addRow( "Password", input_password )
        input_password.valueChanged.connect( self.set_password )

    def set_artwork ( self ):
        ImageDialog().exec()
        print( "Set Artwork" )

    def set_miniature ( self ):
        ImageDialog().exec()
        print( "Set Miniature" )

    def set_title ( self ):
        print( "Set Title" )

    def set_name ( self ):
        print( "Set Name" )

    def set_info ( self ):
        print( "Set Info" )

    def set_type ( self ):
        print( "Set Type" )

    def set_attribute ( self ):
        print( "Set Attribute" )

    def set_guardian ( self ):
        print( "Set Guardian" )

    def set_level ( self ):
        print( "Set Level" )

    def set_attack ( self ):
        print( "Set Attack" )

    def set_defense ( self ):
        print( "Set Defense" )

    def set_price ( self ):
        print( "Set Price" )

    def set_password ( self ):
        print( "Set Password" )

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

class CardSearch ( QtWidgets.QGroupBox ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets( self ):
        # Card default properties
        card_types = ["None"] + [x.capitalize() for x in TYPES]
        card_attributes = ["None"] + [x.capitalize() for x in ATTRIBUTES]
        card_guardians = ["None"] + [x.capitalize() for x in GUARDIANS]

        # Main widget layout
        layout = QtWidgets.QFormLayout()
        self.setLayout( layout )

        # Card filter properties
        input_id = QtWidgets.QSpinBox( minimum=0, maximum=722 )
        layout.addRow( "Number", input_id )

        select_type = QtWidgets.QComboBox()
        select_type.addItems( card_types )
        layout.addRow( "Type", select_type )

        select_attribute = QtWidgets.QComboBox()
        select_attribute.addItems( card_attributes )
        layout.addRow( "Attribute", select_attribute )

        select_guardian = QtWidgets.QComboBox()
        select_guardian.addItems( card_guardians )
        layout.addRow( "Guardian", select_guardian )

        select_group = QtWidgets.QComboBox()
        select_group.addItems( ["Unique Fusion", "Ritual Monster"] )
        layout.addRow( "Group", select_group )

        level_range = QtWidgets.QHBoxLayout()
        minimum_level = QtWidgets.QSpinBox( minimum=0, maximum=12 )
        level_range.addWidget( minimum_level )
        maximum_level = QtWidgets.QSpinBox( minimum=0, maximum=12 )
        level_range.addWidget( maximum_level )
        layout.addRow( "Level Range", level_range )

        attack_range = QtWidgets.QHBoxLayout()
        minimum_attack = QtWidgets.QSpinBox( minimum=0, maximum=5000 )
        attack_range.addWidget( minimum_attack )
        maximum_attack = QtWidgets.QSpinBox( minimum=0, maximum=5000 )
        attack_range.addWidget( maximum_attack )
        layout.addRow( "Attack Range", attack_range )

        defense_range = QtWidgets.QHBoxLayout()
        minimum_defense = QtWidgets.QSpinBox( minimum=0, maximum=5000 )
        defense_range.addWidget( minimum_defense )
        maximum_defense = QtWidgets.QSpinBox( minimum=0, maximum=5000 )
        defense_range.addWidget( maximum_defense )
        layout.addRow( "Defense Range", defense_range )

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

class EquipEditor ( QtWidgets.QWidget ):
    pass

class RitualEditor ( QtWidgets.QWidget ):
    pass

class CardEditor ( QtWidgets.QWidget ):

    def __init__ ( self ):
        super().__init__()
        self.setWindowTitle( "Yu-Gi-Oh! Game Maker" )
        self.create_widgets()

    def create_widgets ( self ):
         # Main card editor layout
        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout( main_layout )

        # Main library widget
        library_list = LibraryList()
        main_layout.addWidget( library_list, 1 )
        self.library_list = library_list

        # Card editor pages
        editor_tabs = QtWidgets.QTabWidget()
        main_layout.addWidget( editor_tabs, 2 )

        # Data editor page
        card_preview = CardPreview()
        card_preview.setSizePolicy( QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding )
        card_preview.setAlignment( QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop )
        card_preview.setMinimumWidth( 140 )
        card_preview.setMaximumWidth( 280 )
        library_list.card_changed.connect( card_preview.create_preview_image )

        data_editor = DataEditor()
        data_editor.setSizePolicy( QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum )

        data_editor_layout = QtWidgets.QHBoxLayout()
        data_editor_layout.addWidget( card_preview, 2 )
        data_editor_layout.addWidget( data_editor, 1 )

        data_editor_widget = QtWidgets.QWidget()
        data_editor_widget.setLayout( data_editor_layout )
        editor_tabs.addTab( data_editor_widget, "Data" )

        # Fusion editor page
        fusion_editor = FusionEditor()
        library_list.card_changed.connect( fusion_editor.fusions_table.initialize_model )
        editor_tabs.addTab( fusion_editor, "Fusions" )
