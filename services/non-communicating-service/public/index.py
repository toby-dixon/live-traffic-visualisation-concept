from fastapi import FastAPI, Response, status

app = FastAPI()

@app.get("/")
def ping(query_param: str = ""):
  return {"data": "pong", "query_param": query_param}

@app.get("/endpoint")
def endpoint(response: Response, query_param: str = ""):
  response.status_code = status.HTTP_400_BAD_REQUEST
  return {"data": "pong endpoint", "query_param": query_param}

