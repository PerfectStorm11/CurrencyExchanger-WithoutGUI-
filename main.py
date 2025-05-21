from fastapi import FastAPI, routing
import uvicorn
from src.api.apimethods import router

app = FastAPI()
app.include_router(router)
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
