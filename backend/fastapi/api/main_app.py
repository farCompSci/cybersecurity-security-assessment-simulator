from fastapi import FastAPI
from .business_generation import router as business_router
from .assets_generation import router as assets_router
from .threats_generation import router as threats_router
from .business_owner_agent import router as business_owner

app = FastAPI()

app.include_router(business_router, prefix="/api/business", tags=["Business"])
app.include_router(assets_router, prefix="/api/assets", tags=["Assets"])
app.include_router(threats_router, prefix="/api/threats", tags=["Threats"])
app.include_router(business_owner, prefix="/api/chat/owner", tags=["Owner"])
