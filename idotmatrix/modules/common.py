from ..connectionManager import ConnectionManager
from datetime import datetime
import logging
from typing import Optional, Union, List


class Common:
    """This class contains generic Bluetooth functions for the iDotMatrix.
    Based on the BleProtocolN.java file of the iDotMatrix Android App.
    """

    logging = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.conn: ConnectionManager = ConnectionManager()

    async def freezeScreen(self) -> bytearray:
        """Freezes or unfreezes the screen.

        Returns:
            bytearray: Command to be sent to the device.
        """
        data = bytearray(
            [
                4,
                0,
                3,
                0,
            ]
        )
        if self.conn:
            await self.conn.connect()
            await self.conn.send(data=data)
        return data

    async def screenOff(self) -> bytearray:
        """Turns the screen off.

        Returns:
            bytearray: Command to be sent to the device.
        """
        data = bytearray(
            [
                5,
                0,
                7,
                1,
                0,
            ]
        )
        if self.conn:
            await self.conn.connect()
            await self.conn.send(data=data)
        return data

    async def screenOn(self) -> bytearray:
        """Turns the screen on.

        Returns:
            bytearray: Command to be sent to the device.
        """
        data = bytearray(
            [
                5,
                0,
                7,
                1,
                1,
            ]
        )
        if self.conn:
            await self.conn.connect()
            await self.conn.send(data=data)
        return data

    async def flipScreen(self, flip: bool = True) -> Union[bool, bytearray]:
        """Rotates the screen 180 degrees.

        Args:
            flip (bool): False = normal, True = rotated. Defaults to True.

        Returns:
            Union[bool, bytearray]: False if input validation fails, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            data = bytearray(
                [
                    5,
                    0,
                    6,
                    128,
                    1 if flip else 0,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except Exception as error:
            self.logging.error(f"Could not rotate the screen of the device: {error}")
            return False

    async def setBrightness(self, brightness_percent: int) -> Union[bool, bytearray]:
        """Set screen brightness. Range 5-100 (%).

        Args:
            brightness_percent (int): Set the brightness in percent.

        Returns:
            Union[bool, bytearray]: False if input validation fails, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            if brightness_percent not in range(5, 101):
                self.logging.error(
                    "Common.setBrightness parameter brightness_percent is not in range between 5 and 100"
                )
                return False
            data = bytearray(
                [
                    5,
                    0,
                    4,
                    128,
                    brightness_percent,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except Exception as error:
            self.logging.error(f"Could not set the brightness of the screen: {error}")
            return False

    async def setSpeed(self, speed: int) -> Union[bool, bytearray]:
        """Sets the speed of ? - not referenced anywhere in the iDotMatrix Android App.

        Args:
            speed (int): Set the speed.

        Returns:
            Union[bool, bytearray]: False if input validation fails, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            data = bytearray(
                [
                    5,
                    0,
                    3,
                    1,
                    speed,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except Exception as error:
            self.logging.error(f"Could not change the speed of the device: {error}")
            return False

    async def setTime(
        self, year: int, month: int, day: int, hour: int, minute: int, second: int
    ) -> Optional[bytearray]:
        """Sets the date and time of the device.

        Args:
            year (int): Year (4 digits).
            month (int): Month.
            day (int): Day.
            hour (int): Hour.
            minute (int): Minute.
            second (int): Second.

        Returns:
            Optional[bytearray]: Command to be sent to the device or None if error.
        """
        try:
            data = bytearray(
                [
                    11,
                    0,
                    1,
                    128,
                    year % 100,
                    month,
                    day,
                    datetime(year, month, day).weekday() + 1,
                    hour,
                    minute,
                    second,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except Exception as error:
            self.logging.error(f"Could not set the time of the device: {error}")
            return False

    async def setJoint(self, mode: int) -> Union[bool, bytearray]:
        """Currently no idea what this is doing.

        Args:
            mode (int): Set the joint mode.

        Returns:
            Union[bool, bytearray]: False if input validation fails, otherwise byte array of the command which needs to be sent to the device.
        """
        try:
            data = bytearray(
                [
                    5,
                    0,
                    12,
                    128,
                    mode,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except Exception as error:
            self.logging.error(f"Could not change the device joint: {error}")
            return False

    async def setPassword(self, password: int) -> Union[bool, bytearray]:
        """Setting password: 6 digits in range 000000..999999. Reset device to clear.

        Args:
            password (int): Password.

        Returns:
            Union[bool, bytearray]: False if input validation fails, otherwise byte array of the command which needs to be sent to the device.
        """

        try:
            pwd_high = (password // 10000) % 256
            pwd_mid = (password // 100) % 100 % 256
            pwd_low = password % 100 % 256
            data = bytearray(
                [
                    8,
                    0,
                    4,
                    2,
                    1,
                    pwd_high,
                    pwd_mid,
                    pwd_low,
                ]
            )
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except Exception as error:
            self.logging.error(f"Could not set the password: {error}")
            return False


    async def reset(self) -> Union[bool, List[bytearray]]:
        """Sends a command that resets the device and its internals.
        Can fix issues that appear over time.

        Note:
            Credits to 8none1 for finding this method:
            https://github.com/8none1/idotmatrix/commit/1a08e1e9b82d78427ab1c896c24c2a7fb45bc2f0

        Returns:
            Union[bool, List[bytearray]]: False if command fails, otherwise list of byte arrays of the commands which needs to be sent to the device.
        """
        try:
            reset_packets = [
                bytes(bytearray.fromhex("04 00 03 80")),
                bytes(bytearray.fromhex("05 00 04 80 50")),
                ]
            if self.conn:
                for data in reset_packets:
                    await self.conn.connect()
                    await self.conn.send(data=data)
            return reset_packets
        except Exception as error:
            self.logging.error(f"Could not reset the device: {error}")
            return False

