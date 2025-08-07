from fastapi import HTTPException, Body, APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

from ..langgraph.ai_agents.security_assessment_assistant import invoke_security_assistant_chat


class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message sender (e.g., 'human', 'ai').")
    content: str = Field(..., description="The text content of the message.")


class SecurityAssistantChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(default_factory=list, description="The history of the conversation so far.")
    thread_id: Optional[str] = Field(None, description="An optional ID to track the conversation session.")


class ChatResponse(BaseModel):
    conversation: List[ChatMessage]


router = APIRouter()


@router.post("/assessment-assistant", response_model=ChatResponse)
def chat_with_security_assistant(request: SecurityAssistantChatRequest = Body(...)):
    try:
        thread_id = request.thread_id or str(uuid.uuid4())

        messages_as_dicts = [msg.dict() for msg in request.messages]
        full_conversation_dicts = invoke_security_assistant_chat(
            messages=messages_as_dicts,
            thread_id=thread_id
        )

        print("DEBUG: full_conversation_dicts =", full_conversation_dicts)

        if not full_conversation_dicts or 'error' in full_conversation_dicts[0].get('content', '').lower():
            raise HTTPException(status_code=500, detail="The security assistant failed to generate a valid response.")

        return ChatResponse(conversation=full_conversation_dicts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")