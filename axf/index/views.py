from django.shortcuts import render
from index.models import MainWheel, MainNav, MainHotGoods, MainShop, Goods, MainShow


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
                       'shop1': shops[0],
                       'shop2to3': shops[1:3],
                       'shop4to7': shops[3:7],
                       'shop8to11': shops[7:11],
                       'shows': shows})


def mine(request):
    """我的页面"""
    if request.method == 'GET':
        return render(request, 'mine/mine.html')


def market(request):
    """闪购"""
    if request.method == 'GET':
        return render(request, 'market/market.html')


def cart(request):
    """购物车"""
    if request.method == 'GET':
        return render(request, 'cart/cart.html')