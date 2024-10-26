from typing import Union, List
from ..connectionManager import ConnectionManager
import io
import logging
from PIL import Image as PilImage
import zlib


class Gif:
    logging = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.conn: ConnectionManager = ConnectionManager()

    def _load(self, file_path: str) -> bytes:
        """Load a gif file into a byte buffer.

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

    def _createPayloads(
        self, gif_data: bytearray, chunk_size: int = 4096
    ) -> List[bytearray]:
        """Creates payloads from a GIF file.

        Args:
            gif_data (bytearray): data of the gif file
            chunk_size (int): size of a chunk

        Returns:
            bytearray: returns bytearray payload
        """
        # chunk header
        header = bytearray(
            [
                255,
                255,
                1,
                0,
                0,
                255,
                255,
                255,
                255,
                255,
                255,
                255,
                255,
                5,
                0,
                13,
            ]
        )
        # split gif into chunks
        chunks = []
        gif_chunks = self._splitIntoChunks(gif_data, chunk_size)
        # set gif length
        header[5:9] = int(len(gif_data)).to_bytes(4, byteorder="little")
        # set crc of gif
        crc = zlib.crc32(gif_data)
        header[9:13] = crc.to_bytes(4, byteorder="little")
        # iterate over chunks
        for i, chunk in enumerate(gif_chunks):
            # starting from the second chunk, set the header to 2
            header[4] = 2 if i > 0 else 0
            # set chunk length in header
            chunk_len = len(chunk) + len(header)
            header[0:2] = chunk_len.to_bytes(2, byteorder="little")
            # append chunk to chunk list
            chunks.append(header + chunk)
        return chunks

    async def uploadUnprocessed(self, file_path: str) -> Union[bool, bytearray]:
        """uploads an image without further checks and resizes.

        Args:
            file_path (str): path to the image file

        Returns:
            Union[bool, bytearray]: False if there's an error, otherwise returns bytearray payload
        """
        try:
            gif_data = self._load(file_path)
            data = self._createPayloads(gif_data)
            if self.conn:
                await self.conn.connect()
                for chunk in data:
                    await self.conn.send(
                        data=chunk,
                        response=True,
                    )
            return data
        except BaseException as error:
            self.logging.error(f"could not upload gif unprocessed: {error}")
            return False

    async def uploadProcessed(
        self, file_path: str, pixel_size: int = 32
    ) -> Union[bool, bytearray]:
        """uploads a file processed to make sure everything is correct before uploading to the device.

        Args:
            file_path (str): path to the image file
            pixel_size (int, optional): amount of pixels (either 16 or 32 makes sense). Defaults to 32.

        Returns:
            Union[bool, bytearray]: False if there's an error, otherwise returns bytearray payload
        """
        try:
            with PilImage.open(file_path) as img:
                frames = []
                try:
                    while True:
                        frame = img.copy()
                        if frame.size != (pixel_size, pixel_size):
                            frame = frame.resize(
                                (pixel_size, pixel_size), PilImage.NEAREST
                            )
                        frames.append(frame.copy())
                        img.seek(img.tell() + 1)
                except EOFError:
                    pass
                gif_buffer = io.BytesIO()
                frames[0].save(
                    gif_buffer,
                    format="GIF",
                    save_all=True,
                    append_images=frames[1:],
                    loop=1,
                    duration=img.info["duration"],
                    disposal=2,
                )
                gif_buffer.seek(0)
                data = self._createPayloads(gif_buffer.getvalue())
                if self.conn:
                    await self.conn.connect()
                    for chunk in data:
                        await self.conn.send(data=chunk, response=True)
                return data
        except BaseException as error:
            self.logging.error(f"could not upload gif processed: {error}")
            return False
