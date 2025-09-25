from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user, auth, call, metric

app = FastAPI(title="Telephony Dashboard API")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],   
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(call.router)
app.include_router(metric.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}