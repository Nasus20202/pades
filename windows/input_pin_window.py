import dearpygui.dearpygui as dpg


def input_pin_window(
    enter_pin_callback: callable,
    position: tuple[int, int] = (0, 0),
    width=216,
    height=0,
) -> str:
    tag = f"input_pin_{dpg.generate_uuid()}"
    with dpg.window(
        label="Input Pin",
        tag=tag,
        width=width,
        height=height,
        pos=position,
    ):
        dpg.add_input_text(
            tag=f"{tag}_pin",
            hint="Enter your pin",
            width=200,
        )
        dpg.add_button(
            label="Submit",
            width=200,
            callback=lambda: enter_pin_callback(tag, dpg.get_value(f"{tag}_pin")),
        )
    return tag
