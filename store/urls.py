
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('store',views.storeViewSet)
urlpatterns = [
        #Leave as empty string for base url
    path('',include(router.urls)),
    path('',views.store, name="store"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('update_item/',views.updateItem, name="update_item"),
    path('process_order/',views.processOrder, name="process_order"),
    path('register/',views.registerPage, name="register"),
    path('login/',views.loginPage, name="login"),
    path('main/',views.main, name="main"),
    path('logout/',views.logoutUser, name="logout"),
    path('order_history/',views.orderHistory, name="order_history"),
    path('my_orders/<int:id>',views.my_orders, name="my_orders"),
    path('product_detail/<int:id>',views.product_detail, name="product_detail"),
   
]































