## @file error_window.py
# This module contains the function to create an error window.
import dearpygui.dearpygui as dpg


def error_window(
    message: str = "An error occurred!",
    position: tuple[int, int] = (0, 0),
) -> str:
    """!
    Create and display an error window.

    @param message: The error message to display.
    @param position: The position of the window.

    @return The tag of the created window.
    """
    tag = f"error_{dpg.generate_uuid()}"
    with dpg.window(label="Error", tag=tag, modal=True, pos=position):
        dpg.add_text(message, color=(255, 0, 0, 255))
        dpg.add_button(
            label="Close",
            callback=lambda: dpg.delete_item(tag),
        )
        dpg.show_item(tag)
    return tag
