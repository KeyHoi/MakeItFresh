import json

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import constants as c
from scan_handler.models import Product, Receipt
from scan_handler.scan_barcode import scan


@csrf_exempt
def connection_handler(request):
    print("connection handler triggered")
    if request.method == 'GET':
        VERIFY_TOKEN = "3153b67bfc6c51a17fd558976844c6bf"

        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        assert mode is not None
        assert token is not None

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("WEBHOOK VERIFIED")
            return HttpResponse(status=200, content=challenge)
    else:
        body = request.body.decode('utf-8')
        body = json.loads(body)

        if body['object'] == 'page':
            for entry in body['entry']:
                for webhook_event in entry['messaging']:

                    print('Webhook Event: \n{}'.format(webhook_event))

                    source_id = webhook_event['sender']['id']
                    message = webhook_event.get('message', None)

                    if message is not None:
                        attachments = message.get('attachments', None)

                        if attachments is not None:
                            for att in attachments:
                                if att['type'] == 'image':
                                    image_url = att['payload']['url']
                                    # barcode = scan(image_url)
                                    barcode = 4029764001807
                                    print("Scanned barcode: {}".format(barcode))

                                    try:
                                        product = Product.objects.get(barcode=barcode)

                                        receipt = Receipt.objects.get(product=product)

                                        receipt_json = receipt.receipt
                                        print("Receipt: \n{}".format(receipt_json))

                                        msg = str(receipt_json['header']) + '\n\n'
                                        for par in receipt_json['paragraphs']:
                                            msg += par + '\n'

                                        print("Message: {}\n".format(msg))

                                        url = c.FB_SEND_API_URL
                                        res = requests.post(url, json={
                                            "recipient": {
                                                "id": source_id
                                            },
                                            "message": {
                                                "text": msg
                                            }
                                        })

                                        assert res.status_code == 200
                                    except Exception as e:
                                        print(e)

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)


@csrf_exempt
def http_get_handler(request, mode, token, challenge):
    print('{}\n{}\n{}'.format(mode, token, challenge))
    assert mode is not None
    assert token is not None

    VERIFY_TOKEN = "3153b67bfc6c51a17fd558976844c6bf"

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED")
        return HttpResponse(status=200, content=challenge)


@csrf_exempt
def test(request):
    print("HELLO WORLD")
    return HttpResponse(status=200)