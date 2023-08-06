import numpy as np


def normalize_image(image, normalize_unit=1) -> np.ndarray:
    """

    :param image: list or numpy.ndarray
    :param normalize_unit: the number where the image will be normalized to
    :return: normalized image
    """
    if type(image) is list:
        image = np.array(image)
    elif type(image) is not np.ndarray:
        raise(TypeError('Argument `image` should be either list or numpy.ndarray.'))
    return image/255*normalize_unit


def intersection_x1_y1_x2_y2(box1=None, box2=None):
    x_i = max(box1[0], box2[0])
    y_i = max(box1[1], box2[1])
    width = min(box1[2], box2[2]) - x_i
    height = min(box1[3], box2[3]) - y_i
    return width * height


def iou_x1_y1_x2_y2(box1=None, box2=None):
    """

    :param box1: a list of x1, y1, x2, y2 coordinates of the box 1 on the image
    :param box2: a list of x1, y1, x2, y2 coordinates of the box 1 on the image
    :return: IoU (intersection of union) between two boxes
    >>> iou_x1_y1_x2_y2(box1=[0,0,100,100], box2=[50,50,100,100])
    0.25
    """
    if box1[0] >= box2[2] or box1[2] <= box2[0] or box1[1] >= box2[3] or box1[3] <= box2[1]:
        return 0.0
    intersection = intersection_x1_y1_x2_y2(box1, box2)
    # union
    boxes_area = (box1[2]-box1[0])*(box1[3]-box1[1]) + (box2[2]-box2[0])*(box2[3]-box2[1])
    union = boxes_area - intersection
    if union == 0:
        return 0
    return intersection/union


def iou_xc_yc_w_h(box1=None, box2=None):
    """

    :param box1: a list of center coordinates, xc, yc and width and height, w, h of box 1
    :param box2: a list of center coordinates, xc, yc and width and height, w, h of box 2
    :return: intersection of union
    >>> iou_xc_yc_w_h(box1=[50,50,100,100], box2=[75,75,50,50])
    0.25
    """
    box1_coordinates = [box1[0]-(box1[2]/2), box1[1]-(box1[3]/2), box1[0]+(box1[2]/2), box1[1]+(box1[3]/2)]
    box2_coordinates = [box2[0]-(box2[2]/2), box2[1]-(box2[3]/2), box2[0]+(box2[2]/2), box2[1]+(box2[3]/2)]
    if box1_coordinates[0] >= box2_coordinates[2] or box1_coordinates[2] <= box2_coordinates[0] or \
       box1_coordinates[1] >= box2_coordinates[3] or box1_coordinates[3] <= box2_coordinates[1]:
        return 0.0
    intersection = intersection_x1_y1_x2_y2(box1=box1_coordinates, box2=box2_coordinates)
    union = box1[2]*box1[3] + box2[2]*box2[3] - intersection
    if union == 0:
        return 0
    return intersection/union
