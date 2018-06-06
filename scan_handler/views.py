import json

import constants as c
from . import models

from django.template import loader
from django.http import HttpResponse


def get_scanner_template(request):
    template = loader.get_template('scan_handler/scanner.html')
    return HttpResponse(template.render())


def get_receipts_from_json_new(json_file):
    """
    @:param json_file file with json content
    one receipt json format
    json_file can contain array of receipts in this format [{...}, {...}, {...}]
    {
        "recipe_name": "<RECIPE_NAME>",
        "ingredients": [],
        "preparation": [],
        "others": [],
        "recipe_image_url": "<IMAGE_URL>",
        "url": "<URL>",
        ("barcode": "<BARCODE>")
    }
    """
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
                print("{\n\"recipe_name\": \"<RECIPE_NAME>\",\n" \
                      "\"ingredients\": [],\n" \
                      "\"preparation\": [],\n" \
                      "\"others\": [],\n" \
                      "{\n\"recipe_image_url\": \"<IMAGE_URL>\",\n" \
                      "(\"barcode\": \"<BARCODE>\")")
                print("JSON Array of valid receipts is also valid")
        except Exception as e:
            print(e)


def add_receipt_with_product_new(json_dict):
    recipe_name = json_dict.get('recipe_name', '')
    ingredients = json_dict.get('ingredients', [])
    preparation = json_dict.get('preparation', [])
    others = json_dict.get('others', [])
    recipe_image_url = json_dict.get('image_url', None)
    barcode = json_dict.get('barcode', None)

    product = None
    try:
        product = models.Product.objects.get(barcode=barcode)
    except Exception as e:
        pass

    recipe = models.Recipe(recipe_name=recipe_name, ingredients=ingredients, preparation=preparation, others=others,
                           recipe_image_url=recipe_image_url)
    recipe.save()

    recipe.recipe_url = c.RECEIPT_BASE_URL + str(recipe.id) + "/"
    recipe.save()


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
    pass
