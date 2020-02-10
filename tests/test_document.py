from http import HTTPStatus
import json

from dos.open_api import OpenAPI
from dos import prop, prop_wrapper
from dos.schema import Fields


class FakeFields(Fields):
    base_schema = {
        "a": prop.String("The error message.")
    }

    def __init__(self):
        super().__init__(self.base_schema)


def test_document():

    open_api = OpenAPI("Capital Rx Fake API", "1.0")

    open_api.add_tag(
        "fake_plan",
        "Endpoints for interacting with a fake_plan",
    )

    fake_module = type('Module', (), {})

    def input_schema():
        return FakeFields().all()

    def output_schema():
        return {
            HTTPStatus.OK: FakeFields().all(),
            HTTPStatus.BAD_REQUEST: FakeFields().all()
        }

    fake_module.input_schema = input_schema
    fake_module.output_schema = output_schema

    open_api.document(fake_module, "/fake_plan/get", http_method="post")
    documentation_json = json.dumps(open_api)

    expected_json = json.dumps(
        {
            "_disclaimer": [], "openapi": "3.0.0",
            "info": {"version": "1.0", "title": "Capital Rx Fake API", "description": None},
            "tags": [{"name": "Fake Plan", "description": "Endpoints for interacting with a fake_plan"}],
            "components": {
                "responses": {
                    "ParseError": {"description": "When a mask can't be parsed"},
                    "MaskError": {"description": "When any error occurs on mask"}
                }, "requestBodies": {
                    "fake_plan_get_input": {
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/fake_plan_get_input"}}
                        }, "required": True
                    }
                }, "schemas": {
                    "fake_plan_get_input": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_400_output": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }
                }
            },
            "paths": {
                "/fake_plan/get": {
                    "post": {
                        "responses": {
                            "200": {
                                "description": "OK", "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/fake_plan_get_200_output"}
                                    }
                                }
                            }, "400": {
                                "description": "Bad Request", "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/fake_plan_get_400_output"}
                                    }
                                }
                            }
                        }, "operationId": "/fake_plan/get", "tags": ["Fake Plan"],
                        "requestBody": {"$ref": "#/components/requestBodies/fake_plan_get_input"}
                    }
                }
            }
        }
    )

    assert documentation_json == expected_json


def test_document_single_field():

    open_api = OpenAPI("Capital Rx Fake API", "1.0")

    open_api.add_tag(
        "fake_plan",
        "Endpoints for interacting with a fake_plan",
    )

    fake_module = type('Module', (), {})

    def input_schema():
        return FakeFields().all()

    def output_schema():
        return {
            HTTPStatus.OK: FakeFields().all()
        }

    fake_module.input_schema = input_schema
    fake_module.output_schema = output_schema

    open_api.document(fake_module, "/fake_plan/get", http_method="post")
    documentation_json = json.dumps(open_api)

    expected_json = json.dumps(
        {
            "_disclaimer": [],
            "openapi": "3.0.0",
            "info": {
                "version": "1.0",
                "title": "Capital Rx Fake API",
                "description": None
            },
            "tags": [
                {
                    "name": "Fake Plan", "description": "Endpoints for interacting with a fake_plan"
                }
            ],
            "components": {
                "responses": {
                    "ParseError": {
                        "description": "When a mask can't be parsed"
                    },
                    "MaskError": {
                        "description": "When any error occurs on mask"
                    }
                },
                "requestBodies": {
                    "fake_plan_get_input": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/fake_plan_get_input"
                                }
                            }
                        },
                        "required": True
                    }
                },
                "schemas": {
                    "fake_plan_get_input": {
                        "required": ["a"],
                        "properties": {
                            "a": {
                                "type": "string",
                                "nullable": False,
                                "description": "The error message."
                            }
                        },
                        "type": "object"
                    },
                    "fake_plan_get_200_output": {
                        "required": ["a"],
                        "properties": {
                            "a": {
                                "type": "string",
                                "nullable": False,
                                "description": "The error message."
                            }
                        },
                        "type": "object"
                    }
                }
            },
            "paths": {
                "/fake_plan/get": {
                    "post": {
                        "responses": {
                            "200": {
                                "description": "OK", "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/fake_plan_get_200_output"}
                                    }
                                }
                            }
                        }, "operationId": "/fake_plan/get", "tags": ["Fake Plan"],
                        "requestBody": {
                            "$ref": "#/components/requestBodies/fake_plan_get_input"
                        }
                    }
                }
            }
        }
    )

    assert documentation_json == expected_json


def test_document_pure_dict():

    open_api = OpenAPI("Capital Rx Fake API", "1.0")

    open_api.add_tag(
        "fake_plan",
        "Endpoints for interacting with a fake_plan",
    )

    fake_module = type('Module', (), {})

    def input_schema():
        return FakeFields().all()

    def output_schema():
        return {
            HTTPStatus.OK: {
                "a": prop.String("The message."),
                "b": prop.Boolean("The boolean.")
            }
        }

    fake_module.input_schema = input_schema
    fake_module.output_schema = output_schema

    open_api.document(fake_module, "/fake_plan/get", http_method="post")
    documentation_json = json.dumps(open_api)

    expected_json = json.dumps(
        {
            "_disclaimer": [], "openapi": "3.0.0",
            "info": {"version": "1.0", "title": "Capital Rx Fake API", "description": None},
            "tags": [{"name": "Fake Plan", "description": "Endpoints for interacting with a fake_plan"}],
            "components": {
                "responses": {
                    "ParseError": {"description": "When a mask can't be parsed"},
                    "MaskError": {"description": "When any error occurs on mask"}
                }, "requestBodies": {
                    "fake_plan_get_input": {
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/fake_plan_get_input"}}
                        }, "required": True
                    }
                }, "schemas": {
                    "fake_plan_get_input": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output": {
                        "required": ["a", "b"], "properties": {
                            "a": {"type": "string", "nullable": False, "description": "The message."},
                            "b": {"type": "boolean", "nullable": False, "description": "The boolean."}
                        }, "type": "object"
                    }
                }
            },
            "paths": {
                "/fake_plan/get": {
                    "post": {
                        "responses": {
                            "200": {
                                "description": "OK", "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/fake_plan_get_200_output"}
                                    }
                                }
                            }
                        }, "operationId": "/fake_plan/get", "tags": ["Fake Plan"],
                        "requestBody": {"$ref": "#/components/requestBodies/fake_plan_get_input"}
                    }
                }
            }
        }
    )

    assert documentation_json == expected_json


def test_document_nested_object():

    open_api = OpenAPI("Capital Rx Fake API", "1.0")

    open_api.add_tag(
        "fake_plan",
        "Endpoints for interacting with a fake_plan",
    )

    fake_module = type('Module', (), {})

    def input_schema():
        return FakeFields().all()

    def output_schema():
        return {
            HTTPStatus.OK: {
                "results": prop.Object(structure=FakeFields().all(), description="Full fake object.")
            }
        }

    fake_module.input_schema = input_schema
    fake_module.output_schema = output_schema

    open_api.document(fake_module, "/fake_plan/get", http_method="post")
    documentation_json = json.dumps(open_api)

    expected_json = json.dumps(
        {
            "_disclaimer": [], "openapi": "3.0.0",
            "info": {"version": "1.0", "title": "Capital Rx Fake API", "description": None},
            "tags": [{"name": "Fake Plan", "description": "Endpoints for interacting with a fake_plan"}],
            "components": {
                "responses": {
                    "ParseError": {"description": "When a mask can't be parsed"},
                    "MaskError": {"description": "When any error occurs on mask"}
                }, "requestBodies": {
                    "fake_plan_get_input": {
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/fake_plan_get_input"}}
                        }, "required": True
                    }
                }, "schemas": {
                    "fake_plan_get_input": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_results": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output": {
                        "required": ["results"], "properties": {
                            "results": {
                                "type": "object", "nullable": False, "description": "Full fake object.",
                                "allOf": [{"$ref": "#/components/schemas/fake_plan_get_200_output_results"}]
                            }
                        }, "type": "object"
                    }
                }
            },
            "paths": {
                "/fake_plan/get": {
                    "post": {
                        "responses": {
                            "200": {
                                "description": "OK", "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/fake_plan_get_200_output"}
                                    }
                                }
                            }
                        }, "operationId": "/fake_plan/get", "tags": ["Fake Plan"],
                        "requestBody": {"$ref": "#/components/requestBodies/fake_plan_get_input"}
                    }
                }
            }
        }
    )

    assert documentation_json == expected_json


def test_document_super_nested_object():

    open_api = OpenAPI("Capital Rx Fake API", "1.0")

    open_api.add_tag(
        "fake_plan",
        "Endpoints for interacting with a fake_plan",
    )

    fake_module = type('Module', (), {})

    def input_schema():
        return FakeFields().all()

    def output_schema():
        return {
            HTTPStatus.OK: {
                "results": prop.Object(structure={
                    "another_object": prop.Object(structure={
                        "final_object": prop.Object(structure=FakeFields().all(), description="wow this is deep")
                        },
                        required=False),
                    "nested_a": prop.String("The nested message.")
                }, description="Full fake object."),
                "a": prop.String("The message.")
            }
        }

    fake_module.input_schema = input_schema
    fake_module.output_schema = output_schema

    open_api.document(fake_module, "/fake_plan/get", http_method="post")
    documentation_json = json.dumps(open_api)

    expected_json = json.dumps(
        {
            "_disclaimer": [], "openapi": "3.0.0",
            "info": {"version": "1.0", "title": "Capital Rx Fake API", "description": None},
            "tags": [{"name": "Fake Plan", "description": "Endpoints for interacting with a fake_plan"}],
            "components": {
                "responses": {
                    "ParseError": {"description": "When a mask can't be parsed"},
                    "MaskError": {"description": "When any error occurs on mask"}
                }, "requestBodies": {
                    "fake_plan_get_input": {
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/fake_plan_get_input"}}
                        }, "required": True
                    }
                }, "schemas": {
                    "fake_plan_get_input": {
                        "required": ["a"], "properties": {
                            "a": {"type": "string", "nullable": False, "description": "The error message."}
                        }, "type": "object"
                    }, "fake_plan_get_200_output_results_another_object_final_object": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_results_another_object": {
                        "required": ["final_object"], "properties": {
                            "final_object": {
                                "type": "object", "nullable": False, "description": "wow this is deep",
                                "allOf": [{
                                    "$ref": "#/components/schemas/fake_plan_get_200_output_results_another_object_final_object"
                                }]
                            }
                        }, "type": "object"
                    }, "fake_plan_get_200_output_results": {
                        "required": ["nested_a"], "properties": {
                            "another_object": {
                                "type": "object", "nullable": False, "allOf": [
                                    {"$ref": "#/components/schemas/fake_plan_get_200_output_results_another_object"}]
                            }, "nested_a": {"type": "string", "nullable": False, "description": "The nested message."}
                        }, "type": "object"
                    }, "fake_plan_get_200_output": {
                        "required": ["results", "a"], "properties": {
                            "results": {
                                "type": "object", "nullable": False, "description": "Full fake object.",
                                "allOf": [{"$ref": "#/components/schemas/fake_plan_get_200_output_results"}]
                            }, "a": {"type": "string", "nullable": False, "description": "The message."}
                        }, "type": "object"
                    }
                }
            },
            "paths": {
                "/fake_plan/get": {
                    "post": {
                        "responses": {
                            "200": {
                                "description": "OK", "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/fake_plan_get_200_output"}
                                    }
                                }
                            }
                        }, "operationId": "/fake_plan/get", "tags": ["Fake Plan"],
                        "requestBody": {"$ref": "#/components/requestBodies/fake_plan_get_input"}
                    }
                }
            }
        }
    )

    assert documentation_json == expected_json


def test_document_array_of_strings():

    open_api = OpenAPI("Capital Rx Fake API", "1.0")

    open_api.add_tag(
        "fake_plan",
        "Endpoints for interacting with a fake_plan",
    )

    fake_module = type('Module', (), {})

    def input_schema():
        return FakeFields().all()

    def output_schema():
        return {
            HTTPStatus.OK: {
                "results": prop.Array(
                    repeated_structure=prop.String(),
                    description="An array of a bunch of strings."
                ),
                "blah": prop.Object(
                    structure=FakeFields().all(),
                    description="another cool object"
                )
            }
        }

    fake_module.input_schema = input_schema
    fake_module.output_schema = output_schema

    open_api.document(fake_module, "/fake_plan/get", http_method="post")
    documentation_json = json.dumps(open_api)

    expected_json = json.dumps(
        {
            "_disclaimer": [], "openapi": "3.0.0",
            "info": {"version": "1.0", "title": "Capital Rx Fake API", "description": None},
            "tags": [{"name": "Fake Plan", "description": "Endpoints for interacting with a fake_plan"}],
            "components": {
                "responses": {
                    "ParseError": {"description": "When a mask can't be parsed"},
                    "MaskError": {"description": "When any error occurs on mask"}
                }, "requestBodies": {
                    "fake_plan_get_input": {
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/fake_plan_get_input"}}
                        }, "required": True
                    }
                }, "schemas": {
                    "fake_plan_get_input": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_blah": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output": {
                        "required": ["results", "blah"], "properties": {
                            "results": {
                                "type": "array", "nullable": False, "description": "An array of a bunch of strings.",
                                "items": {"type": "strings"}
                            }, "blah": {
                                "type": "object", "nullable": False, "description": "another cool object",
                                "allOf": [{"$ref": "#/components/schemas/fake_plan_get_200_output_blah"}]
                            }
                        }, "type": "object"
                    }
                }
            }, "paths": {
                "/fake_plan/get": {
                    "post": {
                        "responses": {
                            "200": {
                                "description": "OK", "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/fake_plan_get_200_output"}
                                    }
                                }
                            }
                        }, "operationId": "/fake_plan/get", "tags": ["Fake Plan"],
                        "requestBody": {"$ref": "#/components/requestBodies/fake_plan_get_input"}
                    }
                }
            }
        }
    )

    assert documentation_json == expected_json


def test_document_custom_structure():

    open_api = OpenAPI("Capital Rx Fake API", "1.0")

    open_api.add_tag(
        "fake_plan",
        "Endpoints for interacting with a fake_plan",
    )

    fake_module = type('Module', (), {})

    def input_schema():
        return FakeFields().all()

    def output_schema():
        return {
            HTTPStatus.OK: {
                "results": prop.Array(
                    repeated_structure=prop.Object(
                        structure={
                            "member": prop.Object(structure=FakeFields().all(), description="A full member object."),
                            "group": prop.Object(structure=FakeFields().all(), description="A full group object."),
                            "plan": prop.Object(structure=FakeFields().all(), description="A full plan object."),
                        },
                        required=True,
                        nullable=False
                    )
                )
            },
            HTTPStatus.BAD_REQUEST: FakeFields().all()
        }

    fake_module.input_schema = input_schema
    fake_module.output_schema = output_schema

    open_api.document(fake_module, "/fake_plan/get", http_method="post")
    documentation_json = json.dumps(open_api)

    expected_json = json.dumps(
        {
            "_disclaimer": [], "openapi": "3.0.0",
            "info": {"version": "1.0", "title": "Capital Rx Fake API", "description": None},
            "tags": [{"name": "Fake Plan", "description": "Endpoints for interacting with a fake_plan"}],
            "components": {
                "responses": {
                    "ParseError": {"description": "When a mask can't be parsed"},
                    "MaskError": {"description": "When any error occurs on mask"}
                }, "requestBodies": {
                    "fake_plan_get_input": {
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/fake_plan_get_input"}}
                        }, "required": True
                    }
                }, "schemas": {
                    "fake_plan_get_input": {
                        "required": ["a"], "properties": {
                            "a": {"type": "string", "nullable": False, "description": "The error message."}
                        }, "type": "object"
                    }, "fake_plan_get_200_output_results_member": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_results_group": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_results_plan": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_results": {
                        "required": ["member", "group", "plan"], "properties": {
                            "member": {
                                "type": "object", "nullable": False, "description": "A full member object.",
                                "allOf": [{"$ref": "#/components/schemas/fake_plan_get_200_output_results_member"}]
                            }, "group": {
                                "type": "object", "nullable": False, "description": "A full group object.",
                                "allOf": [{"$ref": "#/components/schemas/fake_plan_get_200_output_results_group"}]
                            }, "plan": {
                                "type": "object", "nullable": False, "description": "A full plan object.",
                                "allOf": [{"$ref": "#/components/schemas/fake_plan_get_200_output_results_plan"}]
                            }
                        }, "type": "object"
                    }, "fake_plan_get_200_output": {
                        "required": ["results"], "properties": {
                            "results": {
                                "type": "array", "nullable": False,
                                "items": {"$ref": "#/components/schemas/fake_plan_get_200_output_results"}
                            }
                        }, "type": "object"
                    }, "fake_plan_get_400_output": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }
                }
            },
            "paths": {
                "/fake_plan/get": {
                    "post": {
                        "responses": {
                            "200": {
                                "description": "OK", "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/fake_plan_get_200_output"}
                                    }
                                }
                            }, "400": {
                                "description": "Bad Request", "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/fake_plan_get_400_output"}
                                    }
                                }
                            }
                        }, "operationId": "/fake_plan/get", "tags": ["Fake Plan"],
                        "requestBody": {"$ref": "#/components/requestBodies/fake_plan_get_input"}
                    }
                }
            }
        }
    )

    assert documentation_json == expected_json


def test_array_of_custom_objects():

    open_api = OpenAPI("Capital Rx Fake API", "1.0")

    open_api.add_tag(
        "fake_plan",
        "Endpoints for interacting with a fake_plan",
    )

    fake_module = type('Module', (), {})

    def input_schema():
        return FakeFields().all()

    def output_schema():
        return {
            HTTPStatus.OK: {
                "results": prop.Array(
                    repeated_structure=prop.Object(
                        structure={
                            "claim": prop.Object(
                                structure=FakeFields().all(),
                                description="The member claims object."
                            ),
                        },
                        required=False,
                    )
                )
            },
        }

    fake_module.input_schema = input_schema
    fake_module.output_schema = output_schema

    open_api.document(fake_module, "/fake_plan/get", http_method="post")
    documentation_json = json.dumps(open_api)

    expected_json = json.dumps(
        {
            "_disclaimer": [], "openapi": "3.0.0",
            "info": {"version": "1.0", "title": "Capital Rx Fake API", "description": None},
            "tags": [{"name": "Fake Plan", "description": "Endpoints for interacting with a fake_plan"}],
            "components": {
                "responses": {
                    "ParseError": {"description": "When a mask can't be parsed"},
                    "MaskError": {"description": "When any error occurs on mask"}
                }, "requestBodies": {
                    "fake_plan_get_input": {
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/fake_plan_get_input"}}
                        }, "required": True
                    }
                }, "schemas": {
                    "fake_plan_get_input": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_results_claim": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_results": {
                        "required": ["claim"], "properties": {
                            "claim": {
                                "type": "object", "nullable": False, "description": "The member claims object.",
                                "allOf": [{"$ref": "#/components/schemas/fake_plan_get_200_output_results_claim"}]
                            }
                        }, "type": "object"
                    }, "fake_plan_get_200_output": {
                        "required": ["results"], "properties": {
                            "results": {
                                "type": "array", "nullable": False,
                                "items": {"$ref": "#/components/schemas/fake_plan_get_200_output_results"}
                            }
                        }, "type": "object"
                    }
                }
            },
            "paths": {
                "/fake_plan/get": {
                    "post": {
                        "responses": {
                            "200": {
                                "description": "OK", "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/fake_plan_get_200_output"}
                                    }
                                }
                            }
                        }, "operationId": "/fake_plan/get", "tags": ["Fake Plan"],
                        "requestBody": {"$ref": "#/components/requestBodies/fake_plan_get_input"}
                    }
                }
            }
        }
    )

    assert documentation_json == expected_json


def test_document_array_of_arrays():

    open_api = OpenAPI("Capital Rx Fake API", "1.0")

    open_api.add_tag(
        "fake_plan",
        "Endpoints for interacting with a fake_plan",
    )

    fake_module = type('Module', (), {})

    def input_schema():
        return FakeFields().all()

    def output_schema():
        return {
            HTTPStatus.OK: {
                "results": prop.Array(
                    repeated_structure=prop.Array(
                        repeated_structure=prop.Object(
                            structure=FakeFields().all()
                        )
                    )
                ),
                "blah": prop.Object(
                    structure=FakeFields().all(),
                    description="another cool object"
                )
            }
        }

    fake_module.input_schema = input_schema
    fake_module.output_schema = output_schema

    open_api.document(fake_module, "/fake_plan/get", http_method="post")
    documentation_json = json.dumps(open_api)

    expected_json = json.dumps(
        {
            "_disclaimer": [], "openapi": "3.0.0",
            "info": {"version": "1.0", "title": "Capital Rx Fake API", "description": None},
            "tags": [{"name": "Fake Plan", "description": "Endpoints for interacting with a fake_plan"}],
            "components": {
                "responses": {
                    "ParseError": {"description": "When a mask can't be parsed"},
                    "MaskError": {"description": "When any error occurs on mask"}
                }, "requestBodies": {
                    "fake_plan_get_input": {
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/fake_plan_get_input"}}
                        }, "required": True
                    }
                }, "schemas": {
                    "fake_plan_get_input": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_results": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_blah": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output": {
                        "required": ["results", "blah"], "properties": {
                            "results": {
                                "type": "array", "nullable": False,
                                "items": {"$ref": "#/components/schemas/fake_plan_get_200_output_results"}
                            }, "blah": {
                                "type": "object", "nullable": False, "description": "another cool object",
                                "allOf": [{"$ref": "#/components/schemas/fake_plan_get_200_output_blah"}]
                            }
                        }, "type": "object"
                    }
                }
            }, "paths": {
                "/fake_plan/get": {
                    "post": {
                        "responses": {
                            "200": {
                                "description": "OK", "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/fake_plan_get_200_output"}
                                    }
                                }
                            }
                        }, "operationId": "/fake_plan/get", "tags": ["Fake Plan"],
                        "requestBody": {"$ref": "#/components/requestBodies/fake_plan_get_input"}
                    }
                }
            }
        }
    )

    assert documentation_json == expected_json


def test_document_nested_object_with_same_names():

    open_api = OpenAPI("Capital Rx Fake API", "1.0")

    open_api.add_tag(
        "fake_plan",
        "Endpoints for interacting with a fake_plan",
    )

    fake_module = type('Module', (), {})

    def input_schema():
        return FakeFields().all()

    def output_schema():
        return {
            HTTPStatus.OK: {
                "results": prop.Object(
                    structure={
                        "results": prop.Object(structure=FakeFields().all(), description="wow this is deep")
                    }
                )
            },
            HTTPStatus.BAD_GATEWAY: {
                "results": prop.Object(
                    structure={
                        "results": prop.Object(structure=FakeFields().all(), description="wow this is deep")
                    }
                )
            }
        }

    fake_module.input_schema = input_schema
    fake_module.output_schema = output_schema

    open_api.document(fake_module, "/fake_plan/get", http_method="post")
    documentation_json = json.dumps(open_api)

    expected_json = json.dumps(
        {
            "_disclaimer": [], "openapi": "3.0.0",
            "info": {"version": "1.0", "title": "Capital Rx Fake API", "description": None},
            "tags": [{"name": "Fake Plan", "description": "Endpoints for interacting with a fake_plan"}],
            "components": {
                "responses": {
                    "ParseError": {"description": "When a mask can't be parsed"},
                    "MaskError": {"description": "When any error occurs on mask"}
                }, "requestBodies": {
                    "fake_plan_get_input": {
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/fake_plan_get_input"}}
                        }, "required": True
                    }
                }, "schemas": {
                    "fake_plan_get_input": {
                        "required": ["a"], "properties": {
                            "a": {"type": "string", "nullable": False, "description": "The error message."}
                        }, "type": "object"
                    }, "fake_plan_get_200_output_results_results": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_results": {
                        "required": ["results"], "properties": {
                            "results": {
                                "type": "object", "nullable": False, "description": "wow this is deep",
                                "allOf": [{"$ref": "#/components/schemas/fake_plan_get_200_output_results_results"}]
                            }
                        }, "type": "object"
                    }, "fake_plan_get_200_output": {
                        "required": ["results"], "properties": {
                            "results": {
                                "type": "object", "nullable": False,
                                "allOf": [{"$ref": "#/components/schemas/fake_plan_get_200_output_results"}]
                            }
                        }, "type": "object"
                    }, "fake_plan_get_502_output_results_results": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_502_output_results": {
                        "required": ["results"], "properties": {
                            "results": {
                                "type": "object", "nullable": False, "description": "wow this is deep",
                                "allOf": [{"$ref": "#/components/schemas/fake_plan_get_502_output_results_results"}]
                            }
                        }, "type": "object"
                    }, "fake_plan_get_502_output": {
                        "required": ["results"], "properties": {
                            "results": {
                                "type": "object", "nullable": False,
                                "allOf": [{"$ref": "#/components/schemas/fake_plan_get_502_output_results"}]
                            }
                        }, "type": "object"
                    }
                }
            },
            "paths": {
                "/fake_plan/get": {
                    "post": {
                        "responses": {
                            "200": {
                                "description": "OK", "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/fake_plan_get_200_output"}
                                    }
                                }
                            }, "502": {
                                "description": "Bad Gateway", "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/fake_plan_get_502_output"}
                                    }
                                }
                            }
                        }, "operationId": "/fake_plan/get", "tags": ["Fake Plan"],
                        "requestBody": {"$ref": "#/components/requestBodies/fake_plan_get_input"}
                    }
                }
            }
        }
    )

    assert documentation_json == expected_json


def test_document_one_of():

    open_api = OpenAPI("Capital Rx Fake API", "1.0")

    open_api.add_tag(
        "fake_plan",
        "Endpoints for interacting with a fake_plan",
    )

    fake_module = type('Module', (), {})

    def input_schema():
        return FakeFields().all()

    def output_schema():
        return {
            HTTPStatus.OK: {
                "result": prop_wrapper.OneOf([
                    prop.String(description="Test Fields"),
                    prop.String(description="Another String with different validation"),
                    prop.Boolean(description="Test Boolean", required=False),
                    prop.Object(structure=FakeFields().all(), description="Drug Fields"),
                    prop.Object(structure=FakeFields().all()),
                    prop.Array(repeated_structure=prop.Object(structure=FakeFields().all())),
                    prop.Array(
                        repeated_structure=prop.Object(
                            structure={
                                "plan": prop.Object(structure=FakeFields().all(), description="A full plan object.")
                            },
                            required=True,
                            nullable=False
                        )
                    )
                ]),
                "whoa": prop.String("hello"),
                "array_str": prop.Array(repeated_structure=prop.Boolean()),
                "array of objects": prop.Array(repeated_structure=prop.Object(structure=FakeFields().all()),
                                               description="WHat!!!"),
                "another_normal_field": prop.String()
            }
        }

    fake_module.input_schema = input_schema
    fake_module.output_schema = output_schema

    open_api.document(fake_module, "/fake_plan/get", http_method="post")
    documentation_json = json.dumps(open_api)

    expected_json = json.dumps(
        {
            "_disclaimer": [], "openapi": "3.0.0",
            "info": {"version": "1.0", "title": "Capital Rx Fake API", "description": None},
            "tags": [{"name": "Fake Plan", "description": "Endpoints for interacting with a fake_plan"}],
            "components": {
                "responses": {
                    "ParseError": {"description": "When a mask can't be parsed"},
                    "MaskError": {"description": "When any error occurs on mask"}
                }, "requestBodies": {
                    "fake_plan_get_input": {
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/fake_plan_get_input"}}
                        }, "required": True
                    }
                }, "schemas": {
                    "fake_plan_get_input": {
                        "required": ["a"], "properties": {
                            "a": {"type": "string", "nullable": False, "description": "The error message."}
                        }, "type": "object"
                    }, "fake_plan_get_200_output_result_object_0": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_result_object_1": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_result_array_0": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_result_array_1_plan": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output_result_array_1": {
                        "required": ["plan"], "properties": {
                            "plan": {
                                "type": "object", "nullable": False, "description": "A full plan object.",
                                "allOf": [{"$ref": "#/components/schemas/fake_plan_get_200_output_result_array_1_plan"}]
                            }
                        }, "type": "object"
                    }, "fake_plan_get_200_output_array of objects": {
                        "required": ["a"],
                        "properties": {"a": {"type": "string", "nullable": False, "description": "The error message."}},
                        "type": "object"
                    }, "fake_plan_get_200_output": {
                        "required": ["whoa", "array_str", "array of objects", "another_normal_field"], "properties": {
                            "result": {
                                "oneOf": [{"type": "string", "nullable": False, "description": "Test Fields"}, {
                                    "type": "string", "nullable": False,
                                    "description": "Another String with different validation"
                                }, {"type": "boolean", "nullable": False, "description": "Test Boolean"},
                                          {"$ref": "#/components/schemas/fake_plan_get_200_output_result_object_0"},
                                          {"$ref": "#/components/schemas/fake_plan_get_200_output_result_object_1"}, {
                                              "type": "array", "nullable": False, "items": {
                                            "$ref": "#/components/schemas/fake_plan_get_200_output_result_array_0"
                                        }
                                          }, {
                                              "type": "array", "nullable": False, "items": {
                                            "$ref": "#/components/schemas/fake_plan_get_200_output_result_array_1"
                                        }
                                          }]
                            }, "whoa": {"type": "string", "nullable": False, "description": "hello"},
                            "array_str": {"type": "array", "nullable": False, "items": {"type": "booleans"}},
                            "array of objects": {
                                "type": "array", "nullable": False, "description": "WHat!!!",
                                "items": {"$ref": "#/components/schemas/fake_plan_get_200_output_array of objects"}
                            }, "another_normal_field": {"type": "string", "nullable": False}
                        }, "type": "object"
                    }
                }
            },
            "paths": {
                "/fake_plan/get": {
                    "post": {
                        "responses": {
                            "200": {
                                "description": "OK", "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/fake_plan_get_200_output"}
                                    }
                                }
                            }
                        }, "operationId": "/fake_plan/get", "tags": ["Fake Plan"],
                        "requestBody": {"$ref": "#/components/requestBodies/fake_plan_get_input"}
                    }
                }
            }
        }
    )

    assert documentation_json == expected_json
