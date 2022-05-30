from PySide6 import QtCore, QtGui, QtWidgets
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageQt import ImageQt
from scripts.card import Card

class CardPreview ( QtWidgets.QLabel ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.preview_image = Image.open( "./assets/images/card_front_normal.png" )

    def resizeEvent ( self, event: QtGui.QResizeEvent ):
        if self.preview_image:
            self.resize_preview_pixmap()
        return super().resizeEvent( event )

    def create_preview_image ( self, card ):
        self.card_target = card
        self.render_preview_artwork()
        self.render_preview_title()
        self.render_preview_attribute()

        if card.type in ["spell", "trap", "equip", "ritual"]:
            properties = ["artwork", "title", "attribute"]
            front_type = card.type if card.type != "equip" else "spell"
            card_preview = Image.open( f"./assets/images/card_front_{front_type}.png" ).convert( "RGBA" )
        else:
            properties = ["artwork", "title", "attack", "defense", "level", "attribute"]
            card_preview = Image.open( "./assets/images/card_front_normal.png" ).convert( "RGBA" )
            self.render_preview_level()
            self.render_preview_power()

        for prop in properties:
            property_position = ( getattr( Card, f"layout_{prop}_X" ), getattr( Card, f"layout_{prop}_Y" ) )
            property_image = getattr( self, f"preview_{prop}_image" )

            if prop == "level":
                property_position = ( property_position[0] - ( card.level - 1 ) * 8 - ( card.level - 1 ), property_position[1] )

            card_preview.paste( property_image, property_position, property_image )

        self.preview_image = card_preview
        self.setPixmap( QtGui.QPixmap.fromImage( ImageQt( self.preview_image ) ) )
        self.resize_preview_pixmap()

    def resize_preview_pixmap ( self ):
        original_image = self.preview_image
        request_size = self.size()
        aspect_mode = QtCore.Qt.AspectRatioMode.KeepAspectRatio
        transform_mode = QtCore.Qt.TransformationMode.FastTransformation
        resized_pixmap = QtGui.QPixmap.fromImage( ImageQt( original_image ) )
        resized_pixmap = resized_pixmap.scaled( request_size, aspect_mode, transform_mode )

        self.setPixmap( resized_pixmap )

    def render_preview_artwork ( self ):
        card = self.card_target
        self.preview_artwork_image = card.artwork_image.convert( "RGBA" )

    def render_preview_title ( self ):
        card = self.card_target
        title_font = ImageFont.truetype( "./assets/fonts/card_title_bold.ttf", 12 )
        title_size = title_font.getsize( card.name )

        if title_size[0] > 96:
            title_image = Image.new( "RGBA", (title_size[0] + 2, 14), 0 )
            resize_needed = True
        else:
            title_image = Image.new( "RGBA", (96, 14), 0 )
            resize_needed = False

        title_draw = ImageDraw.Draw( title_image, "RGBA" )
        title_draw.text( (2, -2), card.name, (48, 48, 48, 255), title_font )
        title_image = title_image if not resize_needed else title_image.resize( (96, 14), Image.LANCZOS )

        self.preview_title_image = title_image

    def render_preview_attribute ( self ):
        card = self.card_target
        attribute_image = Image.open( f"./assets/images/card_attribute_{card.attribute}.png" )
        self.preview_attribute_image = attribute_image

    def render_preview_level ( self ):
        card = self.card_target
        star_image = Image.open( "./assets/images/card_star.png" )
        level_image = Image.new( "RGBA", ( star_image.width * card.level + card.level - 1, star_image.height ), 0 )

        for index in range( card.level ):
            level_image.paste( star_image, ( index + index * star_image.width, 0 ) )

        self.preview_level_image = level_image

    def render_preview_power ( self ):
        card = self.card_target
        power_font = ImageFont.truetype( "./assets/fonts/card_power.ttf", 12 )

        attack_image_size = power_font.getsize( f"{card.attack:03d}" )
        attack_image = Image.new( "RGBA", attack_image_size, 0 )
        draw_attack = ImageDraw.Draw( attack_image )
        draw_attack.text( (0, 0), str( card.attack ), fill=(0, 0, 0, 255), font=power_font )

        defense_image_size = power_font.getsize( f"{card.defense:03d}" )
        defense_image = Image.new( "RGBA", defense_image_size, 0 )
        draw_defense = ImageDraw.Draw( defense_image )
        draw_defense.text( (0, 0), str( card.defense ), fill=(0, 0, 0, 255), font=power_font )

        if attack_image_size[0] > 24 or attack_image_size[1] > 10:
            attack_image = attack_image.resize( (24, 10), Image.LANCZOS )

        if defense_image_size[0] > 24 or attack_image_size[1] > 10:
            defense_image = defense_image.resize( (24, 10), Image.LANCZOS )

        self.preview_attack_image = attack_image
        self.preview_defense_image = defense_image

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
