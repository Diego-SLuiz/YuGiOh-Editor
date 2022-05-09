import re
import mmap
import textwrap
import numpy as np

from PIL import Image, ImageFont, ImageDraw
from .references import *

NAME_LENGTH_LIMIT = 36
INFO_LENGTH_LIMIT = 140
NAME_BLOCK_LIMIT = 0x27D0
INFO_BLOCK_LIMIT = 0xFFFA

CARD_ADDRESS = {
    "layout": {
        "artwork_X": 0x00019434,
        "artwork_Y": 0x0001944C,
        "name_X": 0x000194C8,
        "name_Y": 0x000194FC,
        "attack_X": 0x000196B0,
        "attack_Y": 0x000196C4,
        "defense_X": 0x0001973C,
        "defense_Y": 0x00019750,
        "level_X": 0x000197CC,
        "level_Y": 0x000197F0,
        "attribute_X": 0x00019884,
        "attribute_Y": 0x00019898,
    },

    "data": {
        "data_1": 0x001C4A44,
        "data_2": 0x001C5B33,
        "data_3": 0x00FB9808,
    },

    "image": {
        "title": 0x0016B840,
        "artwork": 0x00169000,
        "miniature_1": 0x0016BAE0,
        "miniature_2": 0x00000000,
    },

    "text": {
        "name_pointer": 0x001C6002,
        "info_pointer": 0x001B0A02,
        "name_block": 0x001C6801,
        "info_block": 0x001B11F5,
    },

    "compatibility": {
        "fusion_pointer": 0x00B87802,
        "fusion_block": 0x00B87DA6,
        "ritual_block": 0x00B97800,
        "equip_block": 0x00B85000,
    }
}

LIBRARY = []

class Card:

    SL_FILE = None
    WA_FILE = None

    def __init__ ( self, number ):
        self.number = number
        self.get_data()
        self.get_artwork()
        self.get_miniature()
        LIBRARY.append( self )

    def __repr__ ( self ) -> str:
        return \
            f"Name        : {self.name}\n" \
            f"Info        : {self.info}\n" \
            f"Type        : {self.type}\n" \
            f"Attribute   : {self.attribute}\n" \
            f"Guardian I  : {self.guardian_1}\n" \
            f"Guardian II : {self.guardian_2}\n" \
            f"Level       : {self.level}\n" \
            f"Attack      : {self.attack}\n" \
            f"Defense     : {self.defense}\n" \
            f"Price       : {self.price}\n" \
            f"Password    : {self.password}\n" \

    @staticmethod
    def decode_text ( code: bytes ) -> str:
        table = { value: key for key, value in CHARACTERS.items() }
        tokens = { 0x0A: [ "{", "}" ], 0x0B: [ "[", "]" ] }
        result = ""
        index = 0

        def decode_token ():
            nonlocal index

            token_value = format( code[index + 2], "02X" )
            token_text = tokens[code[index + 1]][0] + token_value + tokens[code[index + 1]][1]
            index += 2
            return token_text

        while index < len( code ):
            result += table.get( code[index] ) or decode_token()
            index += 1

        return result

    @staticmethod
    def encode_text ( text: str ) -> bytes:
        table = { key: bytes( [value] ) for key, value in CHARACTERS.items() }
        tokens = { "{": 0x0A, "[": 0x0B }
        result = b""
        index = 0

        def encode_token ():
            nonlocal index

            token_value = int( text[index + 1: index + 3], 16 )
            token_bytes = bytes( [ 0xF8, tokens[text[index]], token_value ] )
            index += 3
            return token_bytes

        while index < len( text ):
            result += table.get( text[index] ) or encode_token()
            index += 1

        return result

    @classmethod
    def load_library ( cls, sl_path, wa_path ):
        with open( sl_path, "r+b" ) as sl_file, open( wa_path, "r+b" ) as wa_file, \
            mmap.mmap( sl_file.fileno(), 0 ) as sl_map, mmap.mmap( wa_file.fileno(), 0 ) as wa_map:

            cls.SL_FILE = sl_map
            cls.WA_FILE = wa_map

            for i in range(722):
                Card(i)

            cls.get_names()
            cls.get_infos()

            for card in LIBRARY:
                card.get_title()

    @classmethod
    def save_library ( cls, sl_path, wa_path ):
        with open( sl_path, "r+b" ) as sl_file, open( wa_path, "r+b" ) as wa_file, \
            mmap.mmap( sl_file.fileno(), 0 ) as sl_map, mmap.mmap( wa_file.fileno(), 0 ) as wa_map:

            cls.SL_FILE = sl_map
            cls.WA_FILE = wa_map

            for card in LIBRARY:
                card.set_data()
                card.set_title()
                card.set_artwork()
                card.set_miniature()

            cls.set_names()
            cls.set_infos()

    @classmethod
    def get_names ( cls ):
        cls.SL_FILE.seek( CARD_ADDRESS["text"]["name_pointer"] )
        address_array = np.frombuffer( cls.SL_FILE.read( 0x05A4 ), "uint16" ) + 0x1C0800

        for number, address in enumerate( address_array ):
            cls.SL_FILE.seek( address )

            name_bytes = cls.SL_FILE.read( 0x24 )
            name_bytes = name_bytes[:name_bytes.find( 0xFF )]
            name = cls.decode_text( name_bytes )

            LIBRARY[number].name = name

    @classmethod
    def set_names ( cls ):
        names_block_address = CARD_ADDRESS["text"]["name_block"]
        names_pointer_address = CARD_ADDRESS["text"]["name_pointer"]
        address_limit = 0x1C92CD # Beginning of other texts
        address_adjust = 0x01C997F # Cave code at end of file

        for card in LIBRARY:
            name_bytes = cls.encode_text( card.name + "|" )
            jump_condition = names_block_address + len( name_bytes ) > address_limit and names_block_address < address_adjust
            names_block_address = address_adjust if jump_condition else names_block_address

            cls.SL_FILE.seek( names_block_address )
            cls.SL_FILE.write( name_bytes )

            cls.SL_FILE.seek( names_pointer_address )
            cls.SL_FILE.write( ( names_block_address - 0x1C0800 ).to_bytes( 0x02, "little" ) )

            names_block_address += len( name_bytes )
            names_pointer_address += 0x02

    @classmethod
    def get_infos ( cls ):
        cls.SL_FILE.seek( CARD_ADDRESS["text"]["info_pointer"] )
        address_array = np.frombuffer( cls.SL_FILE.read( 0x05A4 ), "uint16" ) + 0x1B0800

        for number, address in enumerate( address_array ):
            cls.SL_FILE.seek( address )

            info_bytes = cls.SL_FILE.read( 0x8C )
            info_bytes = info_bytes[:info_bytes.find( 0xFF )]
            info = cls.decode_text( info_bytes )
            info = re.sub( " +", " ", info.replace( "_", " " ) )

            LIBRARY[number].info = info

    @classmethod
    def set_infos ( cls ):
        infos_block_address = CARD_ADDRESS["text"]["info_block"]
        infos_pointer_address = CARD_ADDRESS["text"]["info_pointer"]

        def wrap_text ( text ):
            result = re.sub( "\{..\}|\[..\]", "", text )
            result = "_".join( textwrap.wrap( result, 20) )

            for token in re.findall( "\{..\}|\[..\]", text ):
                index = text.find( token )
                result = result[:index] + token + result[index:]

            return result

        for card in LIBRARY:
            info_bytes = cls.encode_text( wrap_text( card.info + "|" ) )

            cls.SL_FILE.seek( infos_block_address )
            cls.SL_FILE.write( info_bytes )

            cls.SL_FILE.seek( infos_pointer_address )
            cls.SL_FILE.write( ( infos_block_address - 0x1B0800 ).to_bytes( 0x02, "little" ) )

            infos_block_address += len( info_bytes )
            infos_pointer_address += 0x02

    def get_data ( self ):
        types_table = dict( enumerate( TYPES ) )
        attributes_table = dict( enumerate( ATTRIBUTES ) )
        guardians_table = dict( enumerate( GUARDIANS ) )

        # Type, Guardians, Power
        self.SL_FILE.seek( CARD_ADDRESS["data"]["data_1"] + self.number * 0x04 )
        data_1 = int.from_bytes( self.SL_FILE.read( 0x04 ), "little" )

        self.type, data_1 = divmod( data_1, 0x4000000 )
        self.type = types_table[self.type]
        self.guardian_1, data_1 = divmod( data_1, 0x400000 )
        self.guardian_1 = guardians_table[self.guardian_1]
        self.guardian_2, data_1 = divmod( data_1, 0x40000 )
        self.guardian_2 = guardians_table[self.guardian_2]
        self.defense, data_1 = divmod( data_1, 0x200 )
        self.defense *= 10
        self.attack = data_1 * 10

        # Attribute, Level
        self.SL_FILE.seek( CARD_ADDRESS["data"]["data_2"] + self.number * 0x01 )
        data_2 = int.from_bytes( self.SL_FILE.read( 0x01 ), "little" )

        self.attribute, data_2 = divmod( data_2, 0x10 )
        self.attribute = attributes_table[self.attribute]
        self.level = data_2

        # Price, Password
        self.WA_FILE.seek( CARD_ADDRESS["data"]["data_3"] + self.number * 0x08 )

        self.price = int.from_bytes( self.WA_FILE.read( 0x04 ), "little" )
        self.password = format( int.from_bytes( self.WA_FILE.read( 0x04 ), "little" ), "08X" )
        self.password = self.password if self.password.isnumeric() else "00000000"

    def set_data ( self ):
        types_table = { val: key for key, val in dict( enumerate( TYPES ) ).items() }
        attributes_table = { val: key for key, val in dict( enumerate( ATTRIBUTES ) ).items() }
        guardians_table = { val: key for key, val in dict( enumerate( GUARDIANS ) ).items() }

        # Type, Guardians, Power
        data_1 = 0
        data_1 += types_table[self.type] * 0x4000000
        data_1 += guardians_table[self.guardian_1] * 0x400000
        data_1 += guardians_table[self.guardian_2] * 0x40000
        data_1 += self.defense // 10 * 0x200
        data_1 += self.attack // 10

        self.SL_FILE.seek( CARD_ADDRESS["data"]["data_1"] + self.number * 0x04 )
        self.SL_FILE.write( data_1.to_bytes( 0x04, "little" ) )

        # Attribute, Level
        data_2 = 0
        data_2 += attributes_table[self.attribute] * 0x10
        data_2 += self.level

        self.SL_FILE.seek( CARD_ADDRESS["data"]["data_2"] + self.number * 0x01 )
        self.SL_FILE.write( data_2.to_bytes( 0x01, "little" ) )

        # Price, Password
        self.WA_FILE.seek( CARD_ADDRESS["data"]["data_3"] + self.number * 0x08 )

        self.WA_FILE.write( self.price.to_bytes( 0x04, "little" ) )
        self.WA_FILE.write( ( int( self.password, 16 ) or 0xFFFFFFFE ).to_bytes( 0x04, "little" ) )

    def get_title ( self ):
        font_path = r"C:\Users\luizd\Documents\GitHub\YuGiOh-Editor\assets\fonts\card_title.ttf"

        title_font = ImageFont.truetype( font_path, 12 )
        title_size = title_font.getsize( self.name )
        title_sheet = Image.new( "RGB", title_size, "black" )
        title_draw = ImageDraw.Draw( title_sheet, "RGB" )
        title_draw.text( (0, 0), self.name, "white", title_font )

        template = Image.new( "RGB", (96, 14), "black" )

        if title_sheet.width > 94:
            title_sheet = title_sheet.resize( (94, 14), Image.LANCZOS )

        template.paste( title_sheet, (2, -1))
        template = template.quantize( 16 )

        self.title_image = template

    def set_title ( self ):
        title_array = np.asarray( self.title_image, "uint8" ).ravel()
        title_array[title_array > 10] = 15 # reduce blur radius

        left_pixels = title_array[0::2]
        right_pixels = title_array[1::2] * 16
        pixels = left_pixels + right_pixels

        self.WA_FILE.seek( CARD_ADDRESS["image"]["title"] + self.number * 0x3800 )
        self.WA_FILE.write( pixels.tobytes() )

    def get_artwork ( self ):
        self.WA_FILE.seek( CARD_ADDRESS["image"]["artwork"] + self.number * 0x3800)

        artwork_bytes = np.frombuffer( self.WA_FILE.read( 0x2640 ), "uint8" ) # 102x96 image
        colors_bytes = np.frombuffer( self.WA_FILE.read( 0x0200 ), "uint16" ) # 256 colors

        red = colors_bytes % 1024 % 32 * 8
        green = colors_bytes % 1024 // 32 * 8
        blue = colors_bytes // 1024 * 8

        colors = np.array( [red, green, blue], "uint8" ).T
        pixels = colors[artwork_bytes].reshape( (96, 102, 3) )

        self.artwork_image = Image.fromarray( pixels, "RGB" )

    def set_artwork ( self ):
        artwork_data = np.asarray( self.artwork_image, "uint16" ).ravel()

        red = artwork_data[0::3] // 8
        green = artwork_data[1::3] // 8 * 32
        blue = artwork_data[2::3] // 8 * 1024

        artwork_data = red + green + blue

        colors_bytes = np.unique( artwork_data )
        artwork_bytes = np.searchsorted( colors_bytes, artwork_data ).astype( "uint8" )

        self.WA_FILE.seek( CARD_ADDRESS["image"]["artwork"] + self.number * 0x3800)
        self.WA_FILE.write( artwork_bytes.tobytes() )
        self.WA_FILE.write( colors_bytes.tobytes() )

    def get_miniature ( self ):
        self.WA_FILE.seek( CARD_ADDRESS["image"]["miniature_1"] + self.number * 0x3800)

        miniature_bytes = np.frombuffer( self.WA_FILE.read( 0x0500 ), "uint8" ) # 40x32 image
        colors_bytes = np.frombuffer( self.WA_FILE.read( 0x80 ), "uint16" ) # 64 colors

        red = colors_bytes % 1024 % 32 * 8
        green = colors_bytes % 1024 // 32 * 8
        blue = colors_bytes // 1024 * 8

        colors = np.array( [red, green, blue], "uint8" ).T
        pixels = colors[miniature_bytes].reshape( (32, 40, 3) )

        self.miniature_image = Image.fromarray( pixels, "RGB" )

    def set_miniature ( self ):
        miniature_data = np.asarray( self.miniature_image, "uint16" ).ravel()

        red = miniature_data[0::3] // 8
        green = miniature_data[1::3] // 8 * 32
        blue = miniature_data[2::3] // 8 * 1024

        miniature_data = red + green + blue

        colors_bytes = np.unique( miniature_data )
        miniature_bytes = np.searchsorted( colors_bytes, miniature_data ).astype( "uint8" )

        self.WA_FILE.seek( CARD_ADDRESS["image"]["miniature_1"] + self.number * 0x3800)
        self.WA_FILE.write( miniature_bytes.tobytes() )
        self.WA_FILE.write( colors_bytes.tobytes() )

        self.WA_FILE.seek( CARD_ADDRESS["image"]["miniature_2"] + self.number * 0x0800)
        self.WA_FILE.write( miniature_bytes.tobytes() )
        self.WA_FILE.write( colors_bytes.tobytes() )
