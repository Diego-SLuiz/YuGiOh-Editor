from PySide6 import QtWidgets, QtCore
from scripts.card.references import *
from gui.utilities.image_editor_dialog import ImageEditorDialog
from gui.utilities.card_preview_widget import CardPreviewWidget

class EditDataWidget ( QtWidgets.QWidget ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()
        self.working_card = None
        self.image_editor = ImageEditorDialog( self )

    def create_widgets ( self ):
        # Card default properties
        card_types = [ "None" ] + [ x.capitalize() for x in TYPES ]
        card_attributes = [ "None" ] + [ x.capitalize() for x in ATTRIBUTES ]
        card_guardians = [ "None" ] + [ x.capitalize() for x in GUARDIANS ]

        # Main widget layout
        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout( main_layout )

        # Card preview widget
        card_preview = CardPreviewWidget()
        card_preview.setSizePolicy( QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding )
        card_preview.setAlignment( QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop )
        main_layout.addWidget( card_preview )
        self.card_preview = card_preview

        # Data editor fields
        data_layout = QtWidgets.QFormLayout()
        main_layout.addLayout( data_layout )

        search_artwork = QtWidgets.QPushButton( "Select" )
        search_artwork.clicked.connect( self.set_artwork )
        data_layout.addRow( "Artwork", search_artwork )

        search_miniature = QtWidgets.QPushButton( "Select" )
        search_miniature.clicked.connect( self.set_miniature )
        data_layout.addRow( "Miniature", search_miniature )

        enter_title = QtWidgets.QLineEdit( placeholderText="Card Title", maxLength=36 )
        enter_title.editingFinished.connect( self.set_title )
        data_layout.addRow( "Title", enter_title )
        self.enter_title = enter_title

        enter_name = QtWidgets.QLineEdit( placeholderText="Card Name", maxLength=36 )
        enter_name.editingFinished.connect( self.set_name )
        data_layout.addRow( "Name", enter_name )
        self.enter_name = enter_name

        enter_info = QtWidgets.QLineEdit( placeholderText="Card Info", maxLength=140 )
        enter_info.editingFinished.connect( self.set_info )
        data_layout.addRow( "Info", enter_info )
        self.enter_info = enter_info

        select_type = QtWidgets.QComboBox()
        select_type.addItems( card_types )
        select_type.currentIndexChanged.connect( self.set_type )
        data_layout.addRow( "Type", select_type )
        self.select_type = select_type

        select_attribute = QtWidgets.QComboBox()
        select_attribute.addItems( card_attributes )
        select_attribute.currentIndexChanged.connect( self.set_attribute )
        data_layout.addRow( "Attribute", select_attribute )
        self.select_attribute = select_attribute

        select_guardian_1 = QtWidgets.QComboBox()
        select_guardian_1.addItems( card_guardians )
        select_guardian_1.currentIndexChanged.connect( self.set_guardian )
        data_layout.addRow( "Guardian #1", select_guardian_1 )
        self.select_guardian_1 = select_guardian_1

        select_guardian_2 = QtWidgets.QComboBox()
        select_guardian_2.addItems( card_guardians )
        select_guardian_2.currentIndexChanged.connect( self.set_guardian )
        data_layout.addRow( "Guardian #2", select_guardian_2 )
        self.select_guardian_2 = select_guardian_2

        input_level = QtWidgets.QSpinBox( minimum=0, maximum=12 )
        input_level.valueChanged.connect( self.set_level )
        data_layout.addRow( "Level", input_level )
        self.input_level = input_level

        input_attack = QtWidgets.QSpinBox( minimum=0, maximum=5000, singleStep=50 )
        input_attack.valueChanged.connect( self.set_attack )
        data_layout.addRow( "Attack", input_attack )
        self.input_attack = input_attack

        input_defense = QtWidgets.QSpinBox( minimum=0, maximum=5000, singleStep=50 )
        input_defense.valueChanged.connect( self.set_defense )
        data_layout.addRow( "Defense", input_defense )
        self.input_defense = input_defense

        input_price = QtWidgets.QSpinBox( minimum=0, maximum=999999, singleStep=100 )
        input_price.valueChanged.connect( self.set_price )
        data_layout.addRow( "Price", input_price )
        self.input_price = input_price

        input_password = QtWidgets.QSpinBox( minimum=0, maximum=99999999 )
        data_layout.addRow( "Password", input_password )
        input_password.valueChanged.connect( self.set_password )
        self.input_password = input_password

    def change_working_card ( self, card ):
        # Update the current working card
        self.working_card = card
        self.card_preview.create_preview_image( card )
        self.get_data()

    def get_data ( self ):
        # Update the current card display data
        card = self.working_card

        self.enter_title.setText( card.name )
        self.enter_name.setText( card.name )
        self.enter_info.setText( card.info )

        type_index = self.select_type.findText( card.type.capitalize(), QtCore.Qt.MatchFlag.MatchExactly )
        self.select_type.setCurrentIndex( type_index )

        attribute_index = self.select_attribute.findText( card.attribute.capitalize(), QtCore.Qt.MatchFlag.MatchExactly )
        self.select_attribute.setCurrentIndex( attribute_index )

        guardian_index_1 = self.select_guardian_1.findText( card.guardian_1.capitalize(), QtCore.Qt.MatchFlag.MatchExactly )
        self.select_guardian_1.setCurrentIndex( guardian_index_1 )

        guardian_index_2 = self.select_guardian_2.findText( card.guardian_2.capitalize(), QtCore.Qt.MatchFlag.MatchExactly )
        self.select_guardian_2.setCurrentIndex( guardian_index_2 )

        self.input_level.setValue( card.level )
        self.input_attack.setValue( card.attack )
        self.input_defense.setValue( card.defense )
        self.input_price.setValue( card.price )
        self.input_password.setValue( int( card.password, 10 ) )

    def set_artwork ( self ):
        self.image_editor.exec( 102, 96, 256 )
        print( "Set Artwork" )

    def set_miniature ( self ):
        self.image_editor.exec( 40, 32, 64 )
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
