import os
from dataclasses import dataclass


@dataclass
class USBDrive:
    device: str
    mount_point: str

    def __str__(self):
        return f"{self.mount_point.split('/')[-1]} ({self.device})"


def get_usb_drives() -> list[USBDrive]:
    mounted_usb_drives = []

    try:
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

    except Exception as e:
        print(f"An error occurred: {e}")

    return mounted_usb_drives
