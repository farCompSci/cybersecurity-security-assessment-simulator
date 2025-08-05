from fastapi import APIRouter, HTTPException, FastAPI
from ..langgraph.nodes.business_generation import get_validated_business
from ..langgraph.nodes.assets_generation import get_validated_assets
from ..langgraph.nodes.threats_generation import get_validated_threats

from ..langgraph.helpers.graph_state_classes import BusinessState

# router = APIRouter()

router = FastAPI()

@router.get("/generate-business", response_model=BusinessState)
def generate_business():
    business = get_validated_business()
    if not business:
        raise HTTPException(status_code=500, detail="Failed to generate business")
    return business


@router.post("/generate-assets", response_model=BusinessState)
def generate_assets(business: BusinessState):
    try:
        business_with_assets = get_validated_assets(business)
        if not business_with_assets:
            raise HTTPException(status_code=500, detail="Failed to generate assets")
        return business_with_assets
    except Exception as e:
        raise e


@router.post("/generate-threats", response_model=BusinessState)
def generate_threats(business: BusinessState):
    try:
        business_with_threats = get_validated_threats(business)
        if not business_with_threats:
            raise HTTPException(status_code=500, detail="Failed to generate threats")
        return business_with_threats
    except Exception as e:
        raise e
