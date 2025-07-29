from langchain_core.messages import HumanMessage
from loguru import logger


from ..prompts.business_generator_prompt import business_generation_prompt_message
from ..helpers.file_operations import retrieve_input_file
from ..helpers.model_config import fetch_model_from_ollama
from ..helpers.graph_state_classes import BusinessState, BusinessOnlyState


def generate_business(business_generation_prompt: str = business_generation_prompt_message,
                       business_example_filename: str = 'Business_ZenithPoint.txt',
                       llm_model_name: str = "llama3.2") -> BusinessState | None:
    """
    Generates a business idea, using a prompt template, example, and
    :param business_generation_prompt:
    :param business_example_filename:
    :param llm_model_name:
    :return:
    """

    business_example_for_prompt_message = retrieve_input_file(f'{business_example_filename}')

    business_generation_formatted_prompt = business_generation_prompt.format(
        example=business_example_for_prompt_message)

    ollama_llm = fetch_model_from_ollama(f"{llm_model_name}")
    ollama_llm_with_structured_output = ollama_llm.with_structured_output(BusinessOnlyState)

    try:
        ollama_llm_output = ollama_llm_with_structured_output.invoke([HumanMessage(content=business_generation_formatted_prompt)])
        return ollama_llm_output
    except Exception as e:
        logger.error('Failed to produce output with Gemma. Details below:\n', e)
        return


if __name__ == "__main__":
    business = generate_business() # Implement real tests after this
    print(business)
