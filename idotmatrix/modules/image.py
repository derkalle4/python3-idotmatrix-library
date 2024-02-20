from typing import Union, List
from ..connectionManager import ConnectionManager
import io
import logging
from PIL import Image as PilImage
import struct


class Image:
    logging = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.conn: ConnectionManager = ConnectionManager()

    async def setMode(self, mode: int = 1) -> Union[bool, bytearray]:
        """Enter the DIY draw mode of the iDotMatrix device.

        Args:
            mode (int): 0 = disable DIY, 1 = enable DIY, 2 = ?, 3 = ?. Defaults to 1.

        Returns:
            Union[bool, bytearray]: False if there's an error, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            data = bytearray([5, 0, 4, 1, mode % 256])
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except BaseException as error:
            self.logging.error(f"could not enter image mode due to {error}")
            return False

    def _loadPNG(self, file_path: str) -> bytes:
        """Load a PNG file into a byte buffer.

        Args:
            file_path (str): path to file

        Returns:
            bytes: returns the file contents
        """
        with open(file_path, "rb") as file:
            return file.read()

    def _splitIntoChunks(self, data: bytearray, chunk_size: int) -> List[bytearray]:
        """Split the data into chunks of specified size.

        Args:
            data (bytearray): data to split into chunks
            chunk_size (int): size of the chunks

        Returns:
            List[bytearray]: returns list with chunks of given data input
        """
        return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]

    def _createPayloads(self, png_data: bytearray) -> bytearray:
        """Creates payloads from a PNG file.

        Args:
            png_data (bytearray): data of the png file

        Returns:
            bytearray: returns bytearray payload
        """
        png_chunks = self._splitIntoChunks(png_data, 4096)
        idk = len(png_data) + len(png_chunks)
        idk_bytes = struct.pack("h", idk)  # Convert to 16-bit signed int
        png_len_bytes = struct.pack("i", len(png_data))
        payloads = bytearray()
        for i, chunk in enumerate(png_chunks):
            payload = (
                idk_bytes + bytearray([0, 0, 2 if i > 0 else 0]) + png_len_bytes + chunk
            )
            payloads.extend(payload)
        return payloads

    async def uploadUnprocessed(self, file_path: str) -> Union[bool, bytearray]:
        """Uploads an image without further checks and resizes.

        Args:
            file_path (str): path to the image file

        Returns:
            Union[bool, bytearray]: False if there's an error, otherwise returns bytearray payload
        """
        try:
            png_data = self._loadPNG(file_path)
            data = self._createPayloads(png_data)
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except BaseException as error:
            self.logging.error(f"could not upload the unprocessed image: {error}")
            return False

    async def uploadProcessed(
        self, file_path: str, pixel_size: int = 32
    ) -> Union[bool, bytearray]:
        """Uploads a file processed and makes sure everything is correct before uploading to the device.

        Args:
            file_path (str): path to the image file
            pixel_size (int, optional): amount of pixels (either 16 or 32 makes sense). Defaults to 32.

        Returns:
            Union[bool, bytearray]: False if there's an error, otherwise returns bytearray payload
        """
        try:
            with PilImage.open(file_path) as img:
                if img.size != (pixel_size, pixel_size):
                    img = img.resize(
                        (pixel_size, pixel_size), PilImage.LANCZOS
                    )
                png_buffer = io.BytesIO()
                img.save(png_buffer, format="PNG")
                png_buffer.seek(0)
                data = self._createPayloads(png_buffer.getvalue())
                if self.conn:
                    await self.conn.connect()
                    await self.conn.send(data=data)
                return data
        except BaseException as error:
            self.logging.error(f"could not upload processed image: {error}")
            return False
