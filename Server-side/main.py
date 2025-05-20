import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pymysql

app = FastAPI()


class InputLink(BaseModel):
    link: str


class Listing(BaseModel):
    name: str
    percentage: int
    url: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sina.mhreza.ir"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_similar(url):
    db = pymysql.connect(
        host='sahand.liara.cloud',
        port=30896,
        user='root',
        password='3gsc2mpq4mY217f04ccMxncb',
        database='upbeat_hodgkin',
        charset='utf8mb4'
    )
    cursor = db.cursor()
    try:
        # /////////////////// TEMP
        query = "SELECT * FROM listings WHERE url = %s;"
        cursor.execute(query, (url.link,))
        row = cursor.fetchone()
        cursor.close()
        return [Listing(name=f"{row[2]}", percentage=64, url=f"{row[1]}")] * 10
    except:
        raise HTTPException(status_code=404)


@app.post('/link', response_model=list[Listing])
async def get_link(input_link: InputLink):
    time.sleep(2)
    return get_similar(input_link)
