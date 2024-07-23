from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import hashlib
from sqlalchemy import Select
from schemas import URLBAse, URLResponse
from database import database, urls, metadata, engine

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()
    
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    
def generate_key(url : str) -> str:
    # generate a short key using Sha_256 hash function
    return hashlib.sha256(url.encode()).hexdigest()[:6]

# create our ending point of api
@app.post("/", response_model=URLResponse)
async def create_url(url_data:URLBAse):
    query = Select(urls).where(urls.c.long_url==url_data.url)
    existing_url = await database.fetch_one(query)

    if existing_url:
        return URLResponse(
            key = existing_url["key"],
            long_url = existing_url["long_url"],
            short_url = f"http://localhost/{existing_url['key']}"
        )
        
    key = generate_key(url_data.url)
    insert_query = urls.insert().values(key=key, long_url=url_data.url)
    await database.execute(insert_query)
    return URLResponse(
        key = key,
        long_url = url_data.url,
        short_url = f"http://localhost/{key}"
    )
    
@app.exception_handler(HTTPException)
async def http_exception_handler(request:Request, exc:HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"message":exc.detail})

metadata.create_all(engine)
