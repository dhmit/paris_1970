import tempfile
from io import StringIO
import jovian
import tabula
import camelot
import pandas as pd
import numpy as np
import pdftotext
from PIL import Image, ImageFont, ImageDraw
from pdf2image import convert_from_path
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import dataframe_image as dfi
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from django.conf import settings
import os

pd.set_option('display.max_colwidth', None)
PDF = os.path.join(settings.ANALYSIS_DIR, 'A_09.pdf')
pdf_img = convert_from_path(PDF, dpi=300)[0]

plt.figure(figsize=(15, 10))
plt.axis('off')
plt.imshow(pdf_img)

def make_df_image(table,
                  max_cols=-1,
                  max_rows=-1):
    """Return dataframe as image."""
    with tempfile.NamedTemporaryFile(suffix='.jpg',
                                     delete=False) as tmp:
        dfi.export(table, tmp.name, max_cols=max_cols, max_rows=max_rows)
        image = mpimg.imread(tmp.name)
        return image


def make_lines_image(lines,
                     mrgn=15,
                     background=(255, 255, 255),
                     text_color=(0, 0, 0),
                     font_size=8):
    """Return raw text in lines as image."""
    lines = pd.Series(lines)
    longest_line = lines[lines.str.len().idxmax()]
    image = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(image)
    monospace = ImageFont.truetype(r'С:\Windows\Fonts\cour.ttf', font_size)
    line_width, line_height = draw.textsize(longest_line, monospace)
    img_width, img_height = (line_width + mrgn * 2,
                             len(lines) * line_height + mrgn * 2)
    image = Image.new("RGBA", (img_width, img_height), background)
    draw = ImageDraw.Draw(image)
    x, y0 = (mrgn, mrgn)
    for n, line in enumerate(lines):
        y = y0 + n * line_height
        draw.text((x, y), line, text_color, monospace)
    return image

def camelot_table():
    camelot_df = (camelot
                  .read_pdf(PDF,
                            flavor="stream",
                            suppress_stdout=True,
                            pages="7-48")
                  )
    return camelot_df

#fig, ax = plt.subplots(2, 1, figsize=(10, 15))
#titles = ['tabula 2.2.0', 'camelot 0.8.2']
#for i, img in enumerate(map(make_df_image, [tabula_df, camelot_df])):
#    ax[i].axis("off")
#    ax[i].set_adjustable("box")
#    ax[i].title.set_text(titles[i])
#    ax[i].imshow(img)
#fig.tight_layout()
