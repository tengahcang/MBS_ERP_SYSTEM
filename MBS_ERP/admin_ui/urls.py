from django.urls import path
from . import views

app_name = "admin_ui"

urlpatterns = [
    # URL Asli: http://localhost:8000/sales/
    path('', views.dashboard, name='dashboard'), 

    # URL Asli: http://localhost:8000/sales/users/
    path('users/', views.user_list, name='user_list'),
    
    path('products/', views.product_list, name='product_list'),
]