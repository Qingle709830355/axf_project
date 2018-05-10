from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import mixins, viewsets

from index.models import MainWheel, MainNav, MainHotGoods, \
    MainShop, Goods, MainShow, UserModel,FoodType, CartModel
from index.serializers import CartSerializer
from index.filters import CartFilter


# Create your views here.
def home(request):
    if request.method == 'GET':
        wheels = MainWheel.objects.all()
        navs = MainNav.objects.all()
        hotgoods = MainHotGoods.objects.all()
        shops = MainShop.objects.all()
        shows = MainShow.objects.all()
        return render(request, 'home/home.html',
                      {'wheels': wheels,
                       'navs': navs,
                       'hotgoods': hotgoods,
                       # 'shop1': shops[0],
                       # 'shop2to3': shops[1:3],
                       # 'shop4to7': shops[3:7],
                       # 'shop8to11': shops[7:11],
                       'shops': shops,
                       'shows': shows})


def mine(request):
    """我的页面"""
    if request.method == 'GET':
        wait_pay, payed = 0, 0
        ticket = request.COOKIES.get('ticket')
        if ticket:
            users = UserModel.objects.filter(u_ticket=ticket)
            if users:
                orders = users[0].ordermodel_set.all()
                for order in orders:
                    if order.o_status == 0:
                        wait_pay += 1
                    if order.o_status == 1:
                        payed += 1
                data = {
                    'wait': wait_pay,
                    'payed': payed
                }
                return render(request, 'mine/mine.html', {'users': users[0], 'data': data})
            else:
                return render(request, 'mine/mine.html')
        else:
            return render(request, 'mine/mine.html')


def market(request):
    """闪购"""
    if request.method == 'GET':
        typeid = request.GET.get('typeid', 104749)
        type = request.GET.get('type', '0')
        childid = request.GET.get('id', '0')
        foodtypes = FoodType.objects.filter()
        user = request.user
        if childid == '0':
            goods = Goods.objects.filter(categoryid=int(typeid))
        else:
            goods = Goods.objects.filter(childcid=int(childid))
        if type != '0':
            if type == '1':
                goods = goods.order_by('productid')

            if type == '2':
                goods = goods.order_by('-productnum')

            if type == '3':
                goods = goods.order_by('-price')

            if type == '4':
                goods = goods.order_by('price')

        foodtype1 = FoodType.objects.filter(typeid=typeid)[0]
        foodchildnames = foodtype1.childtypenames
        childnames = foodchildnames.split('#')
        listnames = []
        for childname in childnames:
            dictnames = {}
            childname = childname.split(':')
            dictnames['name'] = childname[0]
            dictnames['id'] = childname[1]
            listnames.append(dictnames)
        return render(request, 'market/market.html', {'foodtypes': foodtypes,
                                                      'goods': goods,
                                                      'listnames': listnames,
                                                      'foodtype1': foodtype1,
                                                      'childid': childid,
                                                      'user': user})


def cart(request):
    """购物车"""
    if request.method == 'GET':
        user = request.user
        if user:
            user_id = user.id
            carts, total = calc_total(user_id)
        return render(request, 'cart/cart.html', {'carts': carts, 'total': total})


def calc_total(userid):
    carts = CartModel.objects.filter(user_id=userid)
    total = 0
    for cart in carts:
        if cart.is_select:
            total += (cart.goods.price * cart.c_num)
    return carts, total


class CartEditor(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):
    # 查询所有cart
    queryset = CartModel.objects.all()
    # 序列化
    serializer_class = CartSerializer
    # 过滤器
    filter_class = CartFilter


def add_cart(request):
    listdata = []

    data = {
        'msg': '请求成功！',
        'coding': 200,
    }
    if request.method == 'GET':
        carts = CartModel.objects.all()
        for cart in carts:
            dict1 = {}
            dict1['c_num'] = cart.c_num
            dict1['goods_id'] = cart.goods_id
            dict1['user_id'] = cart.user_id
            listdata.append(dict1)
        data['data'] = listdata
        return JsonResponse(data)

    if request.method == 'POST':

        user = request.user
        if user and user.id:
            goodsid = request.POST.get('goods')
            cart = CartModel.objects.filter(goods_id=goodsid, user_id=user.id).first()
            if cart:
                cart.c_num += 1
                cart.save()
            else:
                CartModel.objects.create(
                    goods_id=goodsid,
                    user_id=user.id
                )
            data['c_num'] = CartModel.objects.filter(goods_id=goodsid, user_id=user.id).first().c_num
            data['total'] = calc_total(user.id)[1]
        return JsonResponse(data)


def sub_car(request):
    if request.method == 'POST':
        data = {
            'msg': '请求成功',
            'coding': 200,
        }
        good_id = request.POST.get('goods')
        user = request.user
        if user and user.id:
            cart = CartModel.objects.filter(goods_id=good_id, user_id=user.id).first()
            if cart:
                if cart.c_num > 1:
                    cart.c_num -= 1
                    cart.save()
                    data['c_num'] = cart.c_num
                else:
                    cart.delete()
                    data['c_num'] = 0
        return JsonResponse(data)


def change_cart_status(request):
    if request.method == 'POST':
        data = {
            'msg': '请求成功！',
            'coding': 200,
        }
        id = request.POST.get('id')
        user = request.user
        if user and user.id:
            cart = CartModel.objects.get(id=id)
            cart.is_select = not cart.is_select
            cart.save()
            data['is_select'] = cart.is_select
        return JsonResponse(data)




