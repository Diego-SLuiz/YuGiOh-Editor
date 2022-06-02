from PySide6 import QtWidgets, QtCore
from scripts.card.card_editor import Card, LIBRARY
from gui.utilities.library_model import LibraryModel
from gui.utilities.card_preview import CardPreview
from gui.card.card_data_ui import DataEditor
from gui.card.card_fusion_ui import FusionEditor

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
