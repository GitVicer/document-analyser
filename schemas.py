from marshmallow import Schema, fields, validate

from marshmallow import Schema, fields, validate

class DocumentTypeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str()

class KeywordSchema(Schema):
    id = fields.Int(dump_only=True)
    keyword = fields.Str(required=True)
    document_type_id = fields.Int(required=True)

class UploadedDocumentSchema(Schema):
    id = fields.Int(dump_only=True)
    filename = fields.Str(required=True)
    document_text = fields.Str()
    document_type_id = fields.Int(required=True)

