from pydantic import BaseModel

class URLBAse(BaseModel):
    url : str

class URLInDB(BaseModel):
    key : str

class URLResponse(BaseModel):
    key : str
    long_url : str
    short_url : str