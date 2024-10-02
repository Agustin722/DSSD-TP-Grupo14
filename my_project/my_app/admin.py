from django.contrib import admin
from .models.material import Formulario, Material

class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1

class FormularioAdmin(admin.ModelAdmin):
    inlines = [MaterialInline]

admin.site.register(Formulario, FormularioAdmin)
