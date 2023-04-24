import redis.asyncio as redis

from src.conf.config import settings
from src.routes import contacts, auth, users
from sqlalchemy.orm import Session
from src.database.db import get_db
from sqlalchemy import text
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter


app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')

origins = [
    "http://localhost:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """
The startup function is called when the application starts up.
It's a good place to initialize things that are used by the app, such as databases or caches.
:return: A future, so we need to await it
:doc-author: Trelent
"""
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    """
The healthchecker function is a simple function that checks if the database is configured correctly.
It does this by executing a SQL query and checking if it returns any results. If it doesn't, then we know something's wrong.
:param db: Session: Pass the database session to the function
:return: A dictionary with a message
:doc-author: Trelent
"""
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
