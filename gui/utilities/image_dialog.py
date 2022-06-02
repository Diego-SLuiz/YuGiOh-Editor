from PySide6 import QtWidgets

class ImageDialog ( QtWidgets.QDialog ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()

    def create_widgets ( self ):
        FOCUS_AREAS = [
            "Center",
            "Top",
            "Bottom",
            "Left",
            "Right",
            "Top-Left",
            "Top-Right",
            "Center-Left",
            "Center-Right",
            "Bottom-Left",
            "Bottom-Right"
        ]

        # Main widget layout
        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout( main_layout )

        # Working image
        main_image = QtWidgets.QLabel()
        main_layout.addWidget( main_image, 3 )

        # Image config layout
        config_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout( config_layout, 1 )

        # Image enhancements
        enhance_layout = QtWidgets.QFormLayout()
        group_enhance = QtWidgets.QGroupBox( "Image Enhancement" )
        group_enhance.setLayout( enhance_layout )
        config_layout.addWidget( group_enhance, 2 )

        enhance_color = QtWidgets.QSpinBox( suffix="%", minimum=0, maximum=200, singleStep=10 )
        enhance_color.valueChanged.connect( self.set_enhance_color )
        enhance_layout.addRow( "Color", enhance_color )

        enhance_contrast = QtWidgets.QSpinBox( suffix="%", minimum=0, maximum=200, singleStep=10 )
        enhance_contrast.valueChanged.connect( self.set_enhance_contrast )
        enhance_layout.addRow( "Contrast", enhance_contrast )

        enhance_brightness = QtWidgets.QSpinBox( suffix="%", minimum=0, maximum=200, singleStep=10 )
        enhance_brightness.valueChanged.connect( self.set_enhance_brightness )
        enhance_layout.addRow( "Brightness", enhance_brightness )

        enhance_sharpness = QtWidgets.QSpinBox( suffix="%", minimum=0, maximum=200, singleStep=10 )
        enhance_sharpness.valueChanged.connect( self.set_enhance_sharpness )
        enhance_layout.addRow( "Sharpness", enhance_sharpness )

        # Image transformations
        compress_layout = QtWidgets.QFormLayout()
        group_compress = QtWidgets.QGroupBox( "Image Compression" )
        group_compress.setLayout( compress_layout )
        config_layout.addWidget( group_compress, 2 )

        compress_width = QtWidgets.QSpinBox( suffix=" Px", minimum=0, maximum=1024 )
        compress_width.valueChanged.connect( self.set_compress_width )
        compress_layout.addRow( "Width", compress_width )

        compress_height = QtWidgets.QSpinBox( suffix=" Px", minimum=0, maximum=1024 )
        compress_height.valueChanged.connect( self.set_compress_height )
        compress_layout.addRow( "Height", compress_height )

        compress_colors = QtWidgets.QSpinBox( suffix=" Colors", minimum=0, maximum=1024 )
        compress_colors.valueChanged.connect( self.set_compress_colors )
        compress_layout.addRow( "Colors", compress_colors )

        # Transformations preferences
        preferences_layout = QtWidgets.QFormLayout()
        group_preferences = QtWidgets.QGroupBox( "Preferences" )
        group_preferences.setLayout( preferences_layout )
        config_layout.addWidget( group_preferences, 2 )

        select_focus = QtWidgets.QComboBox()
        select_focus.addItems( FOCUS_AREAS )
        select_focus.currentIndexChanged.connect( self.set_focus_area )
        preferences_layout.addRow( "Focus Area", select_focus )

        input_focus = QtWidgets.QSpinBox( suffix="%", minimum=0, maximum=100 )
        input_focus.valueChanged.connect( self.set_focus_value )
        preferences_layout.addRow( "Focus Value", input_focus )

        # Buttons actions
        button_layout = QtWidgets.QHBoxLayout()
        group_button = QtWidgets.QGroupBox()
        group_button.setLayout( button_layout )
        config_layout.addWidget( group_button, 1 )

        button_browse = QtWidgets.QPushButton( "Browse" )
        button_browse.clicked.connect( self.set_working_image )
        button_layout.addWidget( button_browse )

        button_confirm = QtWidgets.QPushButton( "Confirm" )
        button_confirm.clicked.connect( self.set_image_changes )
        button_layout.addWidget( button_confirm )

    def set_enhance_color ( self ):
        print( "Enhance Color" )

    def set_enhance_contrast ( self ):
        print( "Enhance Contrast" )

    def set_enhance_brightness ( self ):
        print( "Enhance Brightness" )

    def set_enhance_sharpness ( self ):
        print( "Enhance Sharpness" )

    def set_compress_width ( self ):
        print( "Compress Width" )

    def set_compress_height ( self ):
        print( "Compress Height" )

    def set_compress_colors ( self ):
        print( "Compress Colors" )

    def set_focus_area ( self ):
        print( "Focus Area" )

    def set_focus_value ( self ):
        print( "Focus Value" )

    def set_working_image ( self ):
        print( "Working Image" )

    def set_image_changes ( self ):
        print( "Image Changes" )
