from ..connectionManager import ConnectionManager
import logging
from typing import Union


class Eco:
    """This class contains code for the eco mode of the iDotMatrix device.
    With this class you can enable or disable the screen and change the brightness automatically depending on the time.
    Based on the BleProtocolN.java file of the iDotMatrix Android App.
    """

    logging = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.conn: ConnectionManager = ConnectionManager()

    async def setMode(
        self,
        flag: int,
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int,
        light: int,
    ) -> Union[bool, bytearray]:
        """Sets the eco mode of the device (e.g. turning on or off the device, set the color, ....)

        Args:
            flag (int): currently unknown, seems to be either 1 or 0
            start_hour (int): hour to start
            start_minute (int): minute to start
            end_hour (int): hour to end
            end_minute (int): minute to end
            light (int): the brightness of the screen

        Returns:
            Union[bool, bytearray]: False if input validation fails, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            # TODO check parameters for their valid values and discard everything else
            data = bytearray(
                [
                    10,
                    0,
                    2,
                    128,
                    int(flag) % 256,
                    int(start_hour) % 256,
                    int(start_minute) % 256,
                    int(end_hour) % 256,
                    int(end_minute) % 256,
                    int(light) % 256,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except BaseException as error:
            self.logging.error(f"could not set the eco mode: {error}")
            return False
