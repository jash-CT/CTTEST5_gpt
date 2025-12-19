from marshmallow import Schema, fields, validate, validates, ValidationError


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    full_name = fields.Str(required=True, validate=validate.Length(min=2, max=255))
    password = fields.Str(required=True, validate=validate.Length(min=12))

    @validates("password")
    def validate_password(self, value, **kwargs):
        # Basic complexity checks; can be expanded
        if value.islower() or value.isupper():
            raise ValidationError("Password must include mixed case letters and at least one digit/symbol.")


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
