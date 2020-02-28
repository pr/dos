from flask import request
from http import HTTPStatus

from pet_shop.model import DogFields, ErrorFields


def handler():

    """
    Very basic example, in a real API this would be stored in a database.
    """

    body = request.get_json()

    name = body["name"]

    if name == "Spot":
        dog = {
            "name": "Spot",
            "breed": "Poodle",
            "super_secret": "This is in the database, but should not be exposed."
        }
        return HTTPStatus.OK, dog
    else:
        return HTTPStatus.NOT_FOUND, {"message": "No dog by that name found!"}


def input_schema():
    return DogFields().specialize(only=["name"])


def output_schema():
    return {
        HTTPStatus.OK: DogFields().all(),
        HTTPStatus.NOT_FOUND: ErrorFields().all()
    }
