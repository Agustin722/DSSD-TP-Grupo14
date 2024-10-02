from django.urls import path
from .controllers.form_controller import submit_materials

urlpatterns = [
    path('', submit_materials, name='submit-materials'),
]
