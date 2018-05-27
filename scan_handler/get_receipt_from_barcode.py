import sys
from scan_handler import models


def main():
    barcode = sys.argv[1]

    try:
        product = models.Product.objects.get(barcode=barcode)
        receipt = models.Receipt.objects.get(product=product)
        print(receipt.path)
        print("It worked!")

    except Exception as e:
        print("ERROR")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main()


# print(len(models.Product.objects.all()))
