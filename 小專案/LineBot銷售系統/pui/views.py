from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from .models import products,shopping_cart2

from django.views.decorators.csrf import csrf_exempt

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

@csrf_exempt
def viewer_use(request): #訂單系統
    toast = products.objects.filter(kind="吐司")
    ch = products.objects.filter(kind="蛋餅")
    drink = products.objects.filter(kind="飲料")
    return render(request, 'viewer_use.html',locals())

@csrf_exempt
def view(request):#歷史紀錄
    if request.method == 'POST':
        toast = request.POST.get("toast_name")
        toast_quantity = request.POST.get("toast_quantity")
        egg_pancake = request.POST.get("egg_pancake_name")
        egg_pancake_quantity = request.POST.get("egg_pancake_quantity")
        drink = request.POST.get("drink_name")
        drink_quantity = request.POST.get("drink_quantity")
        username = request.POST.get("user_name")
        phone = request.POST.get("phone")

        buy = toast +","+ egg_pancake +","+ drink
        quantity = toast_quantity +","+ egg_pancake_quantity +","+ drink_quantity
        total = 0
        if (toast != "無"):
            total += products.objects.get(products=toast).price * int(toast_quantity)
        if (egg_pancake != "無"):
            total += products.objects.get(products=egg_pancake).price * int(egg_pancake_quantity)
        if (drink != "無"):
            total += products.objects.get(products=drink).price * int(drink_quantity)
        if (toast != "無" or egg_pancake != "無" or drink != "無"):
            order = shopping_cart2.objects.create(name=username,phone=phone,buy_product=buy,buy_quantity=quantity,total_price=total)
            order.save()
            list_history = shopping_cart2.objects.filter(phone=phone)
            return render(request, 'view.html',locals())
        else:
            toast = products.objects.filter(kind="吐司")
            ch = products.objects.filter(kind="蛋餅")
            drink = products.objects.filter(kind="飲料")
            return render(request, 'viewer_use.html', locals())

@csrf_exempt
def search_history(request):#查詢
    if request.method == 'POST':
        phone = request.POST.get("phone")
        if shopping_cart2.objects.filter(phone=phone).exists():  #查詢此手機號碼是否存在於資料庫
            list_history = shopping_cart2.objects.filter(phone=phone)
            return render(request, 'view.html', locals())
        else:
            return render(request, 'search_history.html', locals())
    else:
        return render(request, 'search_history.html', locals())

def menu(request):#菜單
    menu_toast = products.objects.filter(kind="吐司")
    menu_egg_pancake = products.objects.filter(kind="蛋餅")
    menu_drink = products.objects.filter(kind="飲料")
    return render(request, 'menu.html', locals())