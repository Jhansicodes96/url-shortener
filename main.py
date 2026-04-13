from fastapi import FastAPI
from database import engine
from routes import router
import models
models.Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(router)
@app.get("/")
def home():
    return {"message": "URL Shorctner is running"}