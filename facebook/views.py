import json
import requests
import constants as c
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from scan_handler.scan_barcode import scan
from scan_handler.models import Product, Receipt


@csrf_exempt
def connection_handler(request):
    body = request.body.decode('utf-8')
    body = json.loads(body)
    print(body)

    if request.method == 'GET':
        VERIFY_TOKEN = "3153b67bfc6c51a17fd558976844c6bf"

        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        print(mode)
        print(token)
        print(challenge)

        assert mode is not None
        assert token is not None

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("WEBHOOK VERIFIED")
            return HttpResponse(status=200, content=challenge)

    if body['object'] == 'page':
        for entry in body['entry']:
            for webhook_event in entry['messaging']:

                print(webhook_event)

                source_id = webhook_event['sender']['id']
                message = webhook_event['message']

                if message is not None:
                    attachments = message['attachments']

                    print(message)

                    if attachments is not None:
                        for att in attachments:
                            if att['type'] == 'image':
                                image_url = att['payload']['url']
                                barcode = scan(image_url)

                                product = Product.objects.get(barcode=barcode)
                                assert product is not None

                                receipt = Receipt.objects.get(product=product)
                                assert Receipt is not None

                                receipt_json = receipt.receipt
                                print(receipt_json)

                                msg = str(receipt_json['header']) + '\n\n'
                                for par in receipt_json['paragraphs']:
                                    msg += par + '\n'

                                print(msg)

                                url = c.FB_SEND_API_URL
                                res = requests.post(url, json={
                                    "recipient": {
                                        "id": source_id
                                    },
                                    "message": {
                                        "text": message
                                    }
                                })

                                assert res.status_code == 200

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)
