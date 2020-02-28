from dos import prop
from dos.schema import Fields


class DogFields(Fields):
    base_schema = {
        "name": prop.String("The dog's name."),
        "breed": prop.String("The dog's breed.")
    }

    def __init__(self):
        super().__init__(self.base_schema)


class CatFields(Fields):
    base_schema = {
        "name": prop.String("The cat's name."),
        "breed": prop.String("The cat's breed."),
        "color": prop.String("The cat's color.")
    }

    def __init__(self):
        super().__init__(self.base_schema)


class ErrorFields(Fields):
    base_schema = {
        "message": prop.String("The error message.")
    }

    def __init__(self, validated_fields=None):
        if validated_fields is not None:
            fields = {}

            for field in validated_fields:
                fields[field] = prop.String(f"A error message specific to the {field} field.")

            self.base_schema["field_error_messages"] = prop.Object(structure=fields, required=False, nullable=True)

        super().__init__(self.base_schema)
