from ..connectionManager import ConnectionManager
import logging
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Optional, Union
import zlib


class Text:
    """Manages text processing and packet creation for iDotMatrix devices. With help from https://github.com/8none1/idotmatrix/ :)"""

    logging = logging.getLogger(__name__)
    # must be 16x32 or 8x16
    image_width = 16
    image_height = 32
    # must be x05 for 16x32 or x02 for 8x16
    separator = b"\x05\xff\xff\xff"

    def __init__(self) -> None:
        self.conn: ConnectionManager = ConnectionManager()

    async def setMode(
        self,
        text: str,
        font_size: int = 16,
        font_path: Optional[str] = None,
        text_mode: int = 1,
        speed: int = 95,
        text_color_mode: int = 1,
        text_color: Tuple[int, int, int] = (255, 0, 0),
        text_bg_mode: int = 0,
        text_bg_color: Tuple[int, int, int] = (0, 255, 0),
    ) -> Union[bool, bytearray]:
        try:
            data = self._buildStringPacket(
                text_mode=text_mode,
                speed=speed,
                text_color_mode=text_color_mode,
                text_color=text_color,
                text_bg_mode=text_bg_mode,
                text_bg_color=text_bg_color,
                text_bitmaps=self._StringToBitmaps(
                    text=text,
                    font_size=font_size,
                    font_path=font_path,
                ),
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except BaseException as error:
            self.logging.error(f"could send the text to the device: {error}")
            return False

    def _buildStringPacket(
        self,
        text_bitmaps: bytearray,
        text_mode: int = 1,
        speed: int = 95,
        text_color_mode: int = 1,
        text_color: Tuple[int, int, int] = (255, 0, 0),
        text_bg_mode: int = 0,
        text_bg_color: Tuple[int, int, int] = (0, 255, 0),
    ) -> bytearray:
        """Constructs a packet with the settings and bitmaps for iDotMatrix devices.

        Args:
            text_bitmaps (bytearray): bitmap list of the text characters
            text_mode (int, optional): Text mode. Defaults to 0. 0 = replace text, 1 = marquee, 2 = reversed marquee, 3 = vertical rising marquee, 4 = vertical lowering marquee, 5 = blinking, 6 = fading, 7 = tetris, 8 = filling
            speed (int, optional): Speed of Text. Defaults to 95.
            text_color_mode (int, optional): Text Color Mode. Defaults to 1. 0 = white, 1 = use given RGB color, 2,3,4,5 = rainbow modes
            text_color (Tuple[int, int, int], optional): Text RGB Color. Defaults to (255, 0, 0).
            text_bg_mode (int, optional): Text Background Mode. Defaults to 0. 0 = black, 1 = use given RGB color
            text_bg_color (Tuple[int, int, int], optional): Background RGB Color. Defaults to (0, 0, 0).

        Returns:
            bytearray: _description_
        """
        num_chars = text_bitmaps.count(self.separator)

        text_metadata = bytearray(
            [
                0,
                0,  # Placeholder for num_chars, to be set below
                0,
                1,  # Static values
                text_mode,
                speed,
                text_color_mode,
                *text_color,
                text_bg_mode,
                *text_bg_color,
            ]
        )
        text_metadata[:2] = num_chars.to_bytes(2, byteorder="little")

        packet = text_metadata + text_bitmaps

        header = bytearray(
            [
                0,
                0,  # total_len placeholder
                3,
                0,
                0,  # Static header values
                0,
                0,
                0,
                0,  # Placeholder for packet length
                0,
                0,
                0,
                0,  # Placeholder for CRC
                0,
                0,
                12,  # Static footer values
            ]
        )
        total_len = len(packet) + len(header)
        header[:2] = total_len.to_bytes(2, byteorder="little")
        header[5:9] = len(packet).to_bytes(4, byteorder="little")
        header[9:13] = zlib.crc32(packet).to_bytes(4, byteorder="little")

        return header + packet

    def _StringToBitmaps(
        self, text: str, font_path: Optional[str] = None, font_size: Optional[int] = 20
    ) -> bytearray:
        """Converts text to bitmap images suitable for iDotMatrix devices."""
        if not font_path:
            # using open source font from https://www.fontspace.com/rain-font-f22577
            font_path = "./fonts/Rain-DRM3.otf"
        font = ImageFont.truetype(font_path, font_size)
        byte_stream = bytearray()
        for char in text:
            # todo make image the correct size for 16x16, 32x32 and 64x64
            image = Image.new("1", (self.image_width, self.image_height), 0)
            draw = ImageDraw.Draw(image)
            _, _, text_width, text_height = draw.textbbox((0, 0), text=char, font=font)
            text_x = (self.image_width - text_width) // 2
            text_y = (self.image_height - text_height) // 2
            draw.text((text_x, text_y), char, fill=1, font=font)
            bitmap = bytearray()
            for y in range(self.image_height):
                for x in range(self.image_width):
                    if x % 8 == 0:
                        byte = 0
                    pixel = image.getpixel((x, y))
                    byte |= (pixel & 1) << (x % 8)
                    if x % 8 == 7 or x == self.image_width - 1:
                        bitmap.append(byte)
            byte_stream.extend(self.separator + bitmap)
        return byte_stream
