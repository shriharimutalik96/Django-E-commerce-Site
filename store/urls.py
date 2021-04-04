from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns=[

  path('',views.store,name='store'), #home_ page
  path('cart/',views.cart,name='cart'),
  path('checkout/',views.checkout,name='checkout'),
  path('update_item/',views.updateitem,name='update_item'),
  path('process_order/',views.processOrder,name='process_order'),
  path('login/',LoginView.as_view(template_name='store/login.html'),name='login'), # Class Based View

    ]


