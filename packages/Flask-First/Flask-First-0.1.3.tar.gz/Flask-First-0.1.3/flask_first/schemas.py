"""The module contains Marshmellow schemas for serializing the specification."""
from marshmallow import fields
from marshmallow import pre_load
from marshmallow import Schema
from marshmallow import validate
from marshmallow import validates_schema
from marshmallow import ValidationError

VALUE_TYPES = ['boolean', 'object', 'array', 'number', 'string', 'integer']
VALUE_FORMATS = [
    'date-time',
    'date',
    'time',
    'duration',
    'email',
    'idn-email',
    'hostname',
    'idn-hostname',
    'ipv4',
    'ipv6',
    'uri',
    'uri-reference',
    'iri',
    'iri-reference',
    'uuid',
    'uri-template',
    'json-pointer',
    'relative-json-pointer',
    'regex',
    'int32',
    'int64',
    'float',
    'double',
    'byte',
    'binary',
    'password',
]

MEDIA_TYPES = ['application/json']

PARAMETER_LOCATIONS = ['path', 'query', 'header', 'cookie']

METHODS = ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace']

# Regexp`s.
PROPERTY_NAME = r'^[a-z]{1}[a-z0-9_]+$'
PARAMETER_NAME = r'^[a-zA-Z/{}_\-0-9]+$'
ROUTE_PATH = r'^/[a-zA-Z/{}_\-0-9]+$'
RESPONSE_MEDIA_TYPE = r'^[0-9]{3}$|^default$'


def resolve_ref(ref: str, raw_spec: dict) -> dict:
    keys_from_ref = ref.split('/')[1:]

    value_from_ref = raw_spec
    for key in keys_from_ref:
        value_from_ref = value_from_ref[key]

    return value_from_ref


class BaseSchema(Schema):
    @pre_load
    def preprocess(self, data, **kwargs):
        solved_ref = self.resolve_reference(data)
        params_to_dict = self.parameters_to_dict(solved_ref)
        return params_to_dict

    def resolve_reference(self, data):
        if data.get('$ref'):
            data.update(resolve_ref(data['$ref'], self.context['raw_spec']))
            data.pop('$ref')
        return data

    def parameters_to_dict(self, data):
        if data.get('parameters'):
            parameters = {}
            for param in data['parameters']:
                self.resolve_reference(param)
                parameters[param['name']] = param
            data['parameters'] = parameters
        return data


class SchemaObjectSchema(BaseSchema):
    _type = fields.String(data_key='type', validate=validate.OneOf(VALUE_TYPES))
    example = fields.Raw()
    minimum = fields.Float(strict=True)
    maximum = fields.Float(strict=True)
    minLength = fields.Integer(strict=True, validate=validate.Range(min=0))
    maxLength = fields.Integer(strict=True, validate=validate.Range(min=0))
    format = fields.String(validate=validate.OneOf(VALUE_FORMATS))
    required = fields.List(fields.String())
    additionalProperties = fields.Boolean()
    properties = fields.Dict(
        fields.String(validate=validate.Regexp(PROPERTY_NAME)), fields.Nested('SchemaObjectSchema')
    )
    items = fields.Nested('SchemaObjectSchema')


class MediaTypeObjectSchema(BaseSchema):
    schema = fields.Nested(SchemaObjectSchema)


class ResponseObjectSchema(BaseSchema):
    description = fields.String()
    content = fields.Dict(
        fields.String(required=True, validate=validate.OneOf(MEDIA_TYPES)),
        fields.Nested(MediaTypeObjectSchema, required=True),
    )
    required = fields.Boolean()


class ParameterObjectSchema(BaseSchema):
    name = fields.String(required=True, validate=validate.Regexp(PARAMETER_NAME))
    _in = fields.String(data_key='in', required=True, validate=validate.OneOf(PARAMETER_LOCATIONS))
    description = fields.String()
    required = fields.Boolean()
    schema = fields.Nested(SchemaObjectSchema)
    reference = fields.String(data_key='$ref', load_only=True)

    @validates_schema
    def validate_required_field(self, data, **kwargs):
        if not data.get('required') and data['_in'] == 'path':
            raise ValidationError('Path parameter must be required!')


class OperationObjectSchema(BaseSchema):
    parameters = fields.Dict(fields.String(required=True), fields.Nested(ParameterObjectSchema))
    responses = fields.Dict(
        fields.String(required=True, validate=validate.Regexp(RESPONSE_MEDIA_TYPE)),
        fields.Nested(ResponseObjectSchema, required=True),
        required=True,
    )
    requestBody = fields.Nested(ResponseObjectSchema)
    operationId = fields.String(validate=validate.Regexp(PROPERTY_NAME))
    summary = fields.String()


class InfoObjectSchema(BaseSchema):
    title = fields.String(required=True)
    version = fields.String(required=True)


class OpenAPIObjectSchema(BaseSchema):
    openapi = fields.String(required=True)
    info = fields.Nested(InfoObjectSchema, required=True)
    paths = fields.Dict(
        fields.String(required=True, validate=validate.Regexp(ROUTE_PATH)),
        fields.Dict(
            fields.String(required=True, validate=validate.OneOf(METHODS)),
            fields.Nested(OperationObjectSchema, required=True),
            required=True,
        ),
        required=True,
    )
    components = fields.Raw()
