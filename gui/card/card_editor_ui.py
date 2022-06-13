from PySide6 import QtWidgets
from gui.card.library_widget import LibraryWidget
from gui.card.card_data_ui import DataEditor
from gui.card.card_fusion_ui import FusionEditor
from gui.card.card_equip_ui import EquipEditor
from gui.card.card_ritual_ui import RitualEditor

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
        data_editor = DataEditor()
        library_widget.card_changed.connect( data_editor.card_preview.create_preview_image )
        editor_tabs.addTab( data_editor, "Data" )

        # Fusion editor widget
        fusion_editor = FusionEditor()
        library_widget.card_changed.connect( fusion_editor.initialize_fusions_table )
        editor_tabs.addTab( fusion_editor, "Fusions" )

        # Equip editor widget
        equip_editor = EquipEditor()
        library_widget.card_changed.connect( equip_editor.initialize_equips_table )
        editor_tabs.addTab( equip_editor, "Equips" )

        # Ritual editor widget
        ritual_editor = RitualEditor()
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
