schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
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
        },
        "speed": {
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
        "L1": {
            "type": "array",
            "items": [
                {
                    "type": "integer"
                },
                {
                    "type": "integer"
                }
            ]
        }
    },
    "required": [
        "change_of_speed",
        "speed",
        "rocket_pos",
        "L1"
    ]
}
