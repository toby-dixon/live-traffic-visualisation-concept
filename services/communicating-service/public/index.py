import random
import time

from fastapi import FastAPI
import os
import requests

app = FastAPI()

@app.get("/")
async def ping():
  url = os.getenv("PRIVATE_SERVICE_URL")
  data = requests.get(url)
  time.sleep(random.randint(0,2))
  return {"data": data.json()}