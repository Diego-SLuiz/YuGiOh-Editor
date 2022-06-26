from PySide6 import QtWidgets, QtCore, QtGui
from PIL import ImageQt, ImageEnhance

class EditingImage ( QtWidgets.QLabel ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.original_image = None
        self.current_image = None
        self.focus_value = 0
        self.x_adjust = 50
        self.y_adjust = 50
        self.color_value = 100
        self.contrast_value = 100
        self.sharpen_value = 100
        self.bright_value = 100

    def resizeEvent ( self, event ):
        self.resize_image()
        super().resizeEvent( event )

    def change_image ( self, new_image ):
        self.original_image = new_image
        self.update_image()

    def update_image ( self ):
        if not self.original_image:
            return

        self.apply_focus()
        self.apply_enhancements()
        self.resize_image()

    def resize_image ( self ):
        if not self.current_image:
            return

        transform_mode = QtCore.Qt.TransformationMode.SmoothTransformation
        aspect_mode = QtCore.Qt.AspectRatioMode.KeepAspectRatio

        original_size = self.original_image.size()
        requested_size = self.size()

        if requested_size.width() > original_size.width() * 3:
            requested_size.setWidth( original_size.width() * 3 )

        if requested_size.height() > original_size.height() * 3:
            requested_size.setHeight( original_size.height() * 3 )

        resized_image = self.current_image.scaled( requested_size, aspect_mode, transform_mode )
        self.setPixmap( QtGui.QPixmap.fromImage( resized_image ) )

    def apply_focus ( self ):
        width, height = self.original_image.rect().size().toTuple()
        x_value = self.focus_value / 100 * width
        y_value = self.focus_value / 100 * height
        left = self.x_adjust / 100 * x_value
        top = self.y_adjust / 100 * y_value
        right = ( width - ( 1 - self.x_adjust / 100 ) * x_value ) - left
        bottom = ( height - ( 1 - self.y_adjust / 100 ) * y_value ) - top

        self.current_image = self.original_image.copy( left, top, right, bottom )

    def apply_enhancements ( self ):
        working_image = ImageQt.fromqimage( self.current_image )

        color_enhancer = ImageEnhance.Color( working_image )
        working_image = color_enhancer.enhance( self.color_value / 100 )

        bright_enhance = ImageEnhance.Brightness( working_image )
        working_image = bright_enhance.enhance( self.bright_value / 100 )

        contrast_enhance = ImageEnhance.Contrast( working_image )
        working_image = contrast_enhance.enhance( self.contrast_value / 100 )

        sharpen_enhance = ImageEnhance.Sharpness( working_image )
        working_image = sharpen_enhance.enhance( self.sharpen_value / 100 )

        self.current_image = ImageQt.ImageQt( working_image )

class ImageEditorDialog ( QtWidgets.QDialog ):

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

        input_focus = QtWidgets.QSpinBox( suffix="%", minimum=0, maximum=100, value=0, singleStep=1 )
        input_focus.valueChanged.connect( self.set_focus_value )
        preferences_layout.addRow( "Focus Value", input_focus )

        slider_adjust_x = QtWidgets.QSlider( minimum=0, maximum=100, value=50, singleStep=1 )
        slider_adjust_x.setOrientation( QtCore.Qt.Orientation.Horizontal )
        slider_adjust_x.valueChanged.connect( self.set_adjust_x )
        preferences_layout.addRow( "X Adjust", slider_adjust_x )

        slider_adjust_y = QtWidgets.QSlider( minimum=0, maximum=100, value=50, singleStep=1 )
        slider_adjust_y.setOrientation( QtCore.Qt.Orientation.Horizontal )
        slider_adjust_y.valueChanged.connect( self.set_adjust_y )
        preferences_layout.addRow( "Y Adjust", slider_adjust_y )

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
        self.main_image.update_image()

    def set_enhance_contrast ( self, contrast_value ):
        self.main_image.contrast_value = contrast_value
        self.main_image.update_image()

    def set_enhance_brightness ( self, bright_value ):
        self.main_image.bright_value = bright_value
        self.main_image.update_image()

    def set_enhance_sharpness ( self, sharpen_value ):
        self.main_image.sharpen_value = sharpen_value
        self.main_image.update_image()

    def set_compress_width ( self ):
        print( "Compress Width" )

    def set_compress_height ( self ):
        print( "Compress Height" )

    def set_compress_colors ( self ):
        print( "Compress Colors" )

    def set_focus_value ( self, focus_value ):
        self.main_image.focus_value = focus_value
        self.main_image.update_image()

    def set_adjust_x ( self, adjust_value ):
        self.main_image.x_adjust = adjust_value
        self.main_image.update_image()

    def set_adjust_y ( self, adjust_value ):
        self.main_image.y_adjust = adjust_value
        self.main_image.update_image()

    def set_working_image ( self ):
        file_path = QtWidgets.QFileDialog.getOpenFileName( self, "Choose Image", filter="*.jpg;;*.png" )[ 0 ]

        if file_path:
            image = QtGui.QImage( file_path )
            self.main_image.change_image( image )

    def set_image_changes ( self ):
        print( "Image Changes" )
