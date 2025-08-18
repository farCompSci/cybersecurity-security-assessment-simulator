from fastapi import APIRouter, HTTPException
from ..langgraph.ai_agents.assets_generation import get_validated_assets
from ..langgraph.helpers.graph_state_classes import BusinessState

router = APIRouter()


@router.post("/generate-assets", response_model=BusinessState)
def generate_assets(business: BusinessState):
    try:
        business_with_assets = get_validated_assets(business)
        if not business_with_assets:
            raise HTTPException(status_code=500, detail="Failed to generate assets")
        return business_with_assets
    except Exception as e:
        raise e
