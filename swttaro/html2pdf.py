import datetime
import os

import pdfkit


def html2pdf(html, save_path, from_url=None, extra_options=None):
    options = {
        'page-size': 'A4',
        'margin-top': '0.6in',
        'margin-right': '0.6in',
        'margin-bottom': '0.6in',
        'margin-left': '0.6in',
        'encoding': "UTF-8",
        'quiet': '',
    }
    options.update(extra_options)
    # save_path will error if it is not English, use temp_path and rename
    temp_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + '.pdf'
    temp_dir = os.path.split(save_path)[0]
    temp_path = os.path.join(temp_dir, temp_name)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    if from_url:
        pdfkit.from_url(from_url, temp_path, options=options)
    else:
        pdfkit.from_string(html, temp_path, options=options)

    os.rename(temp_path, save_path)
