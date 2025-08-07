from fastapi import HTTPException, Body, APIRouter
from ..langgraph.helpers.file_operations import retrieve_input_file
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/retrieve-security-template", response_class=PlainTextResponse)
def get_markdown_file():
    content = retrieve_input_file("SecurityAssessmentTemplate-FrontendFile.md")
    if content is None:
        raise HTTPException(status_code=404, detail="File not found.")
    return content
