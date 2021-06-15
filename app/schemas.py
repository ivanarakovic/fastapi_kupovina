from pydantic import BaseModel
from datetime import datetime

class Kupovina(BaseModel):
    id: int
    kupac: str
    grad: str
    datum_vrijeme: datetime
    proizvod: str
    cijena: float