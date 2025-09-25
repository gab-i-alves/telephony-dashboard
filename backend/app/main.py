from fastapi import FastAPI
from app.routes import user, auth

app = FastAPI(title="Telephony Dashboard API")

app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}