import json

import constants as c
from . import models

from django.http import HttpResponse


def get_receipts_from_json(json_file):
    """
    @:param json_file file with json content
    one receipt json format
    json_file can contain array of receipts in this format [{...}, {...}, {...}]
    {
        "header": "<HEADER>",
        "ingredients": [],
        "url": "<URL>",
        "paragraphs": [],
        ("barcode": "<BARCODE>")
    }
    """
    # json_file = open('/home/keyhoi/test.txt', 'r')  # TODO connect to admin page
    file_dict = None

    try:
        file_dict = json.load(json_file)
    except Exception as e:
        print(e)
    finally:
        try:
            if file_dict is None:
                for line in json_file:
                    file_dict = json.loads(line)
                    add_receipt_with_product(file_dict)
            elif isinstance(file_dict, list):
                for it_dict in file_dict:
                    add_receipt_with_product(it_dict)
            elif isinstance(file_dict, dict):
                add_receipt_with_product(file_dict)
            else:
                print("Not even close to valid json!")
                print("valid format of one receipt")
                print("{\n\"header\": \"<HEADER>\",\n" \
                      "\"ingredients\": [],\n" \
                      "\"paragraphs\": [],\n" \
                      "(\"barcode\": \"<BARCODE>\")")
                print("JSON Array of valid receipts is also valid")
        except Exception as e:
            print(e)


def add_receipt_with_product(json_dict):
    header = json_dict.get('header', '')
    ingredients = json_dict.get('ingredients', [])
    paragraphs = json_dict.get('paragraphs', [])
    barcode = json_dict.get('barcode', None)

    product = None
    try:
        product = models.Product.objects.get(barcode=barcode)
    except Exception as e:
        pass

    receipt = models.Receipt(header=header, ingredients=ingredients, paragraphs=paragraphs,
                             product=product)  # TODO change model
    receipt.save()

    receipt.url = c.RECEIPT_BASE_URL + str(receipt.id) + "/"
    receipt.save()


def get_receipt_template(request, id=-1):
    if id == -1:
        return HttpResponse(status=404)
    else:
        header = ''
        ingredients = []
        paragraphs = []

        try:
            receipt = models.ReceiptNew.objects.get(id=id)
            header = receipt.header
            ingredients = receipt.ingredients
            paragraphs = receipt.paragraphs
        except Exception as e:
            print(e)
        # TODO load receipt in template
        # TODO load HTML template + css stylesheet
        # TODO return template + HTTP response

        return HttpResponse(status=200)

