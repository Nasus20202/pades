import dearpygui.dearpygui as dpg


def success_window(
    message: str = "Success!", position: tuple[int, int] = (0, 0)
) -> str:
    tag = f"success_{dpg.generate_uuid()}"
    with dpg.window(label="Success", tag=tag, modal=True, pos=position):
        dpg.add_text(message, color=(0, 255, 0, 255))
        dpg.add_button(
            label="Close",
            callback=lambda: dpg.delete_item(tag),
        )
        dpg.show_item(tag)
    return tag
