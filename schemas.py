from marshmallow import Schema, fields, validate

class CCHSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required=True,validate=validate.Length(min=1,max=20))
    request = fields.Str(required=True,unique=False)
    response = fields.Str(required=True,unique=False)

class DocumentSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required=True,validate=validate.Length(min=1,max=20)) 

