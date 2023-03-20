from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsViewset.as_view({'get':'list'})),
    path('menu-items/<int:pk>', views.MenuItemsViewset.as_view({'get':'retrieve'})),
    path('menu', views.menu),
    path('category/<int:pk>', views.category_detail, name='category-detail'),
    path('welcome', views.welcome),
]
