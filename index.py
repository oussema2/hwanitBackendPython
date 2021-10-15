from fastapi import FastAPI
from routes.imagesRoutes import images
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests
import uvicorn
app = FastAPI()

app.include_router(images)
app.mount("/images", StaticFiles(directory="images"), name="images")
requests.get("http://localhost:9005/sanctum/csrf-cookie")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
