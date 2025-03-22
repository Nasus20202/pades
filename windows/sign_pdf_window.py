import dearpygui.dearpygui as dpg
import threading
import time

from lib.usb import get_usb_drives


def sign_pdf_window(
    position: tuple[int, int] = (0, 0),
    width=800,
    height=550,
) -> str:
    tag = f"verify_signature_window_{dpg.generate_uuid()}"

    usb_devices = []
    selected_device = None
    stop_event = threading.Event()

    def update_usb_devices_thread(stop_event: threading.Event):
        nonlocal usb_devices
        while not stop_event.is_set():
            usb_devices = get_usb_drives()
            dpg.configure_item(f"select_usb_{tag}", items=usb_devices)
            time.sleep(0.1)

    thread = threading.Thread(target=update_usb_devices_thread, args=(stop_event,))
    thread.start()

    def select_usb_drive_callback(sender, app_data):
        nonlocal selected_device
        selected_device = [usb for usb in usb_devices if str(usb) == app_data][0]

        dpg.configure_item(
            f"usb_status_{tag}",
            default_value=f"Selected USB device: {selected_device}",
            color=(0, 255, 0, 255),
        )

    with dpg.window(
        label="Verify Signature",
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
            callback=select_usb_drive_callback,
        )
        dpg.add_text(
            default_value="USB device is not selected",
            tag=f"usb_status_{tag}",
            color=(255, 0, 0, 255),
        )

    return tag
