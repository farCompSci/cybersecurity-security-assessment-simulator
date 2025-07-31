from langchain_core.messages import HumanMessage
from loguru import logger
from typing import Any
from .graph_state_classes import BusinessOnlyState, BusinessValidationResult
from .model_config import fetch_model_from_ollama


def create_business_validation_prompt(original_prompt: str, generated_business: BusinessOnlyState) -> str:
    """
    Returns a prompt to validate whether the business generator's output is acceptable or not.
    :param original_prompt: the prompt that was passed to the business generator
    :param generated_business: the structured business state/object that was populated by the business generator
    :return: a dict with details about why or why not the business is acceptable
    """
    return f"""
        You are a business analyst. Decide if the following business matches the requirements.

        PROMPT:
        {original_prompt}

        BUSINESS:
        Name: {generated_business.business_name}
        Location: {generated_business.business_location}
        Contact: {generated_business.business_contact_info}
        Activity: {generated_business.business_activity}
        Description: {generated_business.business_description}

        Reply in this JSON format:
        {{
          "is_valid": true or false,
          "reason": "short explanation"
        }}
    """


def create_assets_validation_prompt(original_prompt, generated_assets):
    """
    Returns a prompt to validate whether the asset generator's output is acceptable or not.
    :param original_prompt: original prompt used to generate assets
    :param generated_assets: list of returned assets (formatted for llm to understand)
    :return: a dict with details about why or why not the business is acceptable
    """
    return f"""
    You are a business assets specialist. Decide if the following assets are appropriate for the matching business.
    
    PROMPT:
    {original_prompt}
    
    ASSETS:
    {generated_assets}
    
    Reply in this JSON format:
    {{
          "is_valid": true or false,
          "reason": "short explanation"
    }}
    """

def validate_generated_output(
    prompt: str,
    llm_model_name: str = "llama3.2"
) -> BusinessValidationResult:
    """
    Validates whether the business generated is acceptable or not.
    :param prompt: takes in prompt for validation, which is a string that contains the input and output of the business generation function
    :param llm_model_name: the name of the model based on the ollama model registry
    :return: whether the model's response is acceptable or note
    """

    ollama_llm = fetch_model_from_ollama(llm_model_name)
    ollama_llm_with_structured_output = ollama_llm.with_structured_output(BusinessValidationResult)

    try:
        return ollama_llm_with_structured_output.invoke([HumanMessage(content=prompt)])
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return BusinessValidationResult(is_valid=False, reason="Validation error")


def format_assets_for_llm(assets):
    assets_formatted = ""

    for asset in assets.assets:
        assets_formatted += f"\n- {asset.category}: {asset.description}"

    return assets_formatted
