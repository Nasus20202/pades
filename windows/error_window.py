import dearpygui.dearpygui as dpg


def error_window(message: str = "An error occurred!") -> str:
    tag = f"error_{dpg.generate_uuid()}"
    with dpg.window(
        label="Error",
        tag=tag,
        modal=True,
    ):
        dpg.add_text(message, color=(255, 0, 0, 255))
        dpg.add_button(
            label="Close",
            callback=lambda: dpg.delete_item(tag),
        )
        dpg.show_item(tag)
    return tag
