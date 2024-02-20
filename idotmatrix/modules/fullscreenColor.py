from typing import Union
from ..connectionManager import ConnectionManager
import logging


class FullscreenColor:
    """This class contains the management of the iDotMatrix fullscreen color mode.
    Based on the BleProtocolN.java file of the iDotMatrix Android App.
    """

    logging = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.conn: ConnectionManager = ConnectionManager()

    async def setMode(
        self, r: int = 0, g: int = 0, b: int = 0
    ) -> Union[bool, bytearray]:
        """Sets the fullscreen color of the screen of the device

        Args:
            r (int, optional): color red. Defaults to 0.
            g (int, optional): color green. Defaults to 0.
            b (int, optional): color blue. Defaults to 0.

        Returns:
            Union[bool, bytearray]: False if input validation fails, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            if r not in range(0, 256):
                self.logging.error(
                    "FullscreenColor.setMode expects parameter r to be between 0 and 255"
                )
                return False
            if g not in range(0, 256):
                self.logging.error(
                    "FullscreenColor.setMode expects parameter g to be between 0 and 255"
                )
                return False
            if b not in range(0, 256):
                self.logging.error(
                    "FullscreenColor.setMode expects parameter b to be between 0 and 255"
                )
            data = bytearray(
                [
                    7,
                    0,
                    2,
                    2,
                    int(r) % 256,
                    int(g) % 256,
                    int(b) % 256,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except BaseException as error:
            self.logging.error(f"could not set the color: {error}")
            return False
