import urllib.request
import urllib.request

import numpy
import zbar
from PIL import Image

# url = sys.argv[1]
url = ' https://scontent.xx.fbcdn.net/v/t1.15752-9/33994887_2106430352732952_2707800464346316800_n.jpg?_nc_cat=0&_nc_ad=z-m&_nc_cid=0&oh=c22ae3e0717ef8c085d1c10dac60a909&oe=5B8B177D'
file_name = 'tmp.jpg'
urllib.request.urlretrieve(url, file_name)

try:
    image = Image.open('./' + file_name)

    image_array = numpy.array(image.getdata(), numpy.uint8)
    scanner = zbar.Scanner()
    results = scanner.scan(image_array)

    if len(results) > 0:
        result = results[0]
        barcode = result.data.decode('utf-8')

        print(barcode)

except Exception as e:
    print("ERROR")
