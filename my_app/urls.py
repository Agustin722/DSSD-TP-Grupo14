from django.urls import path
from .controllers.form_controller import submit_materials, pago_pendiente
from .controllers.login_controller import login_view

urlpatterns = [
    path('', login_view, name='login'),
    path('ingresar-materiales/', submit_materials, name='submit-materials'),
    path('pago-pendiente/', pago_pendiente, name='pago-pendiente')
]
