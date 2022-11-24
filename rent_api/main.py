from typing import Optional

from sqlalchemy.orm import Session
from db import get_db
from models import ST
from fastapi import FastAPI, Depends

app = FastAPI()


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    query = {
        "address": "\nМинск,Охотскаяул.,140",
        "floor": " 1/1",
        "price": "28000",
        "link": "https://www.t-s.by/buy/flats/1-komnatnaya-kvartira-minsk-okhotskaya-ul-140-982055/",
        "meters": "\n38.9/25.7/8.8м²\n",
    }
    new_row = ST(**query)
    db.add(new_row)
    db.commit()
    db.refresh(new_row)
    return {"Hello": query}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
