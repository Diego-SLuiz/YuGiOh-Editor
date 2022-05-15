import mmap
import numpy as np

SL_FILE = None
WA_FILE = None

def open_files ( func ):
    def wrapper ( *args, **kwargs):
        sl_path = r"C:\Users\luizd\Documents\PSX Games\Yu-Gi-Oh! Forbidden Memories (USA)\Modified\SLUS_014.11"
        wa_path = r"C:\Users\luizd\Documents\PSX Games\Yu-Gi-Oh! Forbidden Memories (USA)\Modified\WA_MRG.MRG"

        global SL_FILE, WA_FILE

        with open( sl_path, "r+b" ) as sl_file, open( wa_path, "r+b" ) as wa_file, \
            mmap.mmap( sl_file.fileno(), 0 ) as sl_map, mmap.mmap( wa_file.fileno(), 0 ) as wa_map:
            SL_FILE, WA_FILE = sl_map, wa_map
            func(*args, **kwargs)

    return wrapper

@open_files
def decode_color_palette ( address, size ):
    WA_FILE.seek( address )

    colors_bytes = np.frombuffer( WA_FILE.read( size ), "uint16" )
    red = colors_bytes % 1024 % 32 * 8
    green = colors_bytes % 1024 // 32 * 8
    blue = colors_bytes // 1024 * 8
    colors = np.array( [red, green, blue], "uint8" ).T

    print( colors )

@open_files
def set_titles_palette ( palette ):
    field_address = 0x00B841C0 # normal forest umi wasteland yami sogen mountain
    menu_address = [0x00F079C0, 0x00FB89C0, 0x010E99C0] # build deck password library

    for index in range( 7 ):
        WA_FILE.seek( field_address + index * 0x75800 )
        WA_FILE.write( palette.tobytes() )

    for address in menu_address:
        WA_FILE.seek( address )
        WA_FILE.write( palette.tobytes() )

def linear_gradient ( start_color, stop_color, shades ):
    red_array = np.linspace( start_color[0], stop_color[0], shades - 1, dtype="uint16" )
    red_array = ( np.append( red_array, 0 ) // 8 ).astype( "uint16" )

    green_array = np.linspace( start_color[1], stop_color[1], shades - 1, dtype="uint16" )
    green_array = ( np.append( green_array, 0 ) // 8 * 32 ).astype( "uint16" )

    blue_array = np.linspace( start_color[2], stop_color[2], shades - 1, dtype="uint16" )
    blue_array = ( np.append( blue_array, 0 ) // 8 * 1024 ).astype( "uint16" )

    palette_array = red_array + green_array + blue_array

    return palette_array

if __name__ == "__main__":
    palette = linear_gradient( (64, 64, 64), (128, 128, 128), 16 )
    set_titles_palette( palette )
