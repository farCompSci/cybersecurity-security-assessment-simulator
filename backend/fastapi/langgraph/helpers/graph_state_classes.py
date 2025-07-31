from pydantic import BaseModel, Field
from typing_extensions import TypedDict, List, Annotated
from langgraph.graph import add_messages


class AssetState(BaseModel):
    category: str
    description: str


class AssetCollection(BaseModel):
    assets: List[AssetState]


class ThreatItem(BaseModel):
    category: str
    description: str


class ThreatItemCollection(BaseModel):
    threats: List[ThreatItem]


# The class below is used to generate businesses without the assets or threats. That is because it becomes too confusing for the llm otherwise
class BusinessOnlyState(BaseModel):
    """Always use this tool to structure your response to the user when asked to generate businesses."""
    business_name: str = Field(description="The generated business's name")
    business_location: str = Field(description="The location of the business")
    business_contact_info: str = Field(description="The email addresses and phone number of the business")
    business_activity: str = Field(
        description="The description of the business activities. This includes what they sell to generate revenue, whether products or services")
    business_description: str = Field(
        description="Other descriptions of the business, such as size, target audience, and other similar things.")


class BusinessState(TypedDict):
    """State representation of a business for LangGraph workflow"""
    business_name: str
    business_location: str
    business_contact_info: str
    business_activity: str
    business_description: str

    assets: AssetCollection
    potential_threats: ThreatItemCollection


class SecurityAssessmentClass(TypedDict):
    """State class to track messages in the security assessment conversation."""
    messages: Annotated[List, add_messages]
    sec_assessment_conversation_history: List
    current_section: str
    available_sections: List[str]


class BusinessValidationResult(BaseModel):
    is_valid: bool = Field(description="True if the provided output from the llm matches the prompt")
    reason: str = Field(description="Short explanation for the decision")
