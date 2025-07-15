from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def ping(query_param: str = ""):
  return {"data": "pong", "query_param": query_param}

@app.get("/endpoint")
def endpoint(query_param: str = ""):
  return {"data": "pong endpoint", "query_param": query_param}

