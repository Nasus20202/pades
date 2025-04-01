## @file success_window.py
# This module contains the function to create a success window.
import dearpygui.dearpygui as dpg


def success_window(
    message: str = "Success!", position: tuple[int, int] = (0, 0)
) -> str:
    """!
    Create and display a success window.

    @param message: The success message to display.
    @param position: The position of the window.

    @return The tag of the created window.
    """
    tag = f"success_{dpg.generate_uuid()}"
    with dpg.window(label="Success", tag=tag, modal=True, pos=position):
        dpg.add_text(message, color=(0, 255, 0, 255))
        dpg.add_button(
            label="Close",
            callback=lambda: dpg.delete_item(tag),
        )
        dpg.show_item(tag)
    return tag
