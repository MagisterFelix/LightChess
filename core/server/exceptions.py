from rest_framework.views import exception_handler


def api_exception_handler(exception, context):
    response = exception_handler(exception, context)

    if response is None:
        return response

    payload = {
        "details": []
    }

    for field, errors in response.data.items():
        if isinstance(errors, list):
            errors = " ".join(errors)

        if "unique set" in errors:
            errors = "Values must be unique."

        payload["details"].append({
            field: ". ".join(err if err[0].isupper() else err.capitalize() for err in errors.split(". "))
        })

    response.data = payload

    return response
