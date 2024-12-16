import dearpygui.dearpygui as dpg
from itertools import chain

STATUS_BAR_HEIGHT = 20

def create_status_bar_theme():
    with dpg.theme() as status_bar_theme:
        with dpg.theme_component():
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (42, 123, 207, 255))
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 4, 0)
    return status_bar_theme

def adjustable_separator(child_window, width=3840, height=5, colour=(255, 255, 255, 50)):
    with dpg.texture_registry():
        data = list(chain.from_iterable([[c / 255 for c in colour] for _ in range(width*height)]))
        separator_texture = dpg.add_static_texture(width=width, height=height, default_value=data)
    separator = dpg.add_image(separator_texture)
    def clicked_callback():
        while dpg.is_mouse_button_down(0):
            y_pos = dpg.get_mouse_pos()[1]
            dpg.split_frame(delay=10)
            y_delta = y_pos - dpg.get_mouse_pos()[1]
            height = dpg.get_item_height(child_window) - y_delta
            if height < 1: height = 1
            dpg.configure_item(child_window, height=height)
    with dpg.item_handler_registry() as item_handler:
        dpg.add_item_clicked_handler(callback=clicked_callback)
    dpg.bind_item_handler_registry(item=separator, handler_registry=item_handler)
 
def build_window():
    status_bar_theme = create_status_bar_theme()

    def resize_primary_window():
        x,y = dpg.get_item_rect_size(primary_window)
        dpg.configure_item(status_bar, width=x)
        dpg.configure_item(status_bar, pos=(0, y-STATUS_BAR_HEIGHT))

    # BUILD MAIN WINDOW
    with dpg.window() as primary_window:
        dpg.set_primary_window(primary_window, True)
        with dpg.item_handler_registry() as registry:
            dpg.add_item_resize_handler(callback=resize_primary_window)
        dpg.bind_item_handler_registry(primary_window, registry)

        with dpg.menu_bar():
            with dpg.menu(label="View"):
                dpg.add_menu_item(label="Show/hide status bar", callback=lambda: dpg.configure_item(status_bar, show=not dpg.is_item_shown(status_bar)))


        with dpg.table(header_row=False, resizable=True):
            dpg.add_table_column(width_fixed=True, init_width_or_weight=200)
            dpg.add_table_column()
            with dpg.table_row():
                with dpg.child_window() as child_window_1:
                    dpg.add_text("Child Window 1")
                with dpg.group():
                    with dpg.child_window() as child_window_2:
                        dpg.add_text("Child Window 2")

        with dpg.window(no_title_bar=True, no_move=True, no_resize=False) as status_bar:
            dpg.bind_item_theme(status_bar, status_bar_theme)
            with dpg.group(horizontal=True):
                dpg.add_text("Hello")
                dpg.add_button(label="world")

if __name__ == "__main__":
    dpg.create_context()

    build_window()

    dpg.create_viewport(width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()