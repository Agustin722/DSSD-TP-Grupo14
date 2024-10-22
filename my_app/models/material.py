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
    
    def clean(self):
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")

    def save(self, *args, **kwargs):
        """
        Realiza una limpieza previa de los datos y luego delega en el save de la clase padre
        para que realice la operacion de guardado en la base de datos.

        El save de la clase padre es el que se encarga de realmente persistir en la
        base de datos los cambios realizados en el objeto.
        """
        self.clean()
        super().save(*args, **kwargs)