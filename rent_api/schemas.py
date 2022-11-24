from main import app
from pydantic import BaseModel


class Appartments(BaseModel):
    address: str
    floor: str
    price: str
    id_r: int
    phone: str
    link: str
    date: str
    meters: str
