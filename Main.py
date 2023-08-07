from Raster import import_file, binarize_image
from Meaning import detect_edges, find_contours
from Vectorize import rescale_contours, generate_GCODE, write_GCODE

inputImage = import_file()
binarizedImage = binarize_image(inputImage)
edges = detect_edges(binarizedImage)
contours, hierarchy = find_contours(edges)
rescaledContours = rescale_contours(contours)
GCODE = []
GCODE = generate_GCODE(GCODE, rescaledContours)
write_GCODE(GCODE)



