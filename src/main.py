import dearpygui.dearpygui as dpg
from itertools import chain
import DearPyGui_DragAndDrop as dpg_dnd
import os
from src.file import File
import ctypes
import numpy as np
import matplotlib.cm as cm

# Include the following code before showing the viewport/calling `dearpygui.dearpygui.show_viewport`.
#ctypes.windll.shcore.SetProcessDpiAwareness(2)

root_path = os.path.dirname(__file__)

STATUS_BAR_HEIGHT = 20
FONT_SCALE = 4
DEBUG_MODE = True
BYTE_SIZE = 256
UPSCALE_FACTOR = 4

# TODO: remove this
texture_data = []
for i in range(0, BYTE_SIZE * BYTE_SIZE * UPSCALE_FACTOR * UPSCALE_FACTOR):
    texture_data.append(255 / 255)
    texture_data.append(0)
    texture_data.append(255 / 255)
    texture_data.append(255 / 255)

texture_data = np.array(object=texture_data, dtype=np.float32)

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

def set_up_fonts():
    # TODO not workin yet
    # Set up fonts
    with dpg.font_registry():
        font_regular = dpg.add_font(os.path.join(root_path, 'CascadiaCode.ttf'), 16*FONT_SCALE)
    dpg.set_global_font_scale(1/FONT_SCALE)
    dpg.bind_font(font_regular)

def create_sidebar_layout():

    def callback(sender, app_data):
        print('OK was clicked.')
        #print("Sender: ", sender)
        #print("App Data: ", app_data)
        file_key = list(app_data["selections"].keys())[0]
        file_path = app_data["selections"][file_key]
        print(file_path)
        if file_path:
            file = File(file_path)
            image = file.get_2D_digraph_image()
            # TODO: move this to the file class
            # Normalize the image to range [0, 1]
            digraph_norm =image.astype(np.float32) / np.max(image) if np.max(image) > 0 else image.astype(np.float32)

            # Select a colormap (e.g., 'viridis', 'plasma', 'magma', 'inferno', 'cividis')
            colormap = cm.get_cmap('magma')

            # Apply colormap (returns RGBA values in [0,1] range)
            rgba_image = colormap(digraph_norm)

            # Convert to float32
            rgba_image = rgba_image.astype(np.float32)
            rgba_image = np.repeat(np.repeat(rgba_image, UPSCALE_FACTOR, axis=0), UPSCALE_FACTOR, axis=1)
            update_texture("raw_texture_digraph", rgba_image)

    def cancel_callback(sender, app_data):
        print('Cancel was clicked.')
        #print("Sender: ", sender)
        #print("App Data: ", app_data)

    with dpg.file_dialog(directory_selector=False, show=False, callback=callback, cancel_callback=cancel_callback, id="file_dialog_id", width=700 ,height=400, file_count=1, modal=True):
        dpg.add_file_extension(".*")
    dpg.add_button(label="File Selector", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_slider_double(vertical=True,
                          min_value=0,
                          max_value=100,
                          )

def update_texture(tag: str, new_texture_data):
    dpg.set_value(tag, new_texture_data)

def create_tabs_layout():

    # First, create texture registry
    with dpg.texture_registry(show=False): # TODO modify to False
        dpg.add_raw_texture(width=BYTE_SIZE * UPSCALE_FACTOR, height=BYTE_SIZE * UPSCALE_FACTOR, default_value=texture_data, format=dpg.mvFormat_Float_rgba, tag="raw_texture_digraph")
    # Create the tab bar and tabs
    with dpg.tab_bar(tag="test_tab_bar") as tb:
        #creating a tab with the tag test_tab_1
        with dpg.tab(label="tab 1", tag="test_tab_1"):
            dpg.add_image("raw_texture_digraph")
            #creating a button that executes the callback change_tab with the tag 100
            dpg.add_button(label="activate tab 2", callback=print("TODO"), tag=100)
        #creating a tab with the tag test_tab_2
        with dpg.tab(label="tab 2", tag="test_tab_2"):
            #creating a button that executes the callback change_tab with the tag 200
            dpg.add_button(label="activate tab 1", tag=200, callback=print("TODO"),)
    update_texture("raw_texture_digraph", texture_data)

def file_drop_callback(sender, app_data, user_data):
    pass

def build_window():
    status_bar_theme = create_status_bar_theme()
    def resize_primary_window():
        x,y = dpg.get_item_rect_size(primary_window)
        dpg.configure_item(status_bar, width=x)
        dpg.configure_item(status_bar, pos=(0, y-STATUS_BAR_HEIGHT))
        dpg.configure_item(child_window_1, height=y-STATUS_BAR_HEIGHT*3)
        dpg.configure_item(child_window_2, height=y-STATUS_BAR_HEIGHT*3)

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
            dpg.add_table_column(width_fixed=True, init_width_or_weight=600)
            dpg.add_table_column()
            with dpg.table_row():
                with dpg.group():
                    with dpg.child_window() as child_window_1:
                        create_sidebar_layout()
                with dpg.group():
                    with dpg.child_window() as child_window_2:
                        # TAB layout
                        create_tabs_layout()

        with dpg.window(no_title_bar=True, no_move=True, no_resize=False) as status_bar:
            dpg.bind_item_theme(status_bar, status_bar_theme)
            with dpg.group(horizontal=True):
                dpg.add_text("Hello")
                dpg.add_button(label="world")

def initialize_drag_and_drop():
    # TODO: add drag over enter etc. https://github.com/IvanNazaruk/DearPyGui-DragAndDrop/blob/main/Examples/example3.py
    
    # Init drop feature
    dpg_dnd.initialize()
    def drop(data, keys):
        print(f'{data}')
        #print(f'{keys}')
    dpg_dnd.set_drop(drop)

if __name__ == "__main__":

    dpg.create_context()
    initialize_drag_and_drop()
    dpg.configure_app(manual_callback_management=DEBUG_MODE)
    set_up_fonts()
    build_window()


    dpg.create_viewport(width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    if DEBUG_MODE:
        # TODO: not working
        while dpg.is_dearpygui_running():
            jobs = dpg.get_callback_queue() # retrieves and clears queue
            dpg.run_callbacks(jobs)
            dpg.render_dearpygui_frame()
    else:
        dpg.start_dearpygui()
    dpg.destroy_context()