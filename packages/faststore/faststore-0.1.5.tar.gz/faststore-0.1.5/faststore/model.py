from google.cloud import firestore
from google.cloud.firestore_v1.base_collection import _auto_id
from pydantic import BaseModel, Field

db = firestore.Client()


class Model(BaseModel):
    id: str = Field(default_factory=_auto_id)

    @classmethod
    def get(cls, id: str):
        doc = db.collection(cls.__name__.lower()).document(id).get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return cls(**data)

    def get_document_reference(self):
        return db.collection(self.__class__.__name__.lower()).document(self.id)

    def save(self):
        data = self.dict()
        data.pop("id")
        db.collection(self.__class__.__name__.lower()).document(self.id).set(data)

    def delete(self):
        db.collection(self.__class__.__name__.lower()).document(self.id).delete()
