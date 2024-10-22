from marshmallow import Schema, fields, validates, ValidationError

class LoginSchema(Schema):
    dni = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates('dni')
    def validate_dni(self, value):
        if not value.isdigit():
            raise ValidationError("El DNI debe contener solo números.")
login_schema = LoginSchema()