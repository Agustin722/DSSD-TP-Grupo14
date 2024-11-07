from django.urls import path
from .controllers.form_controller import submit_materials, pago_pendiente
from .controllers.login_controller import login_view
from . import views

urlpatterns = [
    path('', login_view, name='login'),
    path('ingresar-materiales/', submit_materials, name='submit-materials'),
    path('pago-pendiente/', pago_pendiente, name='pago-pendiente'),
    path('create_order/', views.create_order, name='create_order'),
    path('reserve_order/<int:order_id>/', views.reserve_order, name='reserve_order'),
    path('deliver_order/<int:order_id>/', views.deliver_order, name='deliver_order'),
    path('register_user/', views.register_user, name='register_user'),
    path('login-api/', views.login_api, name='login_api'),
    path('order_list/', views.order_list, name='order_list'),
    path('material_list/', views.material_list, name='material_list'),
]
