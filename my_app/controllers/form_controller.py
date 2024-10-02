from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from my_app.schemas.form_schema import MaterialFormSchema
from my_app.models.material import Formulario, Material
from my_app.api.bonita_api import start_bonita_process
from marshmallow import ValidationError

def submit_materials(request):
    if request.method == 'POST':
        form_data = {
            'materiales': []
        }
        
        # Extraer datos del formulario
        tipos = request.POST.getlist('tipo_material')
        cantidades = request.POST.getlist('cantidad')
        
        for tipo, cantidad in zip(tipos, cantidades):
            if tipo and cantidad:
                form_data['materiales'].append({
                    'tipo_material': tipo,
                    'cantidad': int(cantidad)
                })
        
        # Validar datos con Marshmallow
        schema = MaterialFormSchema()
        try:
            validated_data = schema.load(form_data)
        except ValidationError as err:
            messages.error(request, f"Errores de validación: {err.messages}")
            return render(request, 'form.html')
        
        # Guardar en la base de datos
        formulario = Formulario.objects.create()
        for material in validated_data['materiales']:
            Material.objects.create(
                formulario=formulario,
                tipo_material=material['tipo_material'],
                cantidad=material['cantidad']
            )
        
        # Iniciar proceso en Bonita
        process_definition_id = getattr(settings, 'BONITA_PROCESS_DEFINITION_ID', '<tu-processDefinitionId>')
        try:
            start_bonita_process(process_definition_id, validated_data['materiales'])
            messages.success(request, "Materiales enviados e instancia de proceso creada correctamente.")
        except Exception as e:
            messages.error(request, f"Error al iniciar el proceso en Bonita: {str(e)}")
        
        return redirect('submit-materials')
    
    return render(request, 'form.html')
