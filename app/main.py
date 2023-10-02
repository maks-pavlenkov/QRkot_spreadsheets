from fastapi import FastAPI
from app.core.config import settings
import uvicorn
from app.api.routers import main_router

app = FastAPI(title=settings.app_title)
app.include_router(main_router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)