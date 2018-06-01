import urllib.request
import urllib.request

import numpy
import zbar
from PIL import Image


def scan(url, queue):
    file_path = './tmp.jpg'

    try:
        print("Downloading image temporarily")
        urllib.request.urlretrieve(url, file_path)
        image = Image.open(file_path)

        print("Start scanning")
        image_array = numpy.array(image.getdata(), numpy.uint8)
        scanner = zbar.Scanner()

        results = scanner.scan(image_array)
        print("Finished scanning")

        if len(results) > 0:
            result = results[0]
            barcode = result.data.decode('utf-8')
            queue.put(barcode)

            return True

    except Exception as e:
        print("ERROR while scanning image")
