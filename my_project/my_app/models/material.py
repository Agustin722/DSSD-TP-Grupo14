from django.db import models

class Formulario(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Formulario {self.id} - {self.fecha}"

class Material(models.Model):
    TIPO_MATERIAL_CHOICES = [
        ('plastico', 'Plástico'),
        ('papel', 'Papel'),
        ('vidrio', 'Vidrio'),
        ('metal', 'Metal'),
        ('organico', 'Orgánico'),
    ]

    formulario = models.ForeignKey(Formulario, related_name='materiales', on_delete=models.CASCADE)
    tipo_material = models.CharField(max_length=50, choices=TIPO_MATERIAL_CHOICES)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.tipo_material} - {self.cantidad}"
