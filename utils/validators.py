def input_validator(value: dict) -> dict:
    result: dict = {
        "status": True,
        "errors": []
    }

    for key, val in value.items():
        if not val:
            result["status"] = False
            result['errors'].append(key)

    return result
