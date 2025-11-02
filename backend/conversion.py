import aspose.cad as cad
from aspose.cad.imageoptions import StpOptions, CadRasterizationOptions
from aspose.cad import Color

# Load the STL file
image = cad.Image.load(r"C:\Users\jiayu\Downloads\93332A238_Titanium Helical Insert.STL")

# Set rasterization options
cadRasterizationOptions = CadRasterizationOptions()
cadRasterizationOptions.page_height = 800.5
cadRasterizationOptions.page_width = 800.5
cadRasterizationOptions.zoom = 1.5
cadRasterizationOptions.layers = "Layer"
cadRasterizationOptions.background_color = Color.green

# Set export options
options = StpOptions()
options.vector_rasterization_options = cadRasterizationOptions

# Save as STEP file
image.save("result.stp", options)