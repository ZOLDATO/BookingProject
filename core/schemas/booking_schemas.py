BOOKING_SCHEMA = {
    "type": "object",
    "properties": {
        "firstname": {
            "type": "string"
        },
        "lastname": {
            "type": "string"
        },
        "totalprice": {
            "type": "number"
        },
        "depositpaid": {
            "type": "boolean"
        },
        "bookingdates": {
            "type": "object",
            "properties": {
                "checkin": {
                    "type": "string",
                    "format": "date"
                },
                "checkout": {
                    "type": "string",
                    "format": "date"
                }
            }
        },
        "additionalneeds": {
            "type": "string"
        }
    }
}
