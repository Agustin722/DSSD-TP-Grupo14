from marshmallow import Schema, fields, validate, ValidationError

class MaterialItemSchema(Schema):
    tipo_material = fields.Str(required=True, validate=validate.OneOf([
        'plastico', 'papel', 'vidrio', 'metal', 'organico'
    ]))
    cantidad = fields.Int(required=True, validate=validate.Range(min=1))

class MaterialFormSchema(Schema):
    materiales = fields.List(fields.Nested(MaterialItemSchema), required=True, validate=validate.Length(min=1))
