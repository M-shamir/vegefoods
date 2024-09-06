from django.urls import path
from . import views

urlpatterns = [
    path('',views.view_wishlist,name='view_wishlist'),
    path('add/<int:product_id>/',views.add_to_wishlist,name='add_wishlist'),
    path('remove/<int:product_id>/',views.remove_wishlist,name='remove_wishlist'),

    ]