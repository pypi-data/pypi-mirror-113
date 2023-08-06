# Plot image to screen
import cv2
import numpy
import matplotlib
from matplotlib import pyplot 


def _plot(img):


    image_type = type(img)

    dimensions = numpy.shape(img)

    if image_type == numpy.ndarray:
        matplotlib.rcParams['figure.dpi'] = params.dpi
        if len(dimensions) == 3:
            pyplot.figure()
            pyplot.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            pyplot.show()

        elif cmap is None and len(dimensions) == 2:
            pyplot.figure()
            pyplot.imshow(img, cmap="gray")
            pyplot.show()

        elif cmap is not None and len(dimensions) == 2:
            pyplot.figure()
            pyplot.imshow(img, cmap=cmap)
            pyplot.show()

    elif str(image_type) == "<class 'plotnine.ggplot.ggplot'>":
        print(img)
