from fastapi import APIRouter, HTTPException
from ..langgraph.ai_agents.business_generation import get_validated_business
from ..langgraph.helpers.graph_state_classes import BusinessState


router = APIRouter()


@router.get("/generate-business", response_model=BusinessState)
def generate_business():
    business = get_validated_business()
    if not business:
        raise HTTPException(status_code=500, detail="Failed to generate business")
    return business
