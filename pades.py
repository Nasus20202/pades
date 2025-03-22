import dearpygui.dearpygui as dpg

from lib.usb import get_usb_drives
from windows.sign_pdf_window import sign_pdf_window
from windows.verify_signature_window import verify_signature_window


def resize_callback(sender, app_data):
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()
    dpg.set_item_width("main_window", viewport_width)
    dpg.set_item_height("main_window", viewport_height)


def main():
    dpg.create_context()
    dpg.create_viewport(title="PAdES", width=820, height=600, resizable=False)
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
        dpg.add_text("Sign and verify PDFs with PAdES")

        dpg.add_spacer(height=50)

        dpg.add_button(
            label="Sign PDF",
            width=800,
            height=200,
            callback=lambda: sign_pdf_window(position=(10, 10)),
        )

        dpg.add_spacer(height=50)

        dpg.add_button(
            label="Verify Signature",
            width=800,
            height=200,
            callback=lambda: verify_signature_window(position=(410, 10)),
        )

    dpg.set_viewport_resize_callback(resize_callback)
    resize_callback(None, None)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
