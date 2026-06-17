from pydantic import BaseModel


class DNASplitRequest(BaseModel):
    parent_dna: str
    split_amount: int