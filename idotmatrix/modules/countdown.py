from ..connectionManager import ConnectionManager
import logging
from typing import Union


class Countdown:
    """This class contains the management of the Countdown of the iDotMatrix device."""

    logging = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.conn: ConnectionManager = ConnectionManager()

    async def setMode(
        self, mode: int, minutes: int, seconds: int
    ) -> Union[bool, bytearray]:
        """Sets the countdown (and activates or disables it)

        Args:
            mode (int): mode of the countdown. 0 = disable, 1 = start, 2 = pause, 3 = restart
            minutes (int): minutes to count down from
            seconds (int): seconds to count down from

        Returns:
            Union[bool, bytearray]: False if input validation fails, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            if mode not in range(0, 4):
                self.logging.error(
                    "Countdown.setMode parameter mode is not in range between 0 and 3"
                )
                return False
            # TODO: check for valid range of minutes
            if seconds > 59 or seconds < 0:
                self.logging.error(
                    "Countdown.setMode parameter seconds is not in range between 0 and 59"
                )
                return False
            data = bytearray(
                [
                    7,
                    0,
                    8,
                    128,
                    mode % 256,
                    minutes % 256,
                    seconds % 256,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except BaseException as error:
            self.logging.error(f"could not set the countdown: {error}")
            return False
