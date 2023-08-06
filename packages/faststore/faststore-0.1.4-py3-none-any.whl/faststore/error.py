from pydantic.errors import PydanticTypeError


class DocumentReferenceError(PydanticTypeError):
    msg_template = "value is not a valid DocumentReference"
