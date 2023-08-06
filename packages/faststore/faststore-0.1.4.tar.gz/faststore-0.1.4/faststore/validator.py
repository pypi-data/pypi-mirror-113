from typing import Any

from google.cloud.firestore_v1.document import DocumentReference
from pydantic.validators import _VALIDATORS

from .error import DocumentReferenceError


def document_reference_validator(v: Any):
    if isinstance(v, DocumentReference):
        return v
    raise DocumentReferenceError


def setup_custom_validators():
    _VALIDATORS.append((DocumentReference, [document_reference_validator]))
