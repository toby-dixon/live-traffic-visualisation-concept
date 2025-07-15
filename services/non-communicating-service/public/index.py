import random
import time

from fastapi import FastAPI, Response, status

app = FastAPI()

@app.get("/")
async def ping(query_param: str = ""):
  return {"data": "pong", "query_param": query_param}

@app.get("/endpoint")
async def endpoint(response: Response, query_param: str = ""):
  if random.randint(1, 10) > 6:
    response.status_code = status.HTTP_400_BAD_REQUEST
  else:
    response.status_code = status.HTTP_200_OK

  time.sleep(random.randint(0,2))
  return {"data": "pong endpoint", "query_param": query_param}

