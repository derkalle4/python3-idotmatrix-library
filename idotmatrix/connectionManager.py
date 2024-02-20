from typing import List, Optional
from bleak import BleakClient, BleakScanner, BLEDevice, AdvertisementData
import logging
from .const import UUID_READ_DATA, UUID_WRITE_DATA, BLUETOOTH_DEVICE_NAME


class SingletonMeta(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs) -> "SingletonMeta":
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConnectionManager(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.address: Optional[str] = None
        self.client: Optional[BleakClient] = None

    @staticmethod
    async def scan_and_filter_devices() -> List[str]:
        logging.info("scanning for iDotMatrix bluetooth devices...")
        devices = await BleakScanner.discover(return_adv=True)
        filtered_devices: List[str] = []
        for key, (device, adv) in devices.items():
            if (
                isinstance(adv, AdvertisementData)
                and adv.local_name
                and str(adv.local_name).startswith(BLUETOOTH_DEVICE_NAME)
            ):
                logging.info(f"found device {key} with name {adv.local_name}")
                filtered_devices.append(device.address)
        return filtered_devices

    async def connect_by_address(self, address: str) -> None:
        self.address = address
        await self.connect()

    async def connect_by_search(self) -> None:
        devices = await self.scan_and_filter_devices()
        if devices:
            # connect to first device
            self.address = devices[0]
            await self.connect()
        else:
            logging.error("no target devices found.")

    async def connect(self) -> None:
        if self.address:
            if not self.client:
                self.client = BleakClient(self.address)
            if not self.client.is_connected:
                await self.client.connect()
                logging.info(f"Connected to {self.address}")
        else:
            logging.error("device address is not set.")

    async def disconnect(self) -> None:
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            logging.info(f"disconnected from {self.address}")

    async def send(self, data: bytes) -> None:
        if self.client and self.client.is_connected:
            await self.client.write_gatt_char(UUID_WRITE_DATA, data)
            logging.info("data sent")

    async def read(self) -> bytes:
        if self.client and self.client.is_connected:
            data = await self.client.read_gatt_char(UUID_READ_DATA)
            logging.info("data received")
            return data
