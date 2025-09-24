from fastapi import FastAPI

app = FastAPI(title="Telephony Dashboard API")

@app.get("/")
def read_root():
    return {"Hello": "World"}