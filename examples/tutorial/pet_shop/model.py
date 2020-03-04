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
