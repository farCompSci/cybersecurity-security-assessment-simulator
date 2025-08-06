from loguru import logger
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage,BaseMessage
from typing import List, Dict
from functools import partial

from ..helpers.graph_state_classes import BusinessState, AssetCollection
from ..helpers.model_config import fetch_model_from_ollama
from ..helpers.output_validation import format_items_for_llm
from ..prompts.business_owner_prompt import business_owner_prompt_message


def create_system_prompt(business: BusinessState):
    assets_info = format_items_for_llm(items=AssetCollection(assets=business["assets"].assets)) or "No assets available."
    prompt = business_owner_prompt_message.format(
        business_name=business['business_name'],
        business_description=business['business_description'],
        assets_info=assets_info
    )

    return prompt


def business_owner_node(state: MessagesState, business: BusinessState, llm:ChatOllama) -> Dict[str, list]:
    """
    Invokes the LLM with the current state and returns the new AI message.
    """
    system_prompt = ""
    try:
        system_prompt = create_system_prompt(business)
    except Exception as e:
        logger.error("Could not create system prompt")
        logger.warning(business['assets'].assets)

    messages = state['messages']

    if not messages or not isinstance(messages[0], SystemMessage):
        messages_for_llm = [SystemMessage(content=system_prompt)] + messages
    else:
        messages_for_llm = messages

    try:
        logger.debug(f"Invoking LLM with {len(messages_for_llm)} messages...")
        response = llm.invoke(messages_for_llm)
        logger.debug(f"LLM raw response: {response}")

        if isinstance(response, str):
            response = AIMessage(content=response)
        elif not isinstance(response, BaseMessage) or not response.content:
            logger.warning("LLM returned an empty or invalid response. Creating a fallback message.")
            response = AIMessage(
                content="I'm sorry, I'm not sure how to respond to that. Could you ask in a different way?")

        return {"messages": [response]}

    except Exception as e:
        logger.error(f"Error in business_owner_node: {e}")
        error_msg = AIMessage(content="I'm sorry, I'm having trouble responding right now. Please try again.")
        return {"messages": [error_msg]}


def create_business_owner_graph(business: BusinessState):
    """Creates a compiled LangGraph for the business owner chatbot."""
    llm = fetch_model_from_ollama(model_name="llama3.2", temperature=0.7)

    node_with_context = partial(business_owner_node, business=business, llm=llm)

    builder = StateGraph(MessagesState)
    builder.add_node("business_owner", node_with_context)
    builder.add_edge(START, "business_owner")
    builder.add_edge("business_owner", END)

    return builder.compile()


def invoke_business_owner_chat(business: BusinessState, messages: List[Dict[str, str]] = None, thread_id=None) -> List[
    Dict[str, str]]:
    """
    Main function to invoke the business owner chat graph.
    It manages the conversation state and returns the full history.
    """
    try:
        if messages is None:
            messages = []

        langchain_messages = []
        for msg in messages:
            role = msg.get('role', 'human')
            content = msg.get('content', '')
            if role == 'system':
                langchain_messages.append(SystemMessage(content=content))
            elif role == 'human':
                langchain_messages.append(HumanMessage(content=content))
            elif role == 'ai':
                langchain_messages.append(AIMessage(content=content))
            else:
                langchain_messages.append(HumanMessage(content=content))

        # Create the graph
        graph = create_business_owner_graph(business)

        # Invoke the graph with the current conversation history
        # The result contains the final state of the graph after execution
        result = graph.invoke(
            {"messages": langchain_messages},
            config={"configurable": {"thread_id": thread_id}}
        )

        # The result['messages'] is the complete, updated conversation history
        final_messages = result['messages']

        # We need to ensure the system prompt is part of the returned history for context
        if not final_messages or not isinstance(final_messages[0], SystemMessage):
            system_prompt = create_system_prompt(business)
            final_messages.insert(0, SystemMessage(content=system_prompt))

        # Convert LangChain message objects back to dictionaries for the response
        response_messages = []
        for msg in final_messages:
            role = 'unknown'
            if isinstance(msg, SystemMessage):
                role = 'system'
            elif isinstance(msg, HumanMessage):
                role = 'human'
            elif isinstance(msg, AIMessage):
                role = 'ai'

            response_messages.append({'role': role, 'content': msg.content})

        return response_messages

    except Exception as e:
        logger.error(f"Error in invoke_business_owner_chat: {e}")
        return [{'role': 'ai', 'content': 'I apologize, but I encountered a critical error. Please try again.'}]


if __name__ == '__main__':
    import uuid
    import sys

    # Configure Loguru to show debug messages for better diagnostics
    logger.remove()
    logger.add(sys.stderr, level="INFO")  # Change to "DEBUG" for more verbose output

    # Sample Business Data (shortened for brevity)
    business: BusinessState = {
        "business_name": "Harmony Home Cleaning",
        "business_location": "Austin, TX",
        "business_contact_info": "info@harmonyhomecleaning.com",
        "business_activity": "Professional cleaning services for residential and commercial clients.",
        "business_description": "Harmony Home Cleaning is a small business that provides top-notch cleaning services...",
        "assets": {
            "assets": [
                {"category": "Digital Assets", "description": "List of digital assets..."},
                {"category": "Asset Name", "description": "Local Server Data"},
                {"category": "Description", "description": "Office server storing schedule..."},
            ]
        },
        "potential_threats": {"threats": []}
    }

    thread_id = str(uuid.uuid4())
    print(f"Testing with thread_id: {thread_id}")

    # --- Test 1: Single message conversation ---
    print("\n" + "=" * 50)
    print("TEST 1: Single message about MFA policies")
    print("=" * 50)
    test_messages_1 = [{"role": "human", "content": "Tell me about your business MFA policies if you know."}]
    conversation_history = invoke_business_owner_chat(business, test_messages_1, thread_id)
    for msg in conversation_history:
        if msg['role'] == 'system':
            print("System: [Redacted for brevity]\n")
        else:
            print(f"{msg['role'].capitalize()}: {msg['content']}\n")

    # --- Test 2: Multi-turn conversation ---
    print("\n" + "=" * 50)
    print("TEST 2: Multi-turn conversation")
    print("=" * 50)
    # Use the full history from the previous turn for context
    conversation_history.append({"role": "human", "content": "How do you handle customer data security?"})
    final_conversation = invoke_business_owner_chat(business, conversation_history, thread_id)
    for msg in final_conversation:
        if msg['role'] == 'system':
            print("System: [Redacted for brevity]\n")
        else:
            print(f"{msg['role'].capitalize()}: {msg['content']}\n")

    # --- Test 3: Empty/None messages ---
    print("\n" + "=" * 50)
    print("TEST 3 & 4: Empty and None messages")
    print("=" * 50)
    result_3 = invoke_business_owner_chat(business, None, thread_id)
    for msg in result_3:
        if msg['role'] == 'system':
            print("System: [Redacted for brevity]\n")
        else:
            print(f"{msg['role'].capitalize()}: {msg['content']}\n")

    print("\n" + "=" * 50)
    print("All tests completed!")
    print("=" * 50)
