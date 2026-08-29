from jsonschema import validate


def validate_schema(response, schema: dict):
    validate(
        instance=response.json(),
        schema=schema,
    )
