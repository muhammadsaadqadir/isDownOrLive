from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from core.config import settings
import httpx


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

async def check_website_status(url: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.head(url)
            return response.status_code < 400
    except httpx.HTTPStatusError:
        return False
    except httpx.RequestError:
        return False

@app.get("/check-website/")
async def check_website(url: str):
    is_website_up = await check_website_status(url)
    if is_website_up:
        return {"status": 1}
    else:
        # raise HTTPException(status_code=404, status=0)
        return {"status": 0}
