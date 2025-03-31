## @file generate_signing_key.py
# This module represents the application to generate a signing key, encrypt it with a PIN, and save it to the USB drive.

import threading
import time
import dearpygui.dearpygui as dpg

from lib.crypt import *
from lib.key_management import generate_and_save_keys
from lib.usb import get_usb_drives
from windows.input_pin_window import input_pin_window
from windows.error_window import error_window
from windows.success_window import success_window

## @var popup_position
# The position of the popup windows.
popup_position = (10, 50)


def resize_callback():
    """!
    Callback function to resize the main window to the size of the viewport.
    """
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()
    dpg.set_item_width("main_window", viewport_width)
    dpg.set_item_height("main_window", viewport_height)


def main():
    """!
    Entrypoint of the application.
    """
    pin = None
    available_usb_devices = []
    selected_usb_device = None

    stop_event = threading.Event()

    def refresh_usb_drives_thread(stop_event: threading.Event):
        nonlocal available_usb_devices
        while not stop_event.is_set():
            available_usb_devices = get_usb_drives()
            dpg.configure_item("select_usb", items=available_usb_devices)
            time.sleep(0.1)

    usb_drives_thread = threading.Thread(
        target=refresh_usb_drives_thread, args=(stop_event,)
    )

    def enter_pin_callback(window_tag: str, input_pin: str):
        if len(input_pin) < 4:
            error_window(
                "PIN must be at least 4 characters long!", position=popup_position
            )
            return
        dpg.delete_item(window_tag)

        nonlocal pin
        pin = input_pin
        dpg.configure_item(
            "pin_status",
            default_value=f"PIN is set ({'*' * len(input_pin)})",
            color=(0, 255, 0, 255),
        )

    def select_usb_drive_callback(sender, app_data):
        nonlocal selected_usb_device
        selected_usb_device = [
            usb for usb in available_usb_devices if str(usb) == app_data
        ][0]
        dpg.configure_item(
            "usb_status",
            default_value=f"Selected USB device: {selected_usb_device}",
            color=(0, 255, 0, 255),
        )

    def generate_key_callback(sender, app_data):
        nonlocal pin, selected_usb_device
        if not pin:
            error_window("Please set a PIN first!", position=popup_position)
            return
        if not selected_usb_device:
            error_window("Please select a USB drive first!", position=popup_position)
            return

        dpg.configure_item(
            "generate",
            label="Generating...",
            enabled=False,
        )

        _, public_key_path = generate_and_save_keys(
            selected_usb_device.mount_point, pin
        )

        success_window(
            f"Private key generated successfully at \nthe {selected_usb_device} drive!\n\nPublic key saved at\n{public_key_path}",
            position=popup_position,
        )

        dpg.configure_item(
            "generate",
            label="Generate Key",
            enabled=True,
        )

    dpg.create_context()
    dpg.create_viewport(
        title="Generate Signing Key", width=320, height=300, resizable=False
    )
    dpg.setup_dearpygui()

    monitor_width = dpg.get_viewport_client_width()
    monitor_height = dpg.get_viewport_client_height()
    dpg.set_viewport_pos([monitor_width // 2, monitor_height // 2])

    with dpg.window(
        tag="main_window",
        no_resize=True,
        no_move=True,
        no_title_bar=True,
        no_scrollbar=True,
        no_bring_to_front_on_focus=True,
        pos=[0, 0],
        on_close=lambda: stop_event.set(),
    ):
        dpg.add_text("Generate Signing Key")
        dpg.add_button(
            label="Setup PIN",
            width=300,
            callback=lambda: input_pin_window(enter_pin_callback, position=(10, 10)),
        )
        dpg.add_text(
            default_value="PIN is not set",
            tag="pin_status",
            color=(255, 0, 0, 255),
        )

        dpg.add_spacer(height=20)

        dpg.add_text("Select USB drive")
        dpg.add_listbox(
            items=[],
            tag="select_usb",
            width=300,
            callback=select_usb_drive_callback,
        )
        dpg.add_text(
            default_value="USB device is not selected",
            tag="usb_status",
            color=(255, 0, 0, 255),
        )

        dpg.add_spacer(height=20)

        dpg.add_button(
            label="Generate Key",
            tag="generate",
            width=300,
            height=50,
            callback=generate_key_callback,
        )

    usb_drives_thread.start()

    dpg.set_viewport_resize_callback(resize_callback)
    resize_callback(None, None)

    dpg.show_viewport()
    dpg.start_dearpygui()
    stop_event.set()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
