schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "rocket_pos": {
            "type": "array",
            "items": [
                {
                    "type": "integer"
                },
                {
                    "type": "integer"
                }
            ]
        },
        "Lagrange_pos": {
            "type": "array",
            "items": [
                {
                    "type": "integer"
                },
                {
                    "type": "integer"
                }
            ]
        },
        "rocket_speed": {
            "type": "object",
            "properties": {
                "x": {
                    "type": "integer"
                },
                "y": {
                    "type": "integer"
                },
                "r": {
                    "type": "integer"
                }
            },
            "required": [
                "x",
                "y",
                "r"
            ]
        },
        "change_of_speed": {
            "type": "object",
            "properties": {
                "x": {
                    "type": "integer"
                },
                "y": {
                    "type": "integer"
                },
                "r": {
                    "type": "integer"
                }
            },
            "required": [
                "x",
                "y",
                "r"
            ]
        }
    },
    "required": [
        "rocket_pos",
        "Lagrange_pos",
        "rocket_speed",
        "change_of_speed"
    ]
}
