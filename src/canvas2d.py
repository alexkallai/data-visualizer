from vispy.scene import SceneCanvas, visuals



class CanvasWrapper2D:
    def __init__(self):
        self.canvas = SceneCanvas()
        self.grid = self.canvas.central_widget.add_grid()

        self.view_top = self.grid.add_view(0, 0, bgcolor='cyan')
        #image_data = _generate_random_image_data(IMAGE_SHAPE)
        image_data = None
        self.image = visuals.Image(
            image_data,
            texture_format="auto",
            cmap="viridis",
            parent=self.view_top.scene,
        )
        #self.view_top.camera = "panzoom"
        self.view_top.camera.set_range(x=(0, 800), y=(0, 600), margin=0)

    def set_image_colormap(self, cmap_name: str):
        print(f"Changing image colormap to {cmap_name}")
        self.image.cmap = cmap_name

    def set_line_color(self, color):
        print(f"Changing line color to {color}")
        self.line.set_data(color=color)