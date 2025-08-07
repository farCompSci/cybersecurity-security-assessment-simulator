from fastapi import FastAPI
from .business_generation import router as business_router
from .assets_generation import router as assets_router
from .threats_generation import router as threats_router
from .business_owner_agent import router as business_owner
from .security_template_retrieval import router as security_template
from .security_assessment_assistant import router as security_assessment_assistant

app = FastAPI()

app.include_router(business_router, prefix="/api/business", tags=["Business"])
app.include_router(assets_router, prefix="/api/assets", tags=["Assets"])
app.include_router(threats_router, prefix="/api/threats", tags=["Threats"])
app.include_router(business_owner, prefix="/api/chat/owner", tags=["Owner"])
app.include_router(security_template, prefix="/api/retrieve-file", tags=["Security Template"])
app.include_router(security_assessment_assistant, prefix="/api/chat", tags=["Security Assessment Assistant"])
