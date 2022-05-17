from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from orders.mutation import client
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def payment_capture(request):
    if request.method == 'POST':
        webhook_secret = 'rajesh'
        signature = request.headers.get('X-Razorpay-Signature')
        data = json.dumps(json.loads(request.body), separators=(',', ':'))
        print('webhook bef')
        print(data)
        print('webhook after')
        verify = client.utility.verify_webhook_signature(data, signature, webhook_secret)
        if verify:
            print(data)
            return JsonResponse(data)
        return HttpResponse("Payment Capture Failed.")
    return HttpResponse("Method is Get")
