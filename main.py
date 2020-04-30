
import sqlite3
from fastapi import FastAPI
from fastapi import Depends, Cookie, HTTPException, Response

import secrets

from fastapi import status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

from pydantic import BaseModel


class Album(BaseModel):
    title: str
    artist_id: int


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

  
@app.get("/tracks")
async def getgtracks():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('SELECT * FROM tracks ORDER BY TrackId LIMIT 10 OFFSET 0').fetchall()
    return data
    


@app.get("/tracks/composers/")
async def tracks_with_comp(composer_name): 
    app.db_connection.row_factory = lambda cursor, x: x[0]
    tup=(composer_name,)
    data = app.db_connection.execute('SELECT name FROM tracks WHERE composer LIKE ? ORDER BY name',tup).fetchall()
    if data ==[]:
        raise HTTPException(
        status_code=404,
        detail="error",
        )
    return data




@app.post("/albums")
async def addalbum(album: Album): 
    app.db_connection.row_factory = lambda cursor, x: x[0]
    data2 = app.db_connection.execute('SELECT artistid FROM albums').fetchall()
    if not (album.artist_id in data2):
        raise HTTPException(
        status_code=404,
        detail="error",
        )
    try:  
        t=(album.title,)
        cursor = app.db_connection.execute(
            "INSERT INTO albums (title) VALUES (?)", t
        )
        new_album_id = cursor.lastrowid
        app.db_connection.row_factory = sqlite3.Row
        album = app.db_connection.execute(
            """SELECT title FROM albums WHERE albumid = ?""",
            (new_album_id, )).fetchall()
        raise HTTPException(
            status_code=201,
            detail=str(album)
            )
    except:
        raise HTTPException(
        status_code=404,
        detail="error",
        )
   

       
        


        
