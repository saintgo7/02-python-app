#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from app.tool import *
import json

app = FastAPI(title="44_social_media_scheduler", version="1.0.0")


@app.post("/process")
def process_data(data: dict):
    """Process data"""
    try:
        tool = Tool()
        result = tool.process(data)
        return {"result": result, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
