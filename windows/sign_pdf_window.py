import dearpygui.dearpygui as dpg
import threading
import time

from lib.key_management import (
    check_if_directory_contains_keys,
    read_and_decrypt_private_key,
)
from lib.pdf_signing import sign_pdf
from lib.usb import get_usb_drives
from windows.success_window import success_window
from windows.error_window import error_window
from windows.input_pin_window import input_pin_window


def sign_pdf_window(
    position: tuple[int, int] = (0, 0),
    popup_position=(0, 0),
    width=400,
    height=550,
) -> str:
    tag = f"sign_pdf_{dpg.generate_uuid()}"

    usb_devices = []
    selected_device = None
    pin = None
    selected_pdf_file = None

    stop_event = threading.Event()

    def update_usb_devices_thread(stop_event: threading.Event):
        nonlocal usb_devices
        while not stop_event.is_set():
            usb_devices = [
                device
                for device in get_usb_drives()
                if check_if_directory_contains_keys(device.mount_point)
            ]
            dpg.configure_item(f"select_usb_{tag}", items=usb_devices)
            time.sleep(0.1)

    usb_drives_thread = threading.Thread(
        target=update_usb_devices_thread, args=(stop_event,)
    )

    def select_usb_drive_callback(sender, app_data):
        nonlocal selected_device
        selected_device = [usb for usb in usb_devices if str(usb) == app_data][0]

        dpg.configure_item(
            f"usb_status_{tag}",
            default_value=f"Selected USB device: {selected_device}",
            color=(0, 255, 0, 255),
        )

    def enter_pin_callback(pin_input_tag: str, new_pin: str):
        nonlocal pin
        pin = new_pin
        dpg.delete_item(pin_input_tag)
        dpg.configure_item(
            f"pin_status_{tag}",
            default_value=f"PIN is entered ({'*' * len(pin)})",
            color=(0, 255, 0, 255),
        )

    def select_pdf_callback(sender, app_data):
        nonlocal selected_pdf_file
        selected_pdf_file = app_data["file_path_name"]
        dpg.configure_item(
            f"pdf_status_{tag}",
            default_value=f"Selected PDF file: {app_data["file_name"]}",
            color=(0, 255, 0, 255),
        )

    def sign_pdf_callback(sender, app_data):
        if not selected_device:
            error_window("Please select a USB device first!", position=popup_position)
            return

        if not pin:
            error_window("Please enter a PIN first!", position=popup_position)
            return

        if not selected_pdf_file:
            error_window("Please select a PDF file first!", position=popup_position)
            return

        try:
            private_key = read_and_decrypt_private_key(pin, selected_device.mount_point)
        except ValueError as e:
            error_window(f"Decrypting key failed! {e}", position=popup_position)
            return

        sign_pdf(selected_pdf_file, private_key)

        success_window("PDF signed successfully!", position=popup_position)

    with dpg.file_dialog(
        label="Select PDF",
        tag=f"select_pdf_{tag}",
        width=600,
        height=500,
        callback=select_pdf_callback,
        show=False,
    ):
        dpg.add_file_extension(".pdf", custom_text="PDF files")
        dpg.add_file_extension(".*", custom_text="All files")

    with dpg.window(
        label="Sign PDF",
        tag=tag,
        width=width,
        height=height,
        pos=position,
        on_close=lambda: stop_event.set(),
    ):
        dpg.add_text("Select a USB device to sign the PDF with:")
        dpg.add_listbox(
            items=[],
            tag=f"select_usb_{tag}",
            width=380,
            callback=select_usb_drive_callback,
        )
        dpg.add_text(
            default_value="USB device is not selected",
            tag=f"usb_status_{tag}",
            color=(255, 0, 0, 255),
        )

        dpg.add_spacer(height=30)

        dpg.add_button(
            label="Insert PIN",
            width=380,
            height=50,
            callback=lambda: input_pin_window(enter_pin_callback, position=(100, 150)),
        )
        dpg.add_text(
            default_value="PIN is not entered",
            tag=f"pin_status_{tag}",
            color=(255, 0, 0, 255),
        )

        dpg.add_spacer(height=30)

        dpg.add_text("Select a PDF file to sign:")
        dpg.add_button(
            label="Select PDF",
            width=380,
            height=50,
            callback=lambda: dpg.show_item(f"select_pdf_{tag}"),
        )
        dpg.add_text(
            default_value="PDF file is not selected",
            tag=f"pdf_status_{tag}",
            color=(255, 0, 0, 255),
        )

        dpg.add_spacer(height=30)

        dpg.add_button(
            id=f"sign_pdf_button_{tag}",
            label="Sign PDF",
            callback=sign_pdf_callback,
            height=50,
            width=380,
        )

    usb_drives_thread.start()

    return tag
