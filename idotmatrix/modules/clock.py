from ..connectionManager import ConnectionManager
import logging
from typing import Optional, Union


class Clock:
    """This class contains the management of the iDotMatrix clock.
    Based on the BleProtocolN.java file of the iDotMatrix Android App.
    """

    logging = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.conn: ConnectionManager = ConnectionManager()

    async def setTimeIndicator(self, enabled: bool = True) -> Union[bool, bytearray]:
        """Sets the time indicator of the clock. Does not seem to work currently (maybe in a future update?).
        It is inside the source code of BleProtocolN.java, but not referenced anywhere.

        Args:
            enabled (bool, optional): Whether or not to show the time indicator of the clock. Defaults to True.

        Returns:
            Union[bool, bytearray]: False if input validation fails, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            data: bytearray = bytearray(
                [
                    5,
                    0,
                    7,
                    128,
                    1 if enabled else 0,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except BaseException as error:
            self.logging.error(f"Could not set the time indicator: {error}")
            return False

    async def setMode(
        self,
        style: int,
        visibleDate: bool = True,
        hour24: bool = True,
        r: int = 255,
        g: int = 255,
        b: int = 255,
    ) -> Union[bool, bytearray]:
        """Set the clock mode of the device.

        Args:
            style (int): Style of the clock.
            visibleDate (bool): Whether the date should be shown or not. Defaults to True.
            hour24 (bool): 12 or 24 hour format. Defaults to True.
            r (int, optional): Color red. Defaults to 255.
            g (int, optional): Color green. Defaults to 255.
            b (int, optional): Color blue. Defaults to 255.

        Returns:
            Union[bool, bytearray]: False if input validation fails, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            if style not in range(0, 8):
                self.logging.error(
                    "Clock.setMode expects parameter style to be between 0 and 7"
                )
                return False
            if r not in range(0, 256):
                self.logging.error(
                    "Clock.setMode expects parameter r to be between 0 and 255"
                )
                return False
            if g not in range(0, 256):
                self.logging.error(
                    "Clock.setMode expects parameter g to be between 0 and 255"
                )
                return False
            if b not in range(0, 256):
                self.logging.error(
                    "Clock.setMode expects parameter b to be between 0 and 255"
                )
                return False
            data: bytearray = bytearray(
                [
                    8,
                    0,
                    6,
                    1,
                    (style | (128 if visibleDate else 0)) | (64 if hour24 else 0),
                    r % 256,
                    g % 256,
                    b % 256,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except BaseException as error:
            self.logging.error(f"Could not set the clock mode: {error}")
            return False
