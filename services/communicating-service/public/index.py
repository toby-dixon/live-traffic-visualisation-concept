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
  time.sleep(random.uniform(0,1))
  return {"data": data.json()}