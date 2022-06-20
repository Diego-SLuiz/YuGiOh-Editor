from PySide6 import QtWidgets, QtCore, QtGui
from PIL import Image, ImageQt

class EditingImage ( QtWidgets.QLabel ):

    FOCUS_ADJUST = {
        "Center": ( 0.5, 0.5, 0.5, 0.5 ),
        "Top": ( 0.5, 0, 0.5, 1 ),
        "Bottom": ( 0.5, 1, 0.5, 0 ),
        "Left": ( 0, 0.5, 1, 0.5 ),
        "Right": ( 1, 0.5, 0, 0.5 ),
        "Top-Left": ( 0, 0, 1, 1 ),
        "Top-Right": ( 1, 0, 0, 1 ),
        "Bottom-Left": ( 0, 1, 1, 0 ),
        "Bottom-Right": ( 1, 1, 0, 0 ),
    }

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.original_image = None
        self.current_image = None
        self.focus_value = 0
        self.focus_area = "Center"

    def resizeEvent ( self, event ):
        self.resize_pixmap()
        super().resizeEvent( event )

    def change_pixmap ( self, pixmap ):
        self.original_image = pixmap
        self.current_image = pixmap
        self.apply_focus()

    def resize_pixmap ( self ):
        if not self.current_image:
            return

        new_size = self.size()
        transform_mode = QtCore.Qt.TransformationMode.SmoothTransformation
        aspect_mode = QtCore.Qt.AspectRatioMode.KeepAspectRatio

        pixmap = self.current_image
        pixmap = pixmap.scaled( new_size, aspect_mode, transform_mode )

        self.setPixmap( pixmap )

    def apply_focus ( self ):
        if self.focus_value == 100:
            return

        current_size = self.original_image.rect().size()
        width, height = current_size.toTuple()

        x_value = self.focus_value / 100 * width
        y_value = self.focus_value / 100 * height

        offset_adjust = self.FOCUS_ADJUST.get( self.focus_area, "Center" )
        offset_left = x_value * offset_adjust[ 0 ]
        offset_top = y_value * offset_adjust[ 1 ]
        offset_right = width - x_value * offset_adjust[ 2 ]
        offset_bottom = height - y_value * offset_adjust[ 3 ]

        working_image = ImageQt.fromqpixmap( self.original_image )
        working_image = working_image.crop( ( offset_left, offset_top, offset_right, offset_bottom ) )
        working_image = QtGui.QPixmap.fromImage( ImageQt.ImageQt( working_image ) )

        self.current_image = working_image
        self.resize_pixmap()

class ImageEditorDialog ( QtWidgets.QDialog ):

    # default focus areas
    FOCUS_AREAS = [
        "Center",
        "Top",
        "Bottom",
        "Left",
        "Right",
        "Top-Left",
        "Top-Right",
        "Bottom-Left",
        "Bottom-Right"
    ]

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()
        self.resize( QtCore.QSize( 640, 480 ) )
        self.setSizePolicy( QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum )

    def create_widgets ( self ):
        # Main widget layout
        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout( main_layout )

        # Working image
        main_image = EditingImage()
        main_image.setSizePolicy( QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding )
        main_image.setMinimumSize( QtCore.QSize( 300, 300 ) )
        main_image.setAlignment( QtCore.Qt.AlignmentFlag.AlignCenter )
        main_layout.addWidget( main_image, 3 )
        self.main_image = main_image

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
        select_focus.addItems( self.FOCUS_AREAS )
        select_focus.currentIndexChanged.connect( self.set_focus_area )
        preferences_layout.addRow( "Focus Area", select_focus )
        self.select_focus = select_focus

        input_focus = QtWidgets.QSpinBox( suffix="%", minimum=0, maximum=100 )
        input_focus.valueChanged.connect( self.set_focus_value )
        preferences_layout.addRow( "Focus Value", input_focus )

        # Buttons actions
        button_layout = QtWidgets.QHBoxLayout()
        group_button = QtWidgets.QGroupBox()
        group_button.setLayout( button_layout )
        group_button.setSizePolicy( QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum )
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
        self.main_image.focus_area = self.select_focus.currentText()
        self.main_image.apply_focus()

    def set_focus_value ( self, value ):
        self.main_image.focus_value = value
        self.main_image.apply_focus()

    def set_working_image ( self ):
        file_path = QtWidgets.QFileDialog.getOpenFileName( self, "Choose Image", filter="*.jpg;;*.png" )[ 0 ]
        image_pixmap = QtGui.QPixmap( file_path )
        self.main_image.change_pixmap( image_pixmap )

    def set_image_changes ( self ):
        print( "Image Changes" )
