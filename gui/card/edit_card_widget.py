from PySide6 import QtWidgets
from gui.card.library_widget import LibraryWidget
from gui.card.edit_data_widget import EditDataWidget
from gui.card.edit_fusion_widget import EditFusionWidget
from gui.card.edit_equip_widget import EditEquipWidget
from gui.card.edit_ritual_widget import EditRitualWidget

class CardEditor ( QtWidgets.QWidget ):

    def __init__ ( self ):
        super().__init__()
        self.setWindowTitle( "Yu-Gi-Oh! Game Maker" )
        self.create_widgets()

    def create_widgets ( self ):
        # Main widget layout
        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout( main_layout )

        # Library widget
        library_widget = LibraryWidget()
        main_layout.addWidget( library_widget, 1 )
        self.library_widget = library_widget

        # Card editor navigation tabs
        editor_tabs = QtWidgets.QTabWidget()
        editor_tabs.currentChanged.connect( self.load_editor_page )
        main_layout.addWidget( editor_tabs, 2 )

        # Data editor widget
        data_editor = EditDataWidget()
        library_widget.card_changed.connect( data_editor.card_preview.create_preview_image )
        editor_tabs.addTab( data_editor, "Data" )

        # Fusion editor widget
        fusion_editor = EditFusionWidget()
        library_widget.card_changed.connect( fusion_editor.initialize_fusions_table )
        editor_tabs.addTab( fusion_editor, "Fusions" )

        # Equip editor widget
        equip_editor = EditEquipWidget()
        library_widget.card_changed.connect( equip_editor.initialize_equips_table )
        editor_tabs.addTab( equip_editor, "Equips" )

        # Ritual editor widget
        ritual_editor = EditRitualWidget()
        library_widget.card_changed.connect( ritual_editor.initialize_rituals_table )
        editor_tabs.addTab( ritual_editor, "Rituals" )

    def load_editor_page ( self, index ):
        # Filter the library to work with the appropriate card types
        if index == 2:
            self.library_widget.update_types_filter( [ "equip" ],  None )

        elif index == 3:
            self.library_widget.update_types_filter( [ "ritual" ], None )

        else:
            self.library_widget.update_types_filter( None, None )
