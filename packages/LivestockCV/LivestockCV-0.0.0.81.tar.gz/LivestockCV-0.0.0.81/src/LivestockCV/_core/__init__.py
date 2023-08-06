# Versioning
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__all__ = ['fatal_error', 'Params', 'Outputs', 'deprecation_warning', 'print_image', 'plot_image', 'color_palette', 'rgb2gray', 'rgb2gray_hsv', 'rgb2gray_lab', 'transform', 'apply_mask', 'crop', 'invert', 'rotate', 'roi', 'threshold', 'gaussian_blur', 'analyze_color', 'frame_count', 'js_to_image', 'bbox_to_bytes','take_photo', 'show_image', "calculate_Angle", '_dimensions']



import os
import matplotlib
from LivestockCV.core.classes import Params
from LivestockCV.core.classes import Outputs
from LivestockCV.core.fatal_error import fatal_error

params = Params()
outputs = Outputs()

from LivestockCV._core.deprecation_warning import deprecation_warning
from LivestockCV._core.print_image import print_image
from LivestockCV._core.plot_image import plot_image
from LivestockCV._core.color_palette import color_palette
from LivestockCV._core.rgb2gray import rgb2gray
from LivestockCV._core.rgb2gray_hsv import rgb2gray_hsv
from LivestockCV._core.rgb2gray_lab import rgb2gray_lab
from LivestockCV._core import transform
from LivestockCV._core.apply_mask import apply_mask
from LivestockCV._core.crop import crop
from LivestockCV._core.invert import invert
from LivestockCV._core.rotate import rotate
from LivestockCV._core import roi
from LivestockCV._core import threshold
from LivestockCV._core.gaussian_blur import gaussian_blur
from LivestockCV._core.analyze_color import analyze_color
from LivestockCV._core.frame_count import frame_count
from LivestockCV._core import js_to_image
from LivestockCV._core import bbox_to_bytes
from LivestockCV._core import take_photo
from LivestockCV._core.show_image import show_image
from LivestockCV._core.CalculateAngle import calculate_Angle
from LivestockCV._core.Dimensions import Dimensions




