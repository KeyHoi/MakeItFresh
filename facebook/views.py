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

    # just sebhook subscriptions
    if request.method == 'GET':
        VERIFY_TOKEN = "3153b67bfc6c51a17fd558976844c6bf"

        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode is None or token is None or challenge is None:
            return HttpResponse(status=404)
        elif mode == 'subscribe' and token == VERIFY_TOKEN:
            print("WEBHOOK VERIFIED")
            return HttpResponse(status=200, content=challenge)
        else:
            return HttpResponse(status=403)

    # POST request -> webhook event
    else:
        body = request.body.decode('utf-8')
        body = json.loads(body)

        if body.get('object', '') == 'page':
            for entry in body.get('entry', []):
                for webhook_event in entry.get('messaging',[]):
                    print('Webhook Event: \n{}'.format(webhook_event))

                    source_id = webhook_event.get('sender', {}).get('id', '-1')
                    if source_id != -1:

                        message = webhook_event.get('message', None)
                        if message is not None:     # check if message

                            msg = ''
                            api_url = c.FB_SEND_API_URL

                            attachments = message.get('attachments', None)
                            if attachments is not None and len(attachments) > 0:    # check for attachements

                                for att in attachments:     # check every attachement
                                    if att['type'] == 'image':

                                        image_url = att['payload']['url']
                                        barcode = scan(image_url)
                                        if barcode is not None and barcode != -1:   # check if scan was successful

                                            try:    # barcode is in DB
                                                product = Product.objects.get(barcode=barcode)
                                                receipt = Receipt.objects.get(product=product)
                                                receipt_json = receipt.receipt

                                                msg = str(receipt_json['header']) + '\n\n'
                                                for par in receipt_json['paragraphs']:
                                                    msg += par + '\n'

                                                print("=======================")
                                                if int(barcode) == 8076800195033:
                                                    print("IMAGE SENDING")
                                                    res = requests.post(api_url, json={
                                                        "recipient": {
                                                            "id": source_id
                                                        },
                                                        "message": {
                                                            "attachment": {
                                                                "type": "image",
                                                                "payload": {
                                                                    "url": "https://static.chefkoch-cdn.de/ck.de/rezepte/132/132850/1110326-420x280-fix-spaghetti-bolognese.jpg",
                                                                    "is_reusable": "true"
                                                                }
                                                            }
                                                        }
                                                    })

                                            except Exception as e:
                                                print(e)
                                                msg = c.LIMITED_DB
                                        else:
                                            msg = c.BETTER_IMG
                                    else:
                                        msg = c.JUST_IMG_MSG
                            else:
                                msg = c.JUST_IMG_MSG

                            print("Message: {}\n".format(msg))

                            res = requests.post(api_url, json={
                                "recipient": {
                                    "id": source_id
                                },
                                "message": {
                                    "text": msg
                                }
                            })

                            return HttpResponse(status=res.status_code)

        return HttpResponse(status=404)
