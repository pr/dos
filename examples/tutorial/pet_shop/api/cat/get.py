from flask import request
from http import HTTPStatus

from pet_shop.model import CatFields, ErrorFields


def handler():

    """
    Very basic example, in a real API this would be stored in a database.
    """

    body = request.get_json()

    name = body["name"]

    if name == "Butterball":
        cat = {
            "name": "Butterball",
            "breed": "Tabby",
            "color": "Orange"
        }
        return HTTPStatus.OK, cat
    else:
        return HTTPStatus.NOT_FOUND, {"message": "No cat by that name found!"}


def input_schema():
    return CatFields().specialize(only=["name"])


def output_schema():
    return {
        HTTPStatus.OK: CatFields().all(),
        HTTPStatus.NOT_FOUND: ErrorFields().all()
    }
