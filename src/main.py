from typing_extensions import TypedDict

from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama


# -----------------------------
# Structured LLM Output
# -----------------------------

class TravelRequirements(BaseModel):
    destination: str | None = Field(
        default=None,
        description="Travel destination"
    )

    number_of_days: int | None = Field(
        default=None,
        description="Number of travel days"
    )

    number_of_travelers: int | None = Field(
        default=None,
        description="Number of travelers"
    )

    interests: list[str] = Field(
        default_factory=list,
        description="Travel interests"
    )

    budget: float | None = Field(
        default=None,
        description="Total trip budget"
    )

    currency: str | None = Field(
        default=None,
        description="Budget currency"
    )

    transportation_preference: str | None = Field(
        default=None,
        description="Transportation preference"
    )

    travel_style: str | None = Field(
        default=None,
        description="Travel style"
    )


# -----------------------------
# LangGraph State
# -----------------------------

class TripState(TypedDict, total=False):
    user_message: str

    destination: str | None
    number_of_days: int | None
    number_of_travelers: int | None
    interests: list[str]
    budget: float | None
    currency: str | None
    transportation_preference: str | None
    travel_style: str | None


# -----------------------------
# Ollama
# -----------------------------

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0,
)

structured_llm = llm.with_structured_output(
    TravelRequirements
)


# -----------------------------
# Requirements Node
# -----------------------------

def requirements_node(state: TripState):

    prompt = f"""
You are a travel requirements extraction assistant.

Extract travel requirements from the user's message.

Rules:

1. Extract only information explicitly provided by the user.
2. Do not invent missing information.
3. If information is missing, return null.
4. Convert obvious number words to numbers.
5. Keep interests as a list.
6. Extract budget as a numeric value.
7. Identify the currency when provided or clearly implied.
8. Do not create an itinerary.
9. Do not recommend places.

User message:

{state["user_message"]}
"""

    requirements = structured_llm.invoke(prompt)

    return {
        "destination": requirements.destination,
        "number_of_days": requirements.number_of_days,
        "number_of_travelers": requirements.number_of_travelers,
        "interests": requirements.interests,
        "budget": requirements.budget,
        "currency": requirements.currency,
        "transportation_preference": requirements.transportation_preference,
        "travel_style": requirements.travel_style,
    }


# -----------------------------
# Build Graph
# -----------------------------

builder = StateGraph(TripState)

builder.add_node(
    "requirements",
    requirements_node
)

builder.add_edge(
    START,
    "requirements"
)

builder.add_edge(
    "requirements",
    END
)

graph = builder.compile()


# -----------------------------
# User Input
# -----------------------------

user_message = input("You: ")

result = graph.invoke({
    "user_message": user_message
})


# -----------------------------
# Display Structured State
# -----------------------------

print("\nExtracted travel requirements:")
print(f"Destination: {result.get('destination')}")
print(f"Days: {result.get('number_of_days')}")
print(f"Travelers: {result.get('number_of_travelers')}")
print(f"Interests: {result.get('interests')}")
print(f"Budget: {result.get('budget')}")
print(f"Currency: {result.get('currency')}")
print(
    f"Transportation: "
    f"{result.get('transportation_preference')}"
)
print(f"Travel style: {result.get('travel_style')}")
