from fastapi import FastAPI
import os
import requests

app = FastAPI()

@app.get("/")
def ping():
  url = os.getenv("PRIVATE_SERVICE_URL")
  data = requests.get(url)
  return {"data": data.text}