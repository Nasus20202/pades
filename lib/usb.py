## @file usb.py
# This module contains functions related to handling USB drives.

import os
from dataclasses import dataclass


@dataclass
class USBDrive:
    """! A dataclass representing a USB drive.

    Attributes: \n
    device: The device path of the USB drive. \n
    mount_point: The mount point of the USB drive.
    """

    device: str
    mount_point: str

    def __str__(self):
        """!
        Return a string representation of the USB drive.

        @return A string representation of the USB drive.
        """
        return f"{self.mount_point.split('/')[-1]} ({self.device})"


def get_usb_drives() -> list[USBDrive]:
    """!
    Get a list of mounted USB drives.

    This function reads the /proc/mounts file to get a list of mounted filesystems
    and search for those that suppose to be USB drives.

    @return A list of USBDrive objects representing the mounted USB drives.
    """
    mounted_usb_drives = []

    with open("/proc/mounts", "r") as f:
        mounts = f.readlines()

    # Iterate over each mounted filesystem
    for mount in mounts:
        parts = mount.split()
        usb_drive = USBDrive(
            parts[0],
            parts[1],
        )

        # Check if the device is a USB drive
        if "usb" in usb_drive.device or "/media/" in usb_drive.mount_point:
            mounted_usb_drives.append(usb_drive)

    return mounted_usb_drives
