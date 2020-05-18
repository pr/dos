import arrow
from http import HTTPStatus
import pytest

from dos import prop, prop_wrapper, validators
from dos.schema import Fields
from dos.flask_wrappers import create_output


class SimpleFields(Fields):
    base_schema = {
        "message": prop.String("The message.")
    }

    def __init__(self):
        super().__init__(self.base_schema)


class NestedFields(Fields):
    base_schema = {
        "top_level_id": prop.Integer(
            description="The top level ID.",
        ),
        "top_level_array": prop.Array(
            repeated_structure=prop.Object(
                structure={
                    "nested_id": prop.Integer(
                        "The nested ID."
                    ),
                    "nested_array": prop.Array(
                        repeated_structure=prop.Object(
                            structure={
                                "super_nested_id": prop.Integer(
                                    description="The super nested ID."
                                ),
                                "another_number": prop.Number(
                                    description="The super nested number.",
                                ),
                            }
                        ),
                    ),
                }
            )
        ),
    }

    def __init__(self):
        super().__init__(self.base_schema)


def test_create_output():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String(),
            "basic_boolean": prop.Boolean()
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "test string",
        "basic_boolean": True,
        "secret_info": "secret info"
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "basic_string": "test string",
        "basic_boolean": True
    }


def test_multiple_outputs():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String(),
            "basic_boolean": prop.Boolean()
        },
        HTTPStatus.BAD_REQUEST: {
            "message": prop.String("Nope")
        }
    }

    result = HTTPStatus.BAD_REQUEST, {
        "message": "Oh man"
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 400
    assert returned_dict == {
        "message": "Oh man",
    }


def test_required_true_nullable_true_not_present():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=True, nullable=True),
        }
    }

    result = HTTPStatus.OK, {
    }

    with pytest.raises(prop.ValidationError) as e:
        create_output(result, output_schema)

    assert e.value.message == "The field 'basic_string' is required but not found in the body!"


def test_required_true_nullable_true_is_present_is_none():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=True, nullable=True),
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": None
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "basic_string": None
    }


def test_required_true_nullable_true_is_present_not_none():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=True, nullable=True),
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "test"
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "basic_string": "test"
    }


def test_required_false_nullable_true_not_present():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=False, nullable=True),
        }
    }

    result = HTTPStatus.OK, {
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {}


def test_required_false_nullable_true_is_present_is_none():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=False, nullable=True),
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": None
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {}


def test_required_false_nullable_true_is_present_not_none():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=False, nullable=True),
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "test"
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "basic_string": "test"
    }


def test_required_true_nullable_false_not_present():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=True, nullable=False),
        }
    }

    result = HTTPStatus.OK, {
    }

    with pytest.raises(prop.ValidationError) as e:
        create_output(result, output_schema)

    assert e.value.message == "The field 'basic_string' is required but not found in the body!"


def test_required_true_nullable_false_is_present_is_none():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=True, nullable=False),
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": None
    }

    with pytest.raises(prop.ValidationError) as e:
        create_output(result, output_schema)

    assert e.value.message == "Non nullable field 'basic_string' is null!"


def test_required_true_nullable_false_is_present_not_none():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=True, nullable=False),
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "test"
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "basic_string": "test"
    }


def test_required_false_nullable_false_not_present():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=False, nullable=False),
        }
    }

    result = HTTPStatus.OK, {
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {}


def test_required_false_nullable_false_is_present_is_none():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=False, nullable=False),
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": None
    }

    with pytest.raises(prop.ValidationError) as e:
        create_output(result, output_schema)

    assert e.value.message == "Non nullable field 'basic_string' is null!"


def test_required_false_nullable_false_is_present_not_none():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=False, nullable=False),
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "test"
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "basic_string": "test"
    }


def test_required_false_nullable_false_is_present_not_none_not_there():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=False, nullable=False),
        }
    }

    result = HTTPStatus.OK, {}

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {}


def test_required_false_nullable_true_is_present_not_none_not_there():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=False, nullable=True),
        }
    }

    result = HTTPStatus.OK, {}

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {}


def test_required_false_nullable_false_is_present_not_none_there_and_null():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String("Description", required=False, nullable=False),
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": None
    }

    with pytest.raises(prop.ValidationError) as e:
        create_output(result, output_schema)

    assert e.value.message == "Non nullable field 'basic_string' is null!"


def test_create_output_identical_dict():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String(),
            "basic_boolean": prop.Boolean(),
            "sub_dict": prop.Object(
                structure={
                    "sub_string": prop.String()
                }
            )
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "test string",
        "basic_boolean": True,
        "sub_dict": {
            "sub_string": "hello",
        }
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200

    assert returned_dict == {
        "basic_string": "test string",
        "basic_boolean": True,
        "sub_dict": {
            "sub_string": "hello"
        }
    }


def test_create_output_different_dict():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String(),
            "basic_boolean": prop.Boolean(),
            "sub_dict": prop.Object(
                structure={
                    "sub_string": prop.String()
                },
                description="This is a fake object nested in a dictionary",
                required=True,
                nullable=False
            )
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "test string",
        "basic_boolean": True,
        "sub_dict": {
            "sub_string": "hello",
            "not_this": "Not this"
        }
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200

    assert returned_dict == {
        "basic_string": "test string",
        "basic_boolean": True,
        "sub_dict": {
            "sub_string": "hello"
        }
    }


def test_triple_nested_dicts():


    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String(),
            "basic_boolean": prop.Boolean(),
            "sub_dict": prop.Object(
                structure={
                    "sub_string": prop.String("the string"),
                    "sub_sub_dict": prop.Object(
                        structure={
                            "boo": prop.Boolean()
                        }
                    )
                },
                description="A list of plans."
            )
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "test string",
        "basic_boolean": True,
        "sub_dict": {
            "sub_string": "hello",
            "not_this": "Not this",
            "sub_sub_dict": {
                "boo": False,
                "why_is_this_here": "ignore"
            }
        }
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200

    assert returned_dict == {
        "basic_string": "test string",
        "basic_boolean": True,
        "sub_dict": {
            "sub_string": "hello",
            "sub_sub_dict": {
                "boo": False
            }
        }
    }


def test_create_output_array_of_objects():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String(),
            "basic_boolean": prop.Boolean(),
            "array_of_objects": prop.Array(
                repeated_structure=prop.Object(
                    structure={
                        "sub_string": prop.String("the string")
                    }
                ),
                description="A list of plans."
            )
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "test string",
        "basic_boolean": True,
        "array_of_objects": [
            {
                "sub_string": "hello",
                "not_this": "not this"
            },
            {
                "sub_string": "hello",
                "not_this": "still not this",
                "another_one": "???"
            }
        ]
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200

    assert returned_dict == {
        "basic_string": "test string",
        "basic_boolean": True,
        "array_of_objects": [
            {
                "sub_string": "hello",
            },
            {
                "sub_string": "hello",
            }
        ]
    }


def test_create_output_array_of_strings():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String(),
            "basic_boolean": prop.Boolean(),
            "array_of_strings": prop.Array(
                repeated_structure=prop.String("just a list of strings"),
                description="A description of what this array contains"
            )
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "test string",
        "basic_boolean": True,
        "array_of_strings": ["hello", "hello again"]
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "basic_string": "test string",
        "basic_boolean": True,
        "array_of_strings": ["hello", "hello again"]
    }


def test_specializer_object():

    output_schema = {
        HTTPStatus.OK: SimpleFields().all()
    }

    result = HTTPStatus.OK, {
        "message": "hello"
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "message": "hello"
    }


def test_nested_specializer_object():

    output_schema = {
        HTTPStatus.OK: NestedFields().all()
    }

    result = HTTPStatus.OK, {
        "top_level_id": 34,
        "top_level_array": [
            {
                "nested_id": 45,
                "nested_array": [
                    {
                        "super_nested_id": 56,
                        "another_number": 23
                    },
                    {
                        "super_nested_id": 57,
                        "another_number": 23
                    }
                ]
            }
        ]
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "top_level_id": 34,
        "top_level_array": [
            {
                "nested_id": 45,
                "nested_array": [
                    {
                        "super_nested_id": 56,
                        "another_number": 23
                    },
                    {
                        "super_nested_id": 57,
                        "another_number": 23
                    }
                ]
            }
        ]
    }


def test_nested_specializer_object_with_results_structure():

    output_schema = {
        HTTPStatus.OK: {
            "results": prop.Array(
                repeated_structure=prop.Object(
                    structure=SimpleFields().all(), description="A basic field object"
                )
            )
        }
    }

    result = HTTPStatus.OK, {
        "results": [
            {"message": "hello"},
            {"message": "hello"},
            {"message": "hello"},
            {"message": "hello"}
        ]
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "results": [
            {"message": "hello"},
            {"message": "hello"},
            {"message": "hello"},
            {"message": "hello"}
        ]
    }


def test_nested_specializer_object_with_results_structure_and_specialize():

    output_schema = {
        HTTPStatus.OK: {
            "results": prop.Array(
                repeated_structure=prop.Object(
                    structure=NestedFields().specialize(only=["top_level_id"]), description="A basic field object"
                )
            )
        }
    }

    result = HTTPStatus.OK, {
        "results": [
            {
                "top_level_id": 31,
                "don_t_return_me": "super secret data"
             },
            {
                "top_level_id": 32
            },
            {
                "top_level_id": 33
            },
            {
                "top_level_id": 34,
                "don_t_return_me": "even more secret data"
            },
        ]
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "results": [
            {"top_level_id": 31},
            {"top_level_id": 32},
            {"top_level_id": 33},
            {"top_level_id": 34},
        ]
    }


def test_nested_specializer_object_with_results_array_of_strings():

    output_schema = {
        HTTPStatus.OK: {
            "results": prop.Array(
                repeated_structure=prop.String("this is an array of strings", required=True, nullable=False)
            )
        }
    }

    result = HTTPStatus.OK, {
        "results": ["perfectly", "valid", "array", "of", "strings"]
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "results": ["perfectly", "valid", "array", "of", "strings"]
    }


def test_no_defined_schema():
    output_schema = {
        HTTPStatus.BAD_REQUEST: {
            "basic_string": prop.String("Description", required=True, nullable=True),
        }
    }

    result = HTTPStatus.OK, {
    }

    with pytest.raises(prop.ValidationError) as e:
        create_output(result, output_schema)

    assert e.value.message == "Endpoint does not define http status code 200 in the output schema!"


def test_nested_required_field():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String(),
            "basic_boolean": prop.Boolean(),
            "object": prop.Object(
                structure={
                    "sub_string": prop.String("the string", required=False),
                    "required_string": prop.String(required=True)
                }
            )
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "test string",
        "basic_boolean": True,
        "object": {
            "sub_string": "hello",
        },
    }

    with pytest.raises(prop.ValidationError) as e:
        create_output(result, output_schema)

    assert e.value.message == "The field 'required_string' is required but not found in the body!"


def test_very_nested_required_field():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String(),
            "basic_boolean": prop.Boolean(),
            "array_of_objects": prop.Array(
                repeated_structure=prop.Object(
                    structure={
                        "sub_string": prop.String("the string", required=True, nullable=True),
                        "required_one": prop.String(required=True, nullable=False)
                    }
                ),
                description="A list of plans."
            )
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "test string",
        "basic_boolean": True,
        "array_of_objects": [
            {
                "sub_string": None,
                "required_one": "here"
            },
            {
                "sub_string": "hello",
            }
        ]
    }

    with pytest.raises(prop.ValidationError) as e:
        create_output(result, output_schema)

    assert e.value.message == "The field 'required_one' is required but not found in the body!"


def test_very_nested_nullable_field():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String(),
            "basic_boolean": prop.Boolean(),
            "array_of_objects": prop.Array(
                repeated_structure=prop.Object(
                    structure={
                        "sub_string": prop.String("the string", required=True, nullable=False),
                        "required_one": prop.String(required=True, nullable=False)
                    }
                ),
                description="A list of plans."
            )
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "test string",
        "basic_boolean": True,
        "array_of_objects": [
            {
                "sub_string": None,
                "required_one": "here"
            },
            {
                "sub_string": "hello",
                "required_one": "here_too"
            }
        ]
    }

    with pytest.raises(prop.ValidationError) as e:
        create_output(result, output_schema)

    assert e.value.message == "Non nullable field 'sub_string' is null!"


def test_nullable_array_of_strings():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String(),
            "basic_boolean": prop.Boolean(),
            "array_of_strings": prop.Array(
                repeated_structure=prop.String("just a list of strings"),
                description="A description of what this array contains",
                required=True,
                nullable=False
            )
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "test string",
        "basic_boolean": True,
        "array_of_strings": None
    }

    with pytest.raises(prop.ValidationError) as e:
        create_output(result, output_schema)

    assert e.value.message == "Non nullable field 'array_of_strings' is null!"


def test_one_of():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop_wrapper.OneOf([
                prop.String(),
                prop.Boolean()
            ])
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "asdf"
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "basic_string": "asdf"
    }


def test_one_of_invalid():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop_wrapper.OneOf([
                prop.String(validators=[validators.ExactLength(2)]),
                prop.Boolean()
            ])
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": "asdf"
    }

    with pytest.raises(prop.ValidationError) as e:
        create_output(result, output_schema)

    assert e.value.message == ("The value 'asdf' from field 'basic_string' is not "
                               "valid for one of the defined props for the following "
                               "reasons: String is not the correct length! The string "
                               "'asdf' is 4 characters long, not 2!, The value 'asdf' "
                               "from field 'basic_string' is the wrong type, expected: Boolean")


def test_output_of_wrong_type():

    output_schema = {
        HTTPStatus.OK: {
            "basic_string": prop.String(),
        }
    }

    result = HTTPStatus.OK, {
        "basic_string": 80.99
    }

    with pytest.raises(prop.ValidationError) as e:
        create_output(result, output_schema)

    assert e.value.message == "The value 80.99 from field 'basic_string' is the wrong type, expected: String"


def test_output_number():

    output_schema = {
        HTTPStatus.OK: {
            "basic_number": prop.Number(),
        }
    }

    result = HTTPStatus.OK, {
        "basic_number": 80.99
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "basic_number": 80.99
    }


def test_output_literal_number_string():

    output_schema = {
        HTTPStatus.OK: {
            "basic_number": prop.Number(),
        }
    }

    result = HTTPStatus.OK, {
        "basic_number": "eighty point nine nine"
    }

    with pytest.raises(prop.ValidationError) as e:
        create_output(result, output_schema)

    assert e.value.message == "The value 'eighty point nine nine' from field 'basic_number' is the wrong type, expected: Number"


def test_output_number_string():

    output_schema = {
        HTTPStatus.OK: {
            "basic_number": prop.Number(),
        }
    }

    result = HTTPStatus.OK, {
        "basic_number": "80.99"
    }

    with pytest.raises(prop.ValidationError) as e:
        create_output(result, output_schema)

    assert e.value.message == "The value '80.99' from field 'basic_number' is the wrong type, expected: Number"


def test_output_numeric_string():

    output_schema = {
        HTTPStatus.OK: {
            "basic_number": prop.Numeric(),
        }
    }

    result = HTTPStatus.OK, {
        "basic_number": "80.99"
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "basic_number": "80.99"
    }


def test_arrow_date():
    output_schema = {
        HTTPStatus.OK: {
            "arrow_date": prop.DateTime(),
        }
    }

    result = HTTPStatus.OK, {
        "arrow_date": arrow.get(2020, 7, 1)
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "arrow_date": "2020-07-01T00:00:00+00:00"
    }


def test_none_date_in_a_string():
    output_schema = {
        HTTPStatus.OK: {
            "arrow_date": prop.DateTime(required=False, nullable=True),
        }
    }

    result = HTTPStatus.OK, {
        "arrow_date": "None"
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {
        "arrow_date": "None"
    }


def test_none_date_not_in_a_string():
    output_schema = {
        HTTPStatus.OK: {
            "arrow_date": prop.DateTime(required=False, nullable=True),
        }
    }

    result = HTTPStatus.OK, {
        "arrow_date": None
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {}


def test_none_enum():
    output_schema = {
        HTTPStatus.OK: {
            "enum": prop.Enum(required=False, nullable=True),
        }
    }

    result = HTTPStatus.OK, {
        "enum": None
    }

    http_status_code, returned_dict = create_output(result, output_schema)
    assert http_status_code == 200
    assert returned_dict == {}
