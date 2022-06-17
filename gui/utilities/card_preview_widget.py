from PySide6 import QtWidgets, QtCore, QtGui
from PIL.ImageQt import ImageQt
from PIL import Image, ImageFont, ImageDraw
from scripts.card.card_editor import Card

class CardPreviewWidget ( QtWidgets.QLabel ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.preview_image = Image.open( "./assets/images/card_front_normal.png" )
        self.setMinimumSize( QtCore.QSize( 140, 196 ) )
        self.setMaximumSize( QtCore.QSize( 280, 392 ) )

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
