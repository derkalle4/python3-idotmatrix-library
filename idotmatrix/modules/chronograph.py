from ..connectionManager import ConnectionManager
import logging
from typing import Union


class Chronograph:
    logging = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.conn: ConnectionManager = ConnectionManager()

    async def setMode(self, mode: int) -> Union[bool, bytearray]:
        """Starts/Stops the Chronograph.

        Args:
            mode (int): 0 = reset, 1 = (re)start, 2 = pause, 3 = continue after pause

        Returns:
            Union[bool, bytearray]: False if input validation fails, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            if mode not in range(0, 4):
                self.logging.error(
                    "Chronograph.setMode expects parameter mode to be between 0 and 3"
                )
                return False
            data: bytearray = bytearray(
                [
                    5,
                    0,
                    9,
                    128,
                    mode,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except (
            Exception
        ) as error:  # BaseException is too broad, better to catch Exception here.
            self.logging.error(f"Could not set the chronograph: {error}")
            return False
