

class BaseController(object):
    def __init__(self):
        pass

    @staticmethod
    def abort_if_validate_error(rules, data):
        valid = HttpValidator(rules)
        val_result = valid.validate_object(data)
        if not val_result[VALIDATION_RESULT.VALID]:
            errors = val_result[VALIDATION_RESULT.ERRORS]
            raise ParamInvalidError(LANG.VALIDATE_ERROR, errors)
