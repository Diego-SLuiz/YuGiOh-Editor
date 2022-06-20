from PySide6 import QtWidgets, QtCore, QtGui
from PIL import ImageQt, ImageEnhance

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
        self.original_pixmap = None
        self.focus_area = "Center"
        self.focus_value = 0
        self.color_value = 100
        self.bright_value = 100
        self.sharpen_value = 100
        self.contrast_value = 100

    def resizeEvent ( self, event ):
        self.update_pixmap()
        super().resizeEvent( event )

    def change_pixmap ( self, new_pixmap ):
        self.original_pixmap = new_pixmap
        self.update_pixmap()

    def update_pixmap ( self ):
        if not self.original_pixmap:
            return

        self.apply_focus()
        self.apply_enhancements()
        self.resize_pixmap()

    def apply_focus ( self ):
        if self.focus_value == 100:
            return

        width, height = self.original_pixmap.rect().size().toTuple()

        x_value = self.focus_value / 100 * width
        y_value = self.focus_value / 100 * height

        offset_adjust = self.FOCUS_ADJUST.get( self.focus_area, "Center" )
        offset_left = x_value * offset_adjust[ 0 ]
        offset_top = y_value * offset_adjust[ 1 ]
        offset_right = width - x_value * offset_adjust[ 2 ]
        offset_bottom = height - y_value * offset_adjust[ 3 ]

        working_image = ImageQt.fromqpixmap( self.original_pixmap )
        working_image = working_image.crop( ( offset_left, offset_top, offset_right, offset_bottom ) )

        working_pixmap = QtGui.QPixmap.fromImage( ImageQt.ImageQt( working_image ) )
        self.current_pixmap = working_pixmap

    def apply_enhancements ( self ):
        working_image = ImageQt.fromqpixmap( self.current_pixmap )

        color_enhancer = ImageEnhance.Color( working_image )
        working_image = color_enhancer.enhance( self.color_value / 100 )

        bright_enhance = ImageEnhance.Brightness( working_image )
        working_image = bright_enhance.enhance( self.bright_value / 100 )

        contrast_enhance = ImageEnhance.Contrast( working_image )
        working_image = contrast_enhance.enhance( self.contrast_value / 100 )

        sharpen_enhance = ImageEnhance.Sharpness( working_image )
        working_image = sharpen_enhance.enhance( self.sharpen_value / 100 )

        working_pixmap = QtGui.QPixmap.fromImage( ImageQt.ImageQt( working_image ) )
        self.current_pixmap = working_pixmap

    def resize_pixmap ( self ):
        transform_mode = QtCore.Qt.TransformationMode.SmoothTransformation
        aspect_mode = QtCore.Qt.AspectRatioMode.KeepAspectRatio

        working_pixmap = self.current_pixmap
        working_pixmap = working_pixmap.scaled( self.size(), aspect_mode, transform_mode )
        self.setPixmap( working_pixmap )

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

        enhance_color = QtWidgets.QSpinBox( suffix="%", minimum=0, maximum=200, singleStep=5, value=100 )
        enhance_color.valueChanged.connect( self.set_enhance_color )
        enhance_layout.addRow( "Color", enhance_color )

        enhance_contrast = QtWidgets.QSpinBox( suffix="%", minimum=0, maximum=200, singleStep=5, value=100 )
        enhance_contrast.valueChanged.connect( self.set_enhance_contrast )
        enhance_layout.addRow( "Contrast", enhance_contrast )

        enhance_brightness = QtWidgets.QSpinBox( suffix="%", minimum=0, maximum=200, singleStep=5, value=100 )
        enhance_brightness.valueChanged.connect( self.set_enhance_brightness )
        enhance_layout.addRow( "Brightness", enhance_brightness )

        enhance_sharpness = QtWidgets.QSpinBox( suffix="%", minimum=0, maximum=200, singleStep=5, value=100 )
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
        select_focus.currentTextChanged.connect( self.set_focus_area )
        preferences_layout.addRow( "Focus Area", select_focus )

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

    def set_enhance_color ( self, color_value ):
        self.main_image.color_value = color_value
        self.main_image.update_pixmap()

    def set_enhance_contrast ( self, contrast_value ):
        self.main_image.contrast_value = contrast_value
        self.main_image.update_pixmap()

    def set_enhance_brightness ( self, bright_value ):
        self.main_image.bright_value = bright_value
        self.main_image.update_pixmap()

    def set_enhance_sharpness ( self, sharpen_value ):
        self.main_image.sharpen_value = sharpen_value
        self.main_image.update_pixmap()

    def set_compress_width ( self ):
        print( "Compress Width" )

    def set_compress_height ( self ):
        print( "Compress Height" )

    def set_compress_colors ( self ):
        print( "Compress Colors" )

    def set_focus_area ( self, focus_area ):
        self.main_image.focus_area = focus_area
        self.main_image.update_pixmap()

    def set_focus_value ( self, focus_value ):
        self.main_image.focus_value = focus_value
        self.main_image.update_pixmap()

    def set_working_image ( self ):
        file_path = QtWidgets.QFileDialog.getOpenFileName( self, "Choose Image", filter="*.jpg;;*.png" )[ 0 ]

        if file_path:
            image_pixmap = QtGui.QPixmap( file_path )
            self.main_image.change_pixmap( image_pixmap )

    def set_image_changes ( self ):
        print( "Image Changes" )
