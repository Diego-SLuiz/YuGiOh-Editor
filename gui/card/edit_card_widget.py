from PySide6 import QtWidgets
from gui.card.card_enums import TypesFilter
from gui.card.library_widget import LibraryWidget
from gui.card.edit_data_widget import EditDataWidget
from gui.card.edit_fusion_widget import EditFusionWidget
from gui.card.edit_equip_widget import EditEquipWidget
from gui.card.edit_ritual_widget import EditRitualWidget

class EditCardWidget ( QtWidgets.QWidget ):

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
        library_widget.card_changed.connect( self.update_editor_pages )
        main_layout.addWidget( library_widget, 1 )
        self.library_widget = library_widget

        # Card editor navigation tabs
        editor_tabs = QtWidgets.QTabWidget()
        editor_tabs.currentChanged.connect( self.load_editor_pages )
        main_layout.addWidget( editor_tabs, 2 )
        self.editor_tabs = editor_tabs

        # Data editor widget
        data_editor = EditDataWidget()
        editor_tabs.addTab( data_editor, "Data" )
        self.data_editor = data_editor

        # Fusion editor widget
        fusion_editor = EditFusionWidget()
        editor_tabs.addTab( fusion_editor, "Fusions" )
        self.fusion_editor = fusion_editor

        # Equip editor widget
        equip_editor = EditEquipWidget()
        editor_tabs.addTab( equip_editor, "Equips" )
        self.equip_editor = equip_editor

        # Ritual editor widget
        ritual_editor = EditRitualWidget()
        editor_tabs.addTab( ritual_editor, "Rituals" )
        self.ritual_editor = ritual_editor

    def load_editor_pages ( self, index ):
        # Filter the library to work with the appropriate card types
        if index == 2:
            self.library_widget.change_types_filter( TypesFilter.EQUIP )

        elif index == 3:
            self.library_widget.change_types_filter( TypesFilter.RITUAL )

        else:
            self.library_widget.change_types_filter( TypesFilter.DEFAULT )

    def update_editor_pages ( self, card ):
        # Update the data of the current active editor page
        current_index = self.editor_tabs.currentIndex()

        if current_index == 0:
            self.data_editor.change_working_card( card )

        elif current_index == 1:
            self.fusion_editor.change_working_card( card )

        elif current_index == 2:
            self.equip_editor.change_working_card( card )

        elif current_index == 3:
            self.ritual_editor.change_working_card( card )
