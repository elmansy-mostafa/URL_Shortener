from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
import hashlib
from sqlalchemy.sql import select, delete
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
@app.post("/shorten_url/", response_model=URLResponse)
async def create_url(url_data:URLBAse):
    query = select(urls).where(urls.c.long_url==url_data.url)
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

@app.get("/{key}", response_class=RedirectResponse)
async def redirect_to_url(key:str):
    query = select(urls).where(urls.c.key == key )
    url_record = await database.fetch_one(query)
    if url_record:
        return RedirectResponse(url = url_record["long_url"], status_code=302)
    else:
        raise HTTPException(status_code=404, detail="URL not found")    
    
@app.delete("/{key}")
async def delete_url(key:str):
    query = select(urls).where(urls.c.key == key)
    url_record = await database.fetch_one(query)
    if url_record:
        delete_query = delete(urls).where(urls.c.key == key)
        await database.execute(delete_query)
    return JSONResponse(status_code=200, content={})


@app.exception_handler(HTTPException)
async def http_exception_handler(request:Request, exc:HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"message":exc.detail})

metadata.create_all(engine)
