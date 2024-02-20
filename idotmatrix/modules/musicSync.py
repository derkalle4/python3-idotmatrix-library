from typing import Union
from ..connectionManager import ConnectionManager
import logging


class MusicSync:
    logging = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.conn: ConnectionManager = ConnectionManager()

    async def setMicType(self, type: int) -> Union[bool, bytearray]:
        """Set the microphone type. Not referenced anywhere in the iDotMatrix Android App. So not used atm.

        Args:
            type (int): type of the Microphone. Unknown what values can be used.

        Returns:
            Union[bool, bytearray]: False if there's an error, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            data = bytearray(
                [
                    6,
                    0,
                    11,
                    128,
                    type % 256,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except BaseException as error:
            self.logging.error(f"could not set the microphone type: {error}")
            return False

    async def sendImageRythm(self, value1: int) -> Union[bool, bytearray]:
        """Set the image rhythm. Not referenced anywhere in the iDotMatrix Android App. When used (tested with values up to 10)
        it displays a stick figure which dances if the value1 gets changed often enough to a different one.

        Args:
            value1 (int): type of the rhythm? Unknown what values can be used.

        Returns:
            Union[bool, bytearray]: False if there's an error, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            data = bytearray(
                [
                    6,
                    0,
                    0,
                    2,
                    value1 % 256,
                    1,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except BaseException as error:
            self.logging.error(f"could not set the image rhythm: {error}")
            return False

    async def sendRhythm(
        self, mode: int, byteArray: bytearray
    ) -> Union[bool, bytearray]:
        """Used to send synchronized Microphone sound data to the device and visualizing it. Is handled in MicrophoneActivity.java of the
        iDotMatrix Android App. Will not be implemented here because there are no plans to support the computer microphone. The device
        has an integrated microphone which is able to react to sound.

        Args:
            mode (int): mode of the rhythm.
            byteArray (bytearray): actual microphone sound data for the visualization.

        Returns:
            Union[bool, bytearray]: The original byte array or False if there's an error.
        """
        try:
            # Assuming `mode` is intended to be used in future or within `byteArray` preparation.
            data = byteArray
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except BaseException as error:
            self.logging.error(f"could not set the rhythm: {error}")
            return False

    async def stopRythm(self) -> bytearray:
        """Stops the Microphone Rhythm on the iDotMatrix device.

        Returns:
            bytearray: Byte array of the command which needs to be sent to the device.
        """
        data = bytearray(
            [
                6,
                0,
                0,
                2,
                0,
                0,
            ]
        )
        if self.conn:
            await self.conn.connect()
            await self.conn.send(data=data)
        return data
