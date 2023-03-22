from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsViewset.as_view({'get':'list'})),
    path('menu-items/<int:pk>', views.MenuItemsViewset.as_view({'get':'retrieve'})),
    path('menu', views.menu),
    path('category/<int:pk>', views.category_detail, name='category-detail'),
    path('welcome', views.welcome),
    path('secret/', views.secret),
    path('api-token-auth/', obtain_auth_token),
]
