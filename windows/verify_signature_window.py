## @file verify_signature_window.py
# This module contains the function to create a window to verify the signature of a PDF file.
import dearpygui.dearpygui as dpg

from lib.key_management import read_public_key
from lib.pdf_signing import verify_pdf
from windows.error_window import error_window
from windows.success_window import success_window


def verify_signature_window(
    position: tuple[int, int] = (0, 0),
    popup_position=(0, 0),
    width=400,
    height=550,
) -> str:
    """!
    Create and display a window to verify the signature of a PDF file.

    @param position: The position of the window.
    @param popup_position: The position of the popup windows.
    @param width: The width of the window.
    @param height: The height of the window.

    @return The tag of the created window.
    """
    tag = f"verify_signature_{dpg.generate_uuid()}"

    selected_pdf_file = None
    selected_public_key_file = None

    def select_pdf_callback(sender, app_data):
        nonlocal selected_pdf_file
        selected_pdf_file = app_data["file_path_name"]
        dpg.configure_item(
            f"pdf_status_{tag}",
            default_value=f"Selected PDF: {app_data['file_name']}",
            color=(0, 255, 0, 255),
        )

    def select_public_key_callback(sender, app_data):
        nonlocal selected_public_key_file
        selected_public_key_file = app_data["file_path_name"]
        dpg.configure_item(
            f"public_key_status_{tag}",
            default_value=f"Selected Public Key: {app_data["file_name"]}",
            color=(0, 255, 0, 255),
        )

    def verify_signature_callback(sender, app_data):
        nonlocal selected_pdf_file, selected_public_key_file
        if not selected_pdf_file:
            error_window("Please select a PDF file first!", position=popup_position)
            return
        if not selected_public_key_file:
            error_window(
                "Please select a public key file first!", position=popup_position
            )
            return

        public_key = read_public_key(selected_public_key_file)
        is_valid = verify_pdf(selected_pdf_file, public_key)

        if is_valid:
            success_window("Signature is valid!", position=popup_position)
        else:
            error_window("Signature is not valid!", position=popup_position)

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

    with dpg.file_dialog(
        label="Select Public Key",
        tag=f"select_public_key_{tag}",
        width=600,
        height=500,
        callback=select_public_key_callback,
        show=False,
    ):
        dpg.add_file_extension(".pub", custom_text="PUB files")
        dpg.add_file_extension(".*", custom_text="All files")

    with dpg.window(
        label="Verify Signature", tag=tag, width=width, height=height, pos=position
    ):
        dpg.add_text("Select a PDF file to verify its signature")
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

        dpg.add_spacer(height=50)

        dpg.add_text("Select a public key file to verify the signature")
        dpg.add_button(
            label="Select Public Key",
            width=380,
            height=50,
            callback=lambda: dpg.show_item(f"select_public_key_{tag}"),
        )
        dpg.add_text(
            default_value="Public key file is not selected",
            tag=f"public_key_status_{tag}",
            color=(255, 0, 0, 255),
        )

        dpg.add_spacer(height=50)

        dpg.add_button(
            label="Verify Signature",
            width=380,
            height=50,
            callback=verify_signature_callback,
        )

    return tag
