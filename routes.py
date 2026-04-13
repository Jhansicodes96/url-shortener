from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
import random
import string
from pydantic import BaseModel
from database import get_db
from models import URL
router=APIRouter()
class URLRequest(BaseModel):
    original_url: str
def generate_short_code():
    character=string.ascii_letters+string.digits
    return ''.join(random.choices(character,k=6))
@router.post("/shorten")

def shorten_url(url_data:URLRequest,db:Session=Depends(get_db)):
    short_code=generate_short_code()
    while db.query(URL).filter(URL.short_code==short_code).first():
        short_code=generate_short_code()
    new_url=URL(original_url=url_data.original_url,short_code=short_code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return{
        "original_url":url_data.original_url,
        "short_code":short_code,
        "short_url":f"localhost:8000/{short_code}"
    }
@router.get("/{short_code}")
def redirect_url(short_code:str,db:Session=Depends(get_db)):
    url=db.query(URL).filter(URL.short_code==short_code).first()
    if not url:
        raise HTTPException(status_code=404,detail="URL not found")
    url.clicks+=1
    db.commit()

    return {"original_url": url.original_url}
@router.get("/stats/{short_code}")
def get_stats(short_code :str,db:Session=Depends(get_db)):
    url=db.query(URL).filter(URL.short_code==short_code).first()
    if not url:
        raise HTTPException(status_code=404,detail="URL not found")
    return{
        "original_url": url.original_url,
        "short_code": url.short_code,
        "clicks": url.clicks,
        "created_at": url.created_at
    }