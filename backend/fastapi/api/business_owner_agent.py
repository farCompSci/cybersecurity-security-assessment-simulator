from fastapi import FastAPI, HTTPException, Body, APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uuid

from ..langgraph.nodes.business_owner_agent import invoke_business_owner_chat
from ..langgraph.helpers.graph_state_classes import BusinessState


class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message sender (e.g., 'human', 'ai').")
    content: str = Field(..., description="The text content of the message.")


class ChatRequest(BaseModel):
    business: BusinessState = Field(..., description="The full business state object, including name, description, and assets.")
    messages: List[ChatMessage] = Field(default_factory=list, description="The history of the conversation so far.")
    thread_id: Optional[str] = Field(None, description="An optional ID to track the conversation session.")


class ChatResponse(BaseModel):
    conversation: List[ChatMessage]


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat_with_business_owner(request: ChatRequest = Body(...)):
    try:
        thread_id = request.thread_id or str(uuid.uuid4())

        messages_as_dicts = [msg.dict() for msg in request.messages]
        business_dict = request.business.dict() if hasattr(request.business, "dict") else request.business
        full_conversation_dicts = invoke_business_owner_chat(
            business=business_dict,
            messages=messages_as_dicts,
            thread_id=thread_id
        )
        print("DEBUG: full_conversation_dicts =", full_conversation_dicts)
        if not full_conversation_dicts or 'error' in full_conversation_dicts[0].get('content', '').lower():
            raise HTTPException(status_code=500, detail="The chatbot failed to generate a valid response.")
        return ChatResponse(conversation=full_conversation_dicts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
