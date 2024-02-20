import asyncio
import time
from idotmatrix import ConnectionManager
from idotmatrix import Chronograph
from idotmatrix import Clock
from idotmatrix import Common
from idotmatrix import Countdown

# from idotmatrix import Eco
from idotmatrix import FullscreenColor
from idotmatrix import Gif
from idotmatrix import Graffiti
from idotmatrix import Image

# from idotmatrix import MusicSync
from idotmatrix import Scoreboard

# from idotmatrix import System
from idotmatrix import Text


async def main():
    # connect
    conn = ConnectionManager()
    await conn.connectBySearch()
    # chronograph
    test = Chronograph()
    await test.setMode(1)
    time.sleep(5)
    # clock
    test = Clock()
    await test.setMode(1)
    time.sleep(5)
    # Common
    test = Common()
    await test.flipScreen(True)
    time.sleep(5)
    await test.flipScreen(False)
    # Countdown
    test = Countdown()
    await test.setMode(1, 0, 5)
    time.sleep(5)
    # FullscreenColor
    test = FullscreenColor()
    await test.setMode(r=255, g=255, b=0)
    time.sleep(5)
    # show GIF
    test = Gif()
    await test.uploadProcessed(
        file_path="./images/demo.gif",
        pixel_size=32,
    )
    time.sleep(5)
    # Graffiti
    test = Graffiti()
    await test.setPixel(r=255, g=255, b=255, x=10, y=10)
    time.sleep(5)
    # Image
    test = Image()
    await test.uploadProcessed(
        file_path="./images/demo_512.png",
        pixel_size=32,
    )
    time.sleep(5)
    # Scoreboard
    test = Scoreboard()
    await test.setMode(10, 5)
    time.sleep(5)
    # Text
    test = Text()
    await test.setMode(
        "HELLO WORLD",
        font_path="./fonts/Rain-DRM3.otf",
    )
    time.sleep(5)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        quit()
