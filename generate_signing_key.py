import dearpygui.dearpygui as dpg

from const import *
from lib.crypt import *
from lib.usb import get_usb_drives
from windows.input_pin_window import input_pin_window
from windows.error_window import error_window
from windows.success_window import success_window


def resize_callback(sender, app_data):
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()
    dpg.set_item_width("main_window", viewport_width)
    dpg.set_item_height("main_window", viewport_height)


def main():
    pin = None
    available_usb_devices = []
    selected_usb_device = None

    def enter_pin_callback(window_tag: str, input_pin: str):
        if len(input_pin) < 4:
            error_window("PIN must be at least 4 characters long!")
            return
        dpg.delete_item(window_tag)

        nonlocal pin
        pin = input_pin
        dpg.configure_item(
            "pin_status",
            default_value=f"PIN is set ({'*' * len(input_pin)})",
            color=(0, 255, 0, 255),
        )

    def refresh_usb_drives():
        nonlocal available_usb_devices
        available_usb_devices = get_usb_drives()
        dpg.configure_item("select_usb", items=available_usb_devices)

    def select_usb_drive_callback(sender, app_data):
        nonlocal selected_usb_device
        selected_usb_device = [
            usb for usb in available_usb_devices if str(usb) == app_data
        ][0]
        dpg.configure_item(
            "usb_status",
            default_value=f"USB is set to {selected_usb_device}",
            color=(0, 255, 0, 255),
        )

    def generate_key_callback(sender, app_data):
        nonlocal pin
        nonlocal selected_usb_device
        if not pin:
            error_window("Please set a PIN first!")
            return
        if not selected_usb_device:
            error_window("Please select a USB drive first!")
            return

        dpg.configure_item(
            "generate",
            label="Generating...",
            enabled=False,
        )

        private_key, public_key = generate_rsa_key_pair()
        aes_key = hash_string(pin)
        private_key_nonce, encrypted_private_key, private_key_tag = (
            encrypt_data_with_aes(private_key, aes_key)
        )

        private_key_path = f"{selected_usb_device.mount_point}/{PRIVATE_KEY_DIR}{PRIVATE_KEY_FILENAME}{ENCRYPTED_EXTENSION}"
        with open(
            private_key_path,
            "wb",
        ) as file:
            file.write(
                merge_cipher_data(
                    private_key_nonce, encrypted_private_key, private_key_tag
                )
            )

        public_key_path = f"{PUBLIC_KEY_DIR}/{PUBLIC_KEY_FILENAME}"
        with open(
            public_key_path,
            "wb",
        ) as file:
            file.write(public_key)

        success_window(
            f"Private key generated successfully at \nthe {selected_usb_device} drive!\n\nPublic key saved at\n{public_key_path}"
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
    ):
        dpg.add_text("Generate Signing Key")
        dpg.add_button(
            label="Setup PIN",
            width=300,
            callback=lambda: input_pin_window(enter_pin_callback),
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
            default_value="USB is not set",
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

    dpg.set_viewport_resize_callback(resize_callback)
    resize_callback(None, None)

    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        refresh_usb_drives()
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
