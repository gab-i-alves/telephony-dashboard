from fastapi import FastAPI
from routes import user 

app = FastAPI(title="Telephony Dashboard API")

app.include_router(user.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}