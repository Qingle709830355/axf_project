from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from index import views

router = SimpleRouter()
router.register('shopcar', views.CartEditor)


urlpatterns = [
    url(r'home/', views.home, name='home'),
    url(r'market/', views.market, name='market'),
    url(r'cart/', views.cart, name='cart'),
    url(r'mine/', views.mine, name='mine'),
    url(r'addcar/', views.add_cart),
    url(r'subcar/', views.sub_car),
    url(r'changecartstatus/', views.change_cart_status)
] + router.urls