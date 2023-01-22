from vispy.scene import SceneCanvas, visuals
import numpy as np


class PreviewCanvas:
    def __init__(self):
        self.canvas = SceneCanvas()
        #self.canvas.size = (200, 0)
        self.grid = self.canvas.central_widget.add_grid()

        #self.view_top = self.grid.add_view(0, 0, bgcolor='black')
        #self.view_top = self.grid.add_view(row_span=200, col_span=200, bgcolor='black')
        self.view_top = self.grid.add_view( bgcolor='black')
        image_data = np.empty( (100, 100), dtype=np.uint8 )
        self.image: visuals.Image = visuals.Image(
            data=image_data,
            texture_format="auto",
            cmap="viridis",
            clim="auto",
            parent=self.view_top.scene,
        )
        self.view_top.camera = "panzoom"
        self.view_top.camera.set_range(x=(0, image_data.shape[0]), y=(0, image_data.shape[1]), margin=0)

    def set_image_colormap(self, cmap_name: str):
        print(f"Changing image colormap to {cmap_name}")
        self.image.cmap = cmap_name
    
    def set_image(self, image: np.ndarray):
        self.image.set_data(image)
        self.view_top.camera.set_range(x=(0, image.shape[1]), y=(0, image.shape[0]), margin=0)
        #self.image._update_colortransform_clim()
        #self.image.update()
        self.view_top.update()