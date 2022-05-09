import time
from scripts.card import LIBRARY, Card

def timer ( func ):
    def wrapper ():
        start_time = time.time()
        func()
        stop_time = time.time()
        print( f"Finished in {stop_time - start_time:.2f}s")

    return wrapper

@timer
def main ():
    sl_path = r"C:\Users\luizd\Documents\PSX Games\Yu-Gi-Oh! Forbidden Memories (USA)\Modified\SLUS_014.11"
    wa_path = r"C:\Users\luizd\Documents\PSX Games\Yu-Gi-Oh! Forbidden Memories (USA)\Modified\WA_MRG.MRG"

    Card.load_library( sl_path, wa_path )
    Card.save_library( sl_path, wa_path )

if __name__ == "__main__":
    main()
