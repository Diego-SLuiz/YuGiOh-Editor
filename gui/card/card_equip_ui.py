from PySide6 import QtWidgets, QtCore
from gui.utilities.card_selector import CardSelector
from gui.utilities.library_model import LibraryModel
from gui.utilities.card_search import CardSearch
from gui.utilities.card_preview import CardPreview

class EquipSort ( QtCore.QSortFilterProxyModel ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )

class EquipModel ( QtCore.QAbstractTableModel ):

    def __init__ ( self, source, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.source_data = source
        self.source_model = LibraryModel()
        self.header = [ "Equip Spell", "Compatible Monsters" ]

    def rowCount ( self, parent ):
        return len( self.source_data )

    def columnCount ( self, parent ):
        return 2

    def data ( self, index, role ):
        if not index.isValid():
            return

        target_id = self.source_data[index.row()][index.column()] - 1
        parent_index = QtCore.QModelIndex()
        source_index = self.source_model.index( target_id, 0, parent_index )

        return self.source_model.data( source_index, role )

    def headerData ( self, section, orientation, role ):
        if role == QtCore.Qt.ItemDataRole.DisplayRole and orientation == QtCore.Qt.Orientation.Horizontal:
            return self.header[section]

        return super().headerData( section, orientation, role )

class EquipTable ( QtWidgets.QWidget ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout( layout )

        search_bar = QtWidgets.QLineEdit( placeholderText="Search" )
        search_bar.textChanged.connect( self.search_equip )
        layout.addWidget( search_bar )
        self.search_bar = search_bar

        table_view = QtWidgets.QTableView()
        table_view.horizontalHeader().setSectionResizeMode( QtWidgets.QHeaderView.ResizeMode.Stretch )
        layout.addWidget( table_view )
        self.table_view = table_view

    def initialize_model ( self, card ):
        equips_list = [ [ card.number + 1, x ] for x in card.equips_list ]
        self.table_view.setModel( EquipModel( equips_list ) )

    def search_equip ( self ):
        pass

class EquipFilter ( QtWidgets.QDialog ):

    def __init__( self, *args, **kwargs ):
        super().__init__()
        self.create_widgets()

    def create_widgets ( self ):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout( layout )

        equip_cards_layout = QtWidgets.QHBoxLayout()
        layout.addLayout( equip_cards_layout )

        monster_filter = CardSearch( "Monster Card" )
        monster_filter.setSizePolicy( QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding )
        equip_cards_layout.addWidget( monster_filter )

        equip_selector_group = QtWidgets.QGroupBox( "Equip Card" )
        equip_cards_layout.addWidget( equip_selector_group )

        equip_selector_layout = QtWidgets.QVBoxLayout()
        equip_selector_group.setLayout( equip_selector_layout )

        equip_selector = CardSelector()
        equip_selector_layout.addWidget( equip_selector )

        equip_preview = CardPreview()
        equip_preview.setMinimumWidth( 140 )
        equip_preview.setMaximumWidth( 280 )
        equip_preview.setAlignment( QtCore.Qt.AlignmentFlag.AlignCenter )
        equip_preview.setSizePolicy( QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding )
        equip_selector.card_selected.connect( equip_preview.create_preview_image )
        equip_selector.card_selected.connect( equip_preview.create_preview_image )
        equip_selector_layout.addWidget( equip_preview )

        buttons_action_group = QtWidgets.QGroupBox()
        layout.addWidget( buttons_action_group )

        buttons_action_layout = QtWidgets.QHBoxLayout()
        buttons_action_group.setLayout( buttons_action_layout )

        confirm_button = QtWidgets.QPushButton( "Confirm" )
        confirm_button.clicked.connect( self.on_confirm )
        buttons_action_layout.addWidget( confirm_button )

        cancel_button = QtWidgets.QPushButton( "Cancel" )
        cancel_button.clicked.connect( self.on_cancel )
        buttons_action_layout.addWidget( cancel_button )

    def on_confirm ( self ):
        print( "Confirm" )

    def on_cancel ( self ):
        print( "Cancel" )

class EquipEditor ( QtWidgets.QWidget ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()
        self.equip_filter = EquipFilter()

    def create_widgets ( self ):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout( layout )

        equips_table = EquipTable()
        layout.addWidget( equips_table )
        self.equips_table = equips_table

        buttons_group = QtWidgets.QGroupBox( "Actions" )
        layout.addWidget( buttons_group )

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_group.setLayout( buttons_layout )

        add_equip = QtWidgets.QPushButton( "Add Equip" )
        add_equip.clicked.connect( self.add_card_equip )
        buttons_layout.addWidget( add_equip )

        del_equip = QtWidgets.QPushButton( "Del Equip" )
        del_equip.clicked.connect( self.del_card_equip )
        buttons_layout.addWidget( del_equip )

        add_many = QtWidgets.QPushButton( "Add Many" )
        add_many.clicked.connect( self.add_many_cards )
        buttons_layout.addWidget( add_many )

        del_many = QtWidgets.QPushButton( "Del Many" )
        del_many.clicked.connect( self.del_many_cards )
        buttons_layout.addWidget( del_many )

        clear_card = QtWidgets.QPushButton( "Clear Card" )
        clear_card.clicked.connect( self.clear_card_equips )
        buttons_layout.addWidget( clear_card )

    def add_card_equip ( self ):
        print( "Add Equip Card" )

    def del_card_equip ( self ):
        print( "Del Equip Card" )

    def add_many_cards ( self ):
        self.equip_filter.exec()
        print( "Add Many Equips" )

    def del_many_cards ( self ):
        self.equip_filter.exec()
        print( "Del Many Equips" )

    def clear_card_equips ( self ):
        print( "Clear Card Equips" )
