import os
import urllib.request
import urllib.request

import numpy
import zbar
from PIL import Image


def scan(url):
    file_path = './tmp.jpg'

    try:
        urllib.request.urlretrieve(url, file_path)
        image = Image.open(file_path)

        image_array = numpy.array(image.getdata(), numpy.uint8)
        scanner = zbar.Scanner()
        results = scanner.scan(image_array)

        if len(results) > 0:
            result = results[0]
            barcode = result.data.decode('utf-8')

            return barcode

    except Exception as e:
        print("ERROR")
