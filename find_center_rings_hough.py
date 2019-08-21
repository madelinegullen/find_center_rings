import numpy as np
import matplotlib.pyplot as plt

from skimage import color
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter

def find_center_rings_hough(image, num_rings, rad_range, intensity_thresh, sigma, v_range = None, mute_graph = False):
    """
    Take angled cut or multiple incremented cuts of a image data.

    Parameters
    ----------
    image : ndarray
        Image data
    num_rings : int
        Number of candidate circles to be searched for
    rad_range : array
        The min, max, and increment for range of candidate radii to be searched
    intensity_thresh : array
        Min and max of intensity to be used in canny filter
    sigma : float
        Standard deviation applied in canny filter
    v_range : array
        Min and max for matplotlib colormap

    Returns
    -------
    center :list
        Center coordinates of candidate circles as (x,y) tuples
    radii: array
        radii of the candidate circles

    """

    low_thresh, hi_thresh = intensity_thresh
    sigma = sigma
    edges = feature.canny(image, sigma, low_threshold= low_thresh, high_threshold= hi_thresh)

    # Range of possible radii
    hough_radii = np.arange(*rad_range)
    hough_res = transform.hough_circle(edges, hough_radii)

    # Selects the most prominent circles, up to num_rings
    accums, cx, cy, radii = transform.hough_circle_peaks(hough_res, hough_radii,
                                               total_num_peaks=num_rings)

    # Draw them
    if mute_graph == False:
        fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
    Z = color.gray2rgb(image)

    centers =[]
    for center_y, center_x, radius in zip(cy, cx, radii):
        centers.append((center_x, center_y))
        if mute_graph == False:
            circy, circx = draw.circle_perimeter(center_y, center_x, radius,
                                        shape=Z.shape)
            ax.scatter(center_x, center_y, s =20, c = 'red')
            ax.scatter(x = circx,y =circy, s = 1, c = 'red')

    if mute_graph == False:
        if v_range != None:
            ax.imshow(image, cmap="viridis", vmin = v_range[0], vmax = v_range[1])
        else:
            ax.imshow(image, cmap="viridis")
    plt.show()
    return centers, radii
