from ..connectionManager import ConnectionManager
import logging
from typing import Union

"""
The effect modes are:
0 graduated horizontal rainbow
1 random coloured pixels on black
2 random white pixels on changing background
3 vertical rainbow
4 diagonal right rainbow
5 diagonal left rainbow, on black background
6 random coloured pixels
"""

class Effect:
    """This class contains the Effect controls for the iDotMatrix device."""

    logging = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.conn: ConnectionManager = ConnectionManager()

    async def setMode(
        self,
        style: int,
        rgb_values: list[tuple[int, int, int]],
    ) -> Union[bool, bytearray]:
        """Set the effect mode of the device.

        Args:
            style (int): Style of the effect 0-6.
            list of red, green, blue tuples 2-7.

        Returns:
            Union[bool, bytearray]: False if input validation fails, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            if style not in range(0, 7):
                self.logging.error(
                    "effect.setMode expects parameter style to be between 0 and 6"
                )
                return False

            if len(rgb_values) not in range(2, 8):
                self.logging.error(
                    "effect.setMode expects parameter rgb_values to be a list of tuples to be between 2 and 7"
                )
                return False

            for rgb in rgb_values:
                for r, g, b in [rgb]:
                    if r not in range(0, 256) or g not in range(0, 256) or b not in range(0, 256):
                        self.logging.error(
                            f"effect.setMode expects parameter rgb_values to be a list of tuples of red, green, blue values between 0 and 255. Invalid tuple: {rgb}"
                        )
                        return False

            processed_rgb_values = [
                (r % 256, g % 256, b % 256)
                for rgb in rgb_values
                for r, g, b in [rgb + (255,) * (3 - len(rgb))]
            ]

            data = bytearray(
                [
                    6 + len(processed_rgb_values),
                    0,
                    3,
                    2,
                    style % 256,
                    90,
                    len(processed_rgb_values) % 256,
                ] + [component for rgb in processed_rgb_values for component in rgb]
            )

            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except BaseException as error:
            self.logging.error(f"Could not set the effect mode: {error}")
            return False
