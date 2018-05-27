import sys
import numpy
import zbar
import zbar.misc
from PIL import Image


def main():
    image_path = sys.argv[1]

    try:
        image = Image.open(image_path)

        image_array = numpy.array(image.getdata(), numpy.uint8)
        scanner = zbar.Scanner()
        results = scanner.scan(image_array)

        if len(results) > 0:
            result = results[0]
            barcode = result.data.decode('utf-8')

            print(barcode)
        else:
            raise Exception

    except Exception as e:
        print("ERROR")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main()
