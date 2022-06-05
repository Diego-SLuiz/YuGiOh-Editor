from PySide6 import QtWidgets, QtCore
from scripts.card.references import *
from gui.utilities.image_dialog import ImageDialog
from gui.utilities.card_preview import CardPreview

class DataEditor ( QtWidgets.QWidget ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        # Card default properties
        card_types = ["None"] + [x.capitalize() for x in TYPES]
        card_attributes = ["None"] + [x.capitalize() for x in ATTRIBUTES]
        card_guardians = ["None"] + [x.capitalize() for x in GUARDIANS]

        # Main layout
        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout( main_layout )

        # Card preview
        card_preview = CardPreview()
        card_preview.setMinimumWidth( 140 )
        card_preview.setMaximumWidth( 280 )
        card_preview.setSizePolicy( QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding )
        card_preview.setAlignment( QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop )
        main_layout.addWidget( card_preview )
        self.card_preview = card_preview

        # Data editor
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

        enter_name = QtWidgets.QLineEdit( placeholderText="Card Name", maxLength=36 )
        enter_name.editingFinished.connect( self.set_name )
        data_layout.addRow( "Name", enter_name )

        enter_info = QtWidgets.QLineEdit( placeholderText="Card Info", maxLength=140 )
        enter_info.editingFinished.connect( self.set_info )
        data_layout.addRow( "Info", enter_info )

        select_type = QtWidgets.QComboBox()
        select_type.addItems( card_types )
        select_type.currentIndexChanged.connect( self.set_type )
        data_layout.addRow( "Type", select_type )

        select_attribute = QtWidgets.QComboBox()
        select_attribute.addItems( card_attributes )
        select_attribute.currentIndexChanged.connect( self.set_attribute )
        data_layout.addRow( "Attribute", select_attribute )

        select_guardian_1 = QtWidgets.QComboBox()
        select_guardian_1.addItems( card_guardians )
        select_guardian_1.currentIndexChanged.connect( self.set_guardian )
        data_layout.addRow( "Guardian #1", select_guardian_1 )

        select_guardian_2 = QtWidgets.QComboBox()
        select_guardian_2.addItems( card_guardians )
        select_guardian_2.currentIndexChanged.connect( self.set_guardian )
        data_layout.addRow( "Guardian #2", select_guardian_2 )

        input_level = QtWidgets.QSpinBox( minimum=0, maximum=12 )
        input_level.valueChanged.connect( self.set_level )
        data_layout.addRow( "Level", input_level )

        input_attack = QtWidgets.QSpinBox( minimum=0, maximum=5000, singleStep=50 )
        input_attack.valueChanged.connect( self.set_attack )
        data_layout.addRow( "Attack", input_attack )

        input_defense = QtWidgets.QSpinBox( minimum=0, maximum=5000, singleStep=50 )
        input_defense.valueChanged.connect( self.set_defense )
        data_layout.addRow( "Defense", input_defense )

        input_price = QtWidgets.QSpinBox( minimum=0, maximum=999999, singleStep=100 )
        input_price.valueChanged.connect( self.set_price )
        data_layout.addRow( "Price", input_price )

        input_password = QtWidgets.QSpinBox( minimum=0, maximum=99999999 )
        data_layout.addRow( "Password", input_password )
        input_password.valueChanged.connect( self.set_password )

    def get_data ( self, card ):
        print( f"Get {card.name}" )

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
