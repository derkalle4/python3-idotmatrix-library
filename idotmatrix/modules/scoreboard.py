from typing import Union
from ..connectionManager import ConnectionManager
import logging
import struct


class Scoreboard:
    """This class contains the Scoreboard management of the iDotMatrix device."""

    logging = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.conn: ConnectionManager = ConnectionManager()

    async def setMode(self, count1: int, count2: int) -> Union[bool, bytearray]:
        """Set the scoreboard of the device.

        Args:
            count1 (int): first counter, max: 999 (buffer overflow if more! -> might lead to unintended behavior)
            count2 (int): second counter, max: 999 (buffer overflow if more! -> might lead to unintended behavior)

        Returns:
            Union[bool, bytearray]: False if there's an error, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            # Packing counts into two bytes (big-endian) each, assuming the counts are not exceeding 16-bit max value.
            bytearray_count1 = struct.pack(
                "!H", max(0, min(999, count1))
            )  # Clamping the value to be between 0 and 999
            bytearray_count2 = struct.pack(
                "!H", max(0, min(999, count2))
            )  # Clamping the value to be between 0 and 999

            # Preparing the data to be sent, adjusting the indices according to the byte order.
            data = bytearray(
                [
                    8,  # Command start
                    0,  # Placeholder
                    10,  # Command ID
                    128,  # Another command specifier
                    bytearray_count1[1],  # Lower byte of count1
                    bytearray_count1[0],  # Upper byte of count1
                    bytearray_count2[1],  # Lower byte of count2
                    bytearray_count2[0],  # Upper byte of count2
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except BaseException as error:
            self.logging.error(f"could not update the scoreboard: {error}")
            return False
