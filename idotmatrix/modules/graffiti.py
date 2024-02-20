from typing import Union
from ..connectionManager import ConnectionManager
import logging


class Graffiti:
    """This class contains the Graffiti controls for the iDotMatrix device."""

    logging = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.conn: ConnectionManager = ConnectionManager()

    async def setPixel(
        self, r: int, g: int, b: int, x: int, y: int
    ) -> Union[bool, bytearray]:
        """Set the scoreboard of the device.

        Args:
            r (int): color red value
            g (int): color green value
            b (int): color blue value
            x (int): pixel x position
            y (int): pixel y position

        Returns:
            Union[bool, bytearray]: False if there's an error, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            if r not in range(0, 256):
                self.logging.error(
                    "Graffiti.setPixel expects parameter r to be between 0 and 255"
                )
                return False
            if g not in range(0, 256):
                self.logging.error(
                    "Graffiti.setPixel expects parameter g to be between 0 and 255"
                )
                return False
            if b not in range(0, 256):
                self.logging.error(
                    "Graffiti.setPixel expects parameter b to be between 0 and 255"
                )
                return False
            if x not in range(0, 256):
                self.logging.error(
                    "Graffiti.setPixel expects parameter x to be between 0 and 255"
                )
                return False
            if y not in range(0, 256):
                self.logging.error(
                    "Graffiti.setPixel expects parameter y to be between 0 and 255"
                )
                return False
            data = bytearray(
                [
                    10,
                    0,
                    5,
                    1,
                    0,
                    r % 256,  # Ensure R, G, B, X, Y are within byte range
                    g % 256,
                    b % 256,
                    x % 256,
                    y % 256,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except BaseException as error:
            self.logging.error(f"could not update the Graffiti Board: {error}")
            return False
