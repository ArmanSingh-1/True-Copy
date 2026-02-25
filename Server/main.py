from fastapi import FastAPI
from setup.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug_mode)

@app.get("/")
def read_root():
    return {"status": "success", "message": "TrueCopy API is running smoothly."}