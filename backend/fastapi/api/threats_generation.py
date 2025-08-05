from fastapi import APIRouter, HTTPException
from ..langgraph.nodes.threats_generation import get_validated_threats
from ..langgraph.helpers.graph_state_classes import BusinessState

router = APIRouter()

@router.post("/generate-threats", response_model=BusinessState)
def generate_threats(business: BusinessState):
    try:
        business_with_threats = get_validated_threats(business)
        if not business_with_threats:
            raise HTTPException(status_code=500, detail="Failed to generate threats")
        return business_with_threats
    except Exception as e:
        raise e
