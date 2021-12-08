from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt

from .models import Buy,Pay,Products,State,User
# Create your views here.
@csrf_exempt
def menu(request):
    menu1 = Products.objects.filter(kind=1)
    menu2 = Products.objects.filter(kind=2)
    menu3 = Products.objects.filter(kind=3)
    menu4 = Products.objects.filter(kind=4)
    return render(request,'menu.html',locals())

@csrf_exempt
def homepage(request):
    return render(request, 'homepage.html', locals())

@csrf_exempt
def register(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        name = request.POST.get("name")
        if User.objects.filter(phone=phone).exists():   #查詢此手機號碼是否存在於資料庫
            return render(request, 'register_fail.html', locals())
        if name == "":
            return render(request, 'register_fail2.html', locals())
        user = User.objects.create(phone=phone,name=name)
        user.save()
    return render(request, 'register.html', locals())

@csrf_exempt
def order(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        if User.objects.filter(phone=phone).exists():
            pay_number=1
            while Pay.objects.filter(pay_number=pay_number).exists():
                pay_number += 1
            quantity1 = request.POST.get("quantity1")
            quantity2 = request.POST.get("quantity2")
            quantity3 = request.POST.get("quantity3")
            quantity4 = request.POST.get("quantity4")
            quantity5 = request.POST.get("quantity5")
            quantity6 = request.POST.get("quantity6")
            quantity7 = request.POST.get("quantity7")
            quantity8 = request.POST.get("quantity8")
            quantity9 = request.POST.get("quantity9")
            quantity10 = request.POST.get("quantity10")
            quantity11 = request.POST.get("quantity11")
            total = 0
            if quantity1 != "0":
                total += 30*int(quantity1)
            if quantity2 != "0":
                total += 30*int(quantity2)
            if quantity3 != "0":
                total += 35*int(quantity3)
            if quantity4 != "0":
                total += 35*int(quantity4)
            if quantity5 != "0":
                total += 25*int(quantity5)
            if quantity6 != "0":
                total += 15*int(quantity6)
            if quantity7 != "0":
                total += 15*int(quantity7)
            if quantity8 != "0":
                total += 15*int(quantity8)
            if quantity9 != "0":
                total += 20*int(quantity9)
            if quantity10 != "0":
                total += 30*int(quantity10)
            if quantity11 != "0":
                total += 15*int(quantity11)
            if total == 0:
                return render(request, 'order_fail2.html', locals())
            buy_user = User.objects.get(phone=phone)
            state = State.objects.get(state_number=1)
            pay = Pay.objects.create(pay_phone=buy_user,pay_number=pay_number,total_price=total,state=state)
            pay.save()
            if quantity1 != "0":
                food1 = Products.objects.get(product="培根蛋餅")
                buy1 = Buy.objects.create(phone = buy_user,buy_product=food1,quantity=quantity1
                                          ,buy_price=30*int(quantity1),pay_number=pay)
                buy1.save()
            if quantity2 != "0":
                food2 = Products.objects.get(product="火腿蛋餅")
                buy2 = Buy.objects.create(phone = buy_user,buy_product=food2, quantity=quantity2
                                          , buy_price=30 * int(quantity2), pay_number=pay)
                buy2.save()
            if quantity3 != "0":
                food3 = Products.objects.get(product="培根蛋三明治")
                buy3 = Buy.objects.create(phone = buy_user,buy_product=food3, quantity=quantity3
                                          , buy_price=35 * int(quantity3), pay_number=pay)
                buy3.save()
            if quantity4 != "0":
                food4 = Products.objects.get(product="火腿蛋三明治")
                buy4 = Buy.objects.create(phone = buy_user,buy_product=food4, quantity=quantity4
                                          , buy_price=35 * int(quantity4), pay_number=pay)
                buy4.save()
            if quantity5 != "0":
                food5 = Products.objects.get(product="奶茶")
                buy5 = Buy.objects.create(phone = buy_user,buy_product=food5, quantity=quantity5
                                          , buy_price=25 * int(quantity5), pay_number=pay)
                buy5.save()
            if quantity6 != "0":
                food6 = Products.objects.get(product="紅茶")
                buy6 = Buy.objects.create(phone = buy_user,buy_product=food6, quantity=quantity6
                                          , buy_price=15 * int(quantity6), pay_number=pay)
                buy6.save()
            if quantity7 != "0":
                food7 = Products.objects.get(product="綠茶")
                buy7 = Buy.objects.create(phone = buy_user,buy_product=food7, quantity=quantity7
                                          , buy_price=15 * int(quantity7), pay_number=pay)
                buy7.save()
            if quantity8 != "0":
                food8 = Products.objects.get(product="豆漿")
                buy8 = Buy.objects.create(phone = buy_user,buy_product=food8, quantity=quantity8
                                          , buy_price=15 * int(quantity8), pay_number=pay)
                buy8.save()
            if quantity9 != "0":
                food9 = Products.objects.get(product="小熱狗")
                buy9 = Buy.objects.create(phone = buy_user,buy_product=food9, quantity=quantity9
                                          , buy_price=20 * int(quantity9), pay_number=pay)
                buy9.save()
            if quantity10 != "0":
                food10 = Products.objects.get(product="薯條")
                buy10 = Buy.objects.create(phone = buy_user,buy_product=food10, quantity=quantity10
                                          , buy_price=30 * int(quantity10), pay_number=pay)
                buy10.save()
            if quantity11 != "0":
                food11 = Products.objects.get(product="薯餅")
                buy11 = Buy.objects.create(phone = buy_user,buy_product=food11, quantity=quantity11
                                          , buy_price=15 * int(quantity11), pay_number=pay)
                buy11.save()
            result_buy = Buy.objects.filter(phone=phone, pay_number=pay_number)
            result_pay = Pay.objects.filter(pay_phone=phone, pay_number=pay_number)
            result_user = User.objects.filter(phone=phone)
            return render(request, 'search_result2.html', locals())
        else:
            return render(request, 'order_fail1.html', locals())
    menu1 = Products.objects.filter(kind=1)
    menu2 = Products.objects.filter(kind=2)
    menu3 = Products.objects.filter(kind=3)
    menu4 = Products.objects.filter(kind=4)
    return render(request, 'order.html', locals())

@csrf_exempt
def search(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        number = request.POST.get("number")
        if phone is "":     #django會收到""而不是null
            return render(request, 'search_fail.html', locals())
        if User.objects.filter(phone=phone).exists():
            if Pay.objects.filter(pay_phone=phone).exists():
                if number is "":
                    result_buy = Buy.objects.filter(phone=phone)
                    result_pay = Pay.objects.filter(pay_phone=phone)
                    result_user = User.objects.filter(phone=phone)
                    return render(request, 'search_result.html', locals())
                else:
                    if Buy.objects.filter(phone=phone,pay_number=number).exists():
                        result_buy = Buy.objects.filter(phone=phone,pay_number=number)
                        result_pay = Pay.objects.filter(pay_phone=phone,pay_number=number)
                        result_user = User.objects.filter(phone=phone)
                        return render(request, 'search_result2.html', locals())
                    else:
                        return render(request, 'search_fail2.html', locals())
    return render(request, 'search.html', locals())
