import json
from aimaxsdk import errors


def parse_response(response, *keys):
    status_code = response.status_code
    if status_code == 200:
        data = json.loads(response.text)
        if data["success"]:
            for key in keys:
                data = data[key]
            return True, data
        else:
            if data["message"] in errors.all_errors:
                if data["messageParams"]:
                    return False, errors.all_errors[data["message"]].format(data["messageParams"])
                return False, errors.all_errors[data["message"]]
            else:
                return False, "Unknown Error"
    else:
        return False, status_code
