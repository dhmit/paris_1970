import cv2
import pytesseract
import numpy as np

from pdf2image import convert_from_path
from scipy import ndimage

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

"""
Constants
"""

DOCUMENT_1_INFO = {
    # Measured using image editing software (PAINT.NET)
    # Format: slice(x, x + column_width)
    "columns": {
        0: slice(0, 260),
        1: slice(260, 260 + 482),
        2: slice(742, 742 + 682),
        3: slice(1424, 1424 + 620)
    },
    "row_height": 68,
    "table_area": (slice(243, 243 + 2007), slice(314, 314 + 2290)),
    "rows_per_page": 30,
    "column_scan_mode": {0: "eng", 1: "eng", 2: "eng", 3: "eng"},
    "text_threshold": 180  # Tested several values: 180 works well
}


## Unused
def fill_holes(img, times=1):
    new_img = img
    for t in range(times):
        new_img = ndimage.binary_fill_holes(new_img)
    return new_img


def pdf_to_images(pdf_path, page_ranges, thread_count=4):
    """
    Given a PDF file and a list of page ranges, generate images of the PDF pages
    corresponding to the pages in the ranges.

    Parameters
    ----------
    pdf_path : TYPE
        DESCRIPTION.
    page_ranges : TYPE
        DESCRIPTION.
    thread_count : TYPE, optional
        DESCRIPTION. The default is 4.

    Yields
    ------
    TYPE
        DESCRIPTION.

    """
    images = convert_from_path(pdf_path, thread_count=thread_count)
    pages = ranges_to_page_set(page_ranges) if page_ranges else None
    for i, image in enumerate(images):
        if pages is None or i in pages:
            yield np.array(image)


def place_on_center(main_image, other_image):
    coord = []
    for c in range(2):
        coord.append((main_image.shape[c] - other_image.shape[c]) / 2)
    y, x = coord
    if y < 0 and x < 0:
        x, y = int(round(x)), int(round(y))
        return other_image[-y:main_image.shape[0] - y, -x:main_image.shape[1] - x]
    if y < 0:
        y = int(round(y))
        other_image = other_image[-y:main_image.shape[0] - y]
        x, y = int(round(x)), 0
    if x < 0:
        x = int(round(x))
        other_image = other_image[:, -x:main_image.shape[1] - x]
        x, y = 0, int(round(y))
    x, y = int(round(x)), int(round(y))
    main_image[y:y + other_image.shape[0], x:x + other_image.shape[1]] = other_image


def expand_dims_to(np_array, expand_axis, axis_dim):
    new_shape = list(np_array.shape)
    new_shape.insert(expand_axis, axis_dim)
    return np.broadcast_to(np.expand_dims(np_array, axis=expand_axis), new_shape)


def expand_canvas(img, new_shape, fill=0):
    new_img = np.full(new_shape, fill, 'uint8')
    if len(new_shape) >= 3 and new_shape[2] == 4 and fill == 0:
        new_img[:, :, 3] = 255
    place_on_center(new_img, img)
    return new_img


def ranges_to_page_set(page_ranges):
    """
    Given a list of page ranges, expand the ranges into a set of pages

    Parameters
    ----------
    page_ranges : Iterable (list or tuple)
        Iterable of page ranges. Page ranges can be a list/tuple of [start page,
        end page] or a specific page number.

    Returns
    -------
    Set of pages that are included in the provided ranges.

    """
    page_set = set()
    for page_range in page_ranges:
        if type(page_range) is int:
            page_set.add(page_range)
        elif type(page_range) in [list, tuple]:
            new_set = range(*page_range, )
            page_set.update(new_set)
            page_set.add(new_set.stop)
    return page_set


def image_to_text(img, mode="eng"):
    return pytesseract.image_to_string(
        img, lang=mode
    ).replace('\x0c', '').replace('\n', '')


def extract(pdf_path, doc_info, page_ranges=None, threads=4):
    pages = []
    # Convert to images with pdf at 200 dpi resolution
    for img in pdf_to_images(pdf_path, page_ranges, thread_count=threads):

        thresh_img = cv2.cvtColor(
            img, cv2.COLOR_RGBA2GRAY
        ) < doc_info['text_threshold']

        base = thresh_img[doc_info['table_area']]
        rows = []
        for r in range(doc_info['rows_per_page']):
            row = []
            for c in range(len(doc_info['columns'])):
                col_slice = doc_info['columns'][c]
                cell_width = col_slice.stop - col_slice.start
                cell_img = base[
                           r * doc_info['row_height']:(r + 1) * doc_info['row_height'],
                           col_slice
                           ]

                # Convert to image with black text and white background
                # (Better results from pytesseract)
                cell_img = (255 * (1 - cell_img)).astype('uint8')

                # Center image cutout on larger canvas to improve pytesseract results
                # 40 and 20 padding chosen arbitrarily
                ex_cell_img = expand_canvas(
                    cell_img, (doc_info['row_height'] + 40, cell_width + 20)
                )
                mode = doc_info.get("column_scan_mode", "eng")[c]
                text = image_to_text(ex_cell_img, mode)
                row.append(text)
            rows.append(row)
        pages.append(rows)
    return pages
