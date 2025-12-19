from marshmallow import Schema, fields, validate


class LoanApplySchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(min=100.0))
    income = fields.Float(required=True, validate=validate.Range(min=0.0))
    credit_score = fields.Integer(required=True, validate=validate.Range(min=300, max=850))
    purpose = fields.Str(required=False, validate=validate.Length(max=255))


class LoanResponseSchema(Schema):
    id = fields.Int()
    amount = fields.Float()
    income = fields.Float()
    credit_score = fields.Int()
    purpose = fields.Str()
    status = fields.Str()
    risk_score = fields.Int(allow_none=True)
    created_at = fields.DateTime()
