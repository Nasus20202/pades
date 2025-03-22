import dearpygui.dearpygui as dpg


def resize_callback(sender, app_data):
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()
    dpg.set_item_width("main_window", viewport_width)
    dpg.set_item_height("main_window", viewport_height)


def main():
    dpg.create_context()
    dpg.create_viewport(title="Generate Signing Key", width=400, height=500)
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
        pos=[0, 0],
    ):
        dpg.add_text("Generate Signing Key")

    dpg.set_viewport_resize_callback(resize_callback)
    resize_callback(None, None)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
