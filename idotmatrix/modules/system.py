from ..connectionManager import ConnectionManager
from cryptography.fernet import Fernet
import logging
from typing import Union


class System:
    """This class contains system calls for the iDotMatrix device."""

    logging = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.conn: ConnectionManager = ConnectionManager()

    async def deleteDeviceData(self) -> bytearray:
        """Deletes the device data and resets it to defaults.

        Returns:
            bytearray: Byte array of the command which needs to be sent to the device.
        """
        data = bytearray(
            [
                17,
                0,
                2,
                1,
                12,
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
            ]
        )
        if self.conn:
            await self.conn.connect()
            await self.conn.send(data=data)
        return data

    def _encryptAes(self, data: bytes, key: bytes) -> bytes:
        """Encrypts data using AES encryption with the given key.

        Args:
            data (bytes): Data to be encrypted.
            key (bytes): Encryption key.

        Returns:
            bytes: Encrypted data.
        """
        f = Fernet(key)
        encrypted_data = f.encrypt(data)
        return encrypted_data

    async def getDeviceLocation(self) -> Union[bool, bytearray]:
        """Gets the device location (untested yet). Missing some AES encryption stuff of iDotMatrix to work.

        Returns:
            Union[bool, bytearray]: False if there's an error, otherwise byte array of the command which needs to be sent to the device.
        """
        # TODO: implement Aes encryption according to iDotMatrix Android App
        try:
            command = bytearray(
                [
                    6,
                    76,
                    79,
                    67,
                    65,
                    84,
                    69,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ]
            )
            key = Fernet.generate_key()
            data = self._encryptAes(bytes(command), key)
            if self.conn:
                await self.conn.connect()
                await self.conn.send(data=data)
            return data
        except Exception as error:
            self.logging.error(f"could not get device location: {error}")
            return False
