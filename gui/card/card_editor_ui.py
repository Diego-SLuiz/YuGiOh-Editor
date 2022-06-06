from PySide6 import QtWidgets, QtCore
from scripts.card.card_editor import Card, LIBRARY
from gui.utilities.library_model import LibraryModel
from gui.utilities.library_sort import LibrarySort
from gui.card.card_data_ui import DataEditor
from gui.card.card_fusion_ui import FusionEditor
from gui.card.card_equip_ui import EquipEditor

class LibraryList ( QtWidgets.QWidget ):

    card_changed = QtCore.Signal( Card )

    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        # Main layout
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins( 0, 0, 0, 0 )
        self.setLayout( layout )

        # Card search input line
        search_card = QtWidgets.QLineEdit( placeholderText="Search" )
        search_card.textChanged.connect( self.filter_cards )
        layout.addWidget( search_card )
        self.search_card = search_card

        # Model with sort proxy
        library_model = LibrarySort()
        library_model.setSourceModel( LibraryModel() )
        library_model.setFilterCaseSensitivity( QtCore.Qt.CaseInsensitive.CaseInsensitive )

        # Library view
        library_view = QtWidgets.QListView()
        library_view.setModel( library_model )
        library_view.selectionModel().currentChanged.connect( self.current_card )
        layout.addWidget( library_view )
        self.library_view = library_view

    def reset_library ( self ):
        self.library_view.model().sourceModel().beginResetModel()
        self.library_view.model().sourceModel().endResetModel()

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

        # Card editor
        editor_tabs = QtWidgets.QTabWidget()
        editor_tabs.currentChanged.connect( self.load_editor_page )
        main_layout.addWidget( editor_tabs, 2 )

        # Data editor page
        data_editor = DataEditor()
        data_editor.setSizePolicy( QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum )
        library_list.card_changed.connect( data_editor.card_preview.create_preview_image )
        editor_tabs.addTab( data_editor, "Data" )

        # Fusion editor page
        fusion_editor = FusionEditor()
        library_list.card_changed.connect( fusion_editor.fusions_table.initialize_model )
        editor_tabs.addTab( fusion_editor, "Fusions" )

        # Equip editor page
        equip_editor = EquipEditor()
        library_list.card_changed.connect( equip_editor.equips_table.initialize_model )
        editor_tabs.addTab( equip_editor, "Equips" )

    def load_editor_page ( self, index ):
        library_model = self.library_list.library_view.model()

        if index == 0 or index == 1:
            library_model.set_accept_types( None )
            library_model.set_reject_types( None )
            return

        elif index == 2:
            library_model.set_accept_types( [ "equip" ] )
            library_model.set_reject_types( None )

        elif index == 3:
            library_model.set_accept_types( [ "ritual" ] )
            library_model.set_reject_types( None )
