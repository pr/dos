from http import HTTPStatus

from dos import prop, prop_wrapper, validators
from dos.flask_wrappers import validate_input


def test_validate_input():

    input_schema = {
        "basic_string": prop.String(),
        "basic_boolean": prop.Boolean()
    }

    given_request = {
        "basic_string": "test string",
        "basic_boolean": True,
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {}
    assert http_status is HTTPStatus.OK


def test_validate_input_unexpected_field():

    input_schema = {
        "basic_string": prop.String(),
        "basic_boolean": prop.Boolean()
    }

    given_request = {
        "basic_string": "test string",
        "basic_boolean": True,
        "what_the_heck": "is this????"
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {
        "message": "An unexpected field was sent to the server: what_the_heck"
    }
    assert http_status == HTTPStatus.BAD_REQUEST


def test_validate_input_multiple_unexpected_fields():

    input_schema = {
        "basic_string": prop.String(),
        "basic_boolean": prop.Boolean()
    }

    given_request = {
        "basic_string": "test string",
        "basic_boolean": True,
        "what_the_heck": "is this????",
        "more_BS": "SQL INJECTION!!"
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {
        "message": "Unexpected fields were sent to the server: [\'what_the_heck\', \'more_BS\']"
    }
    assert http_status == HTTPStatus.BAD_REQUEST


def test_validate_input_missing_field():

    input_schema = {
        "basic_string": prop.String(required=True),
        "basic_boolean": prop.Boolean()
    }

    given_request = {
        "basic_boolean": True,
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {
        "message": "A required field is missing: basic_string"
    }
    assert http_status == HTTPStatus.BAD_REQUEST


def test_validate_input_multiple_missing_fields():

    input_schema = {
        "basic_string": prop.String(required=True),
        "another_basic_string": prop.String(required=True),
        "basic_boolean": prop.Boolean()
    }

    given_request = {
        "basic_boolean": True,
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {
        "message": "Required fields are missing: ['basic_string', 'another_basic_string']",
    }
    assert http_status == HTTPStatus.BAD_REQUEST


def test_validate_input_wrong_type():

    input_schema = {
        "basic_string": prop.String(),
        "basic_boolean": prop.Boolean()
    }

    given_request = {
        "basic_string": ["what", "the", "heck", "is", "this"],
        "basic_boolean": True,
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {
        'field_error_messages': {
            'basic_string': "The value ['what', 'the', 'heck', 'is', 'this'] from field "
                            "'basic_string' is the wrong type, expected: String"
        }
    }

    assert http_status == HTTPStatus.BAD_REQUEST


def test_validate_input_string_id():

    input_schema = {
        "id": prop.Number(),
    }

    given_request = {
        "id": "89"
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {}
    assert http_status is HTTPStatus.OK


def test_validate_input_string_id_not_a_number():

    input_schema = {
        "id": prop.Number(),
    }

    given_request = {
        "id": "banana_phone"
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {
        'field_error_messages': {
            'id': "The value 'banana_phone' from field 'id' is "
                  "the wrong type, expected: Number"
        }
    }

    assert http_status == HTTPStatus.BAD_REQUEST


def test_validate_numeric_string():

    input_schema = {
        "id": prop.Numeric()
    }

    given_request = {
        "id": "1,000"
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {}
    assert http_status is HTTPStatus.OK


def test_validate_number_string():

    input_schema = {
        "id": prop.Number()
    }

    given_request = {
        "id": "1,000"
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {}
    assert http_status is HTTPStatus.OK


def test_validate_input_one_of():

    input_schema = {
        "id": prop_wrapper.OneOf([
            prop.String(validators=[validators.ExactLength(3)]),
            prop.String(validators=[validators.ExactLength(8)]),
            prop.Number()
        ])
    }

    given_request = {
        "id": "abc"
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {}
    assert http_status is HTTPStatus.OK


def test_validate_input_one_of_invalid():

    input_schema = {
        "id": prop_wrapper.OneOf([
            prop.String(validators=[validators.ExactLength(3)]),
            prop.String(validators=[validators.ExactLength(8)]),
            prop.Number()
        ])
    }

    given_request = {
        "id": "banana_phone"
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {
        'field_error_messages': {

            'id': ("The value 'banana_phone' from field 'id' is not valid for one of the defined props for "
                   "the following reasons: String is not the correct length! The string 'banana_phone' is "
                   "12 characters long, not 3!, String is not the correct length! The string 'banana_phone' is "
                   "12 characters long, not 8!, The value 'banana_phone' from field 'id' is the wrong "
                   'type, expected: Number')

        }
    }

    assert http_status == HTTPStatus.BAD_REQUEST


def test_validate_input_string_id_not_an_integer():

    input_schema = {
        "id": prop.Number(),
    }

    given_request = {
        "id": "56.32"
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {}
    assert http_status is HTTPStatus.OK


def test_validate_input_string_id_not_negative_number():

    input_schema = {
        "id": prop.Number(),
    }

    given_request = {
        "id": "-2"
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {}
    assert http_status is HTTPStatus.OK


def test_validate_input_multiple_input_issues():

    input_schema = {
        "basic_string": prop.String(),
        "basic_boolean": prop.Boolean(),
        "not_present_required_field": prop.String(required=True)
    }

    given_request = {
        "basic_string": "test string",
        "basic_boolean": True,
        "what_the_heck": "is this????",
        "more_BS": "SQL INJECTION!!"
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {
        "message": ("Unexpected fields were sent to the server: [\'what_the_heck\', \'more_BS\'] /// "
                    "A required field is missing: not_present_required_field")
    }
    assert http_status == HTTPStatus.BAD_REQUEST


def test_validate_input_exact_length_string():

    input_schema = {
        "basic_string": prop.String(validators=[validators.ExactLength(8)]),
    }

    given_request = {
        "basic_string": "noteightlong",
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {
        'field_error_messages': {
            'basic_string': 'String is not the correct length! The string \'noteightlong\' is 12 characters long, not 8!'
        }
    }

    assert http_status == HTTPStatus.BAD_REQUEST


def test_validate_input_exact_length_object():

    input_schema = {
        "basic_object": prop.Object(
            structure={
                "basic_string": prop.String()
            },
            validators=[validators.ExactLength(8)]
        ),
    }

    given_request = {
        "basic_object": {
            "basic_string": "this is irrelevant",
        }
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {
        'field_error_messages': {'basic_object': 'ExactLength is not supported for class Object!!'}
    }

    assert http_status == HTTPStatus.BAD_REQUEST


def test_validate_social_security_number():

    input_schema = {
        "social_security_number": prop.String(validators=[validators.SocialSecurityNumber()]),
    }

    given_request = {
        "social_security_number": "219099999",
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {
        'field_error_messages': {
            'social_security_number': '219099999 is not a valid social security number!'
        }
    }

    assert http_status == HTTPStatus.BAD_REQUEST


def test_validate_number_social_security_number():
    input_schema = {
        "social_security_number": prop.Number(validators=[validators.SocialSecurityNumber()]),
    }

    given_request = {
        "social_security_number": "219099999",
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {
        'field_error_messages': {
            'social_security_number': 'SocialSecurityNumber is not supported for class Number!!'
        }
    }

    assert http_status == HTTPStatus.BAD_REQUEST


def test_impossible_validation():
    input_schema = {
        "social_security_number": prop.String(validators=[validators.SocialSecurityNumber(), validators.ExactLength(3)]),
    }

    given_request = {
        "social_security_number": "578271234",
    }

    http_status, reject_dict = validate_input(given_request, input_schema)
    assert reject_dict == {
        'field_error_messages': {
            'social_security_number': 'String is not the correct length! The string \'578271234\' is 9 characters long, not 3!'
        }
    }

    assert http_status == HTTPStatus.BAD_REQUEST
