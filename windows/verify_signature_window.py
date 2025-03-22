import dearpygui.dearpygui as dpg


def verify_signature_window(
    position: tuple[int, int] = (0, 0),
    width=400,
    height=550,
) -> str:
    tag = f"verify_signature_{dpg.generate_uuid()}"

    with dpg.window(
        label="Verify Signature", tag=tag, width=width, height=height, pos=position
    ):
        pass

    return tag
